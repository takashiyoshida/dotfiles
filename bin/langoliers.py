#!/usr/bin/env python

import argparse
import csv
import logging
import logging.handlers
import multiprocessing
import re
from time import time


YEAR  = '\d{4}'
MONTH = '[01]\d'
DAY   = '[0-3]\d'

HOUR    = '[0-2]\d'
MINUTE  = '[0-5]\d'
SECOND  = '[0-5]\d'
MSECOND = '\d{3}'

TIMESTAMP = '(?P<timestamp>%s-%s-%s %s:%s:%s\.%s)' % (YEAR, MONTH, DAY, HOUR, MINUTE,
                                                      SECOND, MSECOND)
# Allow both SCS and SIG RTU hostnames
HOSTNAME = '(?P<host>[a-z]{3}rt[su][12]) '
LEVEL    = '(?P<level>[a-z0-9]+):'
PROCESS  = '(?P<process>nelrtuapp_[a-z]{3})\[(?P<process_id>\d+)\]:'

# <filename>:?(?<line number>)?:?
FILENAME1   = '(?P<filename>[\w\-]+\.[a-z]+):?\(?(?P<line>\d+)\)?:?'
# <filename>:<function name:ignored>(<line number>):
FILENAME2   = '(?P<filename>[\w\-]+\.[a-z]+):\w+[:\(]?(?P<line>\d+)\)?:?'
# <function name:ignored> - <filename>(<line number>)
FILENAME3   = '.+ - (?P<filename>[\w\-\/]+\.[a-z]+)\((?P<line>\d+)\)'

USER_ACTION = '(?P<user>[a-z]+):'


def init_logging():
    '''
    Initialize logging
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    consoleFormatter = logging.Formatter(fmt='%(message)s')
    console.setFormatter(consoleFormatter)
    console.setLevel(logging.INFO)

    fileHandler = logging.handlers.RotatingFileHandler('langoliers_log', mode='a',
                                                       maxBytes=1000000, backupCount=10)
    fileFormatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s')
    fileHandler.setFormatter(fileFormatter)
    fileHandler.setLevel(logging.WARN)

    logger.addHandler(console)
    logger.addHandler(fileHandler)
    return logger


def purify_text(text):
    '''
    Remove non-ASCII characters from text
    '''
    cleaned = (c for c in text if 0 < ord(c) < 127)
    return ''.join(cleaned).strip()


def convert_level_num_to_level_name(text):
    '''
    '''
    levels = {0: 'emerg',
              1: 'alert',
              2: 'crit',
              3: 'err',
              4: 'warning',
              5: 'notice',
              6: 'info',
              7: 'debug'}
    try:
        num = int(text)
        if 0 < num > 7:
            text = 'unknown'
        else:
            text = levels[num]
    except:
        # the text is already a level name, not a level number
        pass
    return text


def do_work(infile, hostname='unknown'):
    events = []

    with open(infile, 'r') as logfile:
        t0 = time()
        count = 0

        for line in logfile:
            count = count + 1
            line = purify_text(line)

            match = re.match(TIMESTAMP, line)
            if match:
                event = {'timestamp': '',
                         'host': hostname, # use default hostname, first
                         'level': '',
                         'process': '',
                         'process_id': '',
                         'filename': '',
                         'line': '',
                         'user': '',
                         'message': '',
                         'raw_message': line.strip()}

                event['timestamp'] = match.group('timestamp')
                line = line[match.end():].strip()

                match = re.match(HOSTNAME, line)
                if match:
                    event['host'] = match.group('host')
                    line = line[match.end():].strip()

                match = re.match(LEVEL, line)
                if match:
                    event['level'] = convert_level_num_to_level_name(match.group('level'))
                    line = line[match.end():].strip()

                    match = re.match(PROCESS, line)
                    if match:
                        event['process'] = match.group('process')
                        event['process_id'] = match.group('process_id')
                        line = line[match.end():].strip()

                        match = re.match(FILENAME1, line)
                        if match:
                            event['filename'] = match.group('filename')
                            event['line'] = match.group('line')
                            event['message'] = line[match.end():].strip()
                        else:
                            match = re.match(FILENAME2, line)
                            if match:
                                event['filename'] = match.group('filename')
                                event['line'] = match.group('line')
                                event['message'] = line[match.end():].strip()
                            else:
                                match = re.match(FILENAME3, line)
                                if match:
                                    event['filename'] = match.group('filename')
                                    event['line'] = match.group('line')
                                    event['message'] = line[match.end():].strip()
                                else:
                                    event['message'] = line.strip()
                    else:
                        match = re.match(USER_ACTION, line)
                        if match:
                            event['user'] = match.group('user')
                            event['message'] = line[match.end():].strip()
                        else:
                            logging.error('Unable to match process name and ID in %s at %d',
                                          infile, count)
                            logging.error(line)
                else:
                    logging.error('Unable to match log level in %s at %d', infile, count)
                    logging.error(line)

                logging.debug('timestamp: %s', event['timestamp'])
                logging.debug('host: %s', event['host'])
                logging.debug('level: %s', event['level'])
                logging.debug('process: %s', event['process'])
                logging.debug('process id: %s', event['process_id']),
                logging.debug('filename: %s', event['filename']),
                logging.debug('line: %s', event['line'])
                logging.debug('user: %s', event['user'])
                logging.debug('message: %s', event['message'])
                logging.debug('raw_message: %s', event['raw_message'])

                if event['level'] == 'debug':
                    continue
                if event['message'].find('[RECEIVE DATA]') != -1:
                    continue
                if event['message'].find('[SEND DATA]') != -1:
                    continue
                if event['message'].find('0x', 0, 2) != -1:
                    continue

                events.append(event)                
            else:
                logging.error('Unable to match timestamp in %s at %d', infile, count)
                logging.error(line)

        t1 = time()
        logging.info('Extracted %d events from %s, took %.3f seconds',
                     len(events), infile, t1 - t0)
    return events


def write_events_to_csv(outfile, events):
    '''
    '''
    with open(outfile, 'w') as csvfile:
        fieldnames = ['timestamp', 'host', 'level', 'process', 'process_id',
                      'filename', 'line', 'message', 'raw_message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for event in events:
            writer.writerow({'timestamp': event['timestamp'],
                             'host': event['host'],
                             'level': event['level'],
                             'process': event['process'],
                             'process_id': event['process_id'],
                             'filename': event['filename'],
                             'line': event['line'],
                             'message': event['message'],
                             'raw_message': event['raw_message']})


def write_events_to_json(outfile, events):
    '''
    '''
    j = json.dumps(events, indent=2)
    with open(outfile, 'w') as jsonfile:
        print >> jsonfile, j
    

def main():
    '''
    main function
    '''
    parser = argparse.ArgumentParser(prog='langoliers')
    parser.add_argument('--log', '-l', required=True, nargs='+', dest='logs',
                        help='')
    parser.add_argument('--csv', '-c', required=False, dest='csvfile',
                        help='')
    parser.add_argument('--json', '-j', required=False, dest='jsonfile',
                        help='')
    parser.add_argument('--name', '-n', required=False, default='unknown', dest='name',
                        help='')
    parser.add_argument('--pool', '-p', required=False, type=int, default=1, dest='pool',
                        help='')
    args = parser.parse_args()

    init_logging()

    t0 = time()
    results = []

    pool = multiprocessing.Pool(args.pool)
    # do something useful here
    for infile in args.logs:
        result = pool.apply_async(do_work, [infile, args.name])
        results.append(result)
    pool.close()
    pool.join()

    t1 = time()
    events = []
    for result in results:
        events.extend(result.get())

    logging.info('Extracted %d events, took %.3f seconds', len(events), t1 - t0)
    if len(events) > 0:
        events.sort(key=lambda event: event['timestamp'])

    if args.csvfile:
        write_events_to_csv(args.csvfile, events)
    if args.jsonfile:
        write_events_to_json(args.jsonfile, events)

    
if __name__ == "__main__":
    main()

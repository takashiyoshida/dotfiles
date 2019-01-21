#!/usr/bin/env python

import argparse
import csv
import logging
import logging.handlers
import re

YEAR  = '\d{4}'
MONTH = '[0-2]\d'
DAY   = '[0-3]\d'

HOUR    = '[0-2]\d'
MINUTE  = '[0-5]\d'
SECOND  = '[0-5]\d'
MSECOND = '\d{3}'

TIMESTAMP   = '(?P<timestamp>%s-%s-%s %s:%s:%s\.%s)' \
              % (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, MSECOND)
HOST        = '(?P<host>[a-z]{3}rtu[12]) '
LEVEL       = '(?P<level>[a-z0-9]+):'
PROCESS     = '(?P<process>nelrtuapp_[a-z]{3})\[(?P<process_id>\d+)\]:'


# <filename>:?(?<line number>)?:?
FILENAME1   = '(?P<filename>[\w\-]+\.[a-z]+):?\(?(?P<line>\d+)\)?:?'
# <filename>:<function name:ignored>(<line number>):
FILENAME2   = '(?P<filename>[\w\-]+\.[a-z]+):\w+[:\(]?(?P<line>\d+)\)?:?'
# <function name:ignored> - <filename>(<line number>)
FILENAME3   = '.+ - (?P<filename>[\w\-\/]+\.[a-z]+)\((?P<line>\d+)\)'
USER_ACTION = '(?P<user>[a-z]+):'


def init_logger():
    '''
    Initialize logger
    '''
    f = logging.Formatter(fmt='%(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setFormatter(f)
    console.setLevel(logging.INFO)
    logger.addHandler(console)
    return logger


def purify_text(line):
    '''
    Remove non-ASCII characters from the text
    '''
    cleaned = (c for c in line if 0 < ord(c) < 127)
    return ''.join(cleaned)


def convert_level_num_to_level_name(text):
    '''
    Convert the level number to the level name
    Note that the level should be logged as string (i.e. 'err') rather than number (3)
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
            return 'unknown'
        return levels[num]
    except:
        pass
    return text


def parse_log(infile, server='unknown'):
    '''
    '''
    events = []

    with open(infile, 'r') as logs:
        count = 0 # line number
        for line in logs:
            count = count + 1
            line = purify_text(line)

            match = re.match(TIMESTAMP, line)
            if match:
                event = {'timestamp': '',
                         'host': '',
                         'level': 'debug', # default value
                         'process': '',
                         'process_id': '',
                         'filename': '',
                         'line': '',
                         'user': '',
                         'message': '',
                         'raw_message': ''}

                event['timestamp'] = match.group('timestamp')
                event['raw_message'] = '"%s"' % (line.strip())
                line = line[match.end():].strip()

                match = re.match(HOST, line)
                if match:
                    event['host'] = match.group('host')
                    line = line[match.end():].strip()
                else:
                    # Prior to release 1.0.2, the log does not contain hostname
                    # so we need to specify the RTU hostname
                    event['host'] = server

                match = re.match(LEVEL, line)
                if match:
                    # Under some circumstances, the log level appears as a number,
                    # instead of log level name (i.e. err, debug)
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
                            line = line[match.end():].strip()
                            event['message'] = line
                        else:
                            match = re.match(FILENAME2, line)
                            if match:
                                event['filename'] = match.group('filename')
                                event['line'] = match.group('line')
                                line = line[match.end():].strip()
                                event['message'] = line
                            else:
                                match = re.match(FILENAME3, line)
                                if match:
                                    event['filename'] = match.group('filename')
                                    event['line'] = match.group('line')
                                    line = line[match.end():].strip()
                                    event['message'] = line
                                else:
                                    # This is likely to be a SWC log
                                    event['message'] = line
                    else:
                        match = re.match(USER_ACTION, line)
                        if match:
                            event['user'] = match.group('user')
                            line = line[match.end():].strip()
                            event['message'] = line
                        else:
                            logging.error('Unable to match process name and ID in %s at %d', infile, count)
                            logging.error(line)
                else:
                    logging.error('Unable to match log level in %s at %d', infile, count)
                    logging.error(line)

                logging.debug('TIMESTAMP: %s', event['timestamp'])
                logging.debug('HOST: %s', event['host'])
                logging.debug('LEVEL: %s', event['level'])
                logging.debug('PROCESS: %s', event['process'])
                logging.debug('PROCESS_ID: %s', event['process_id'])
                logging.debug('FILENAME: %s', event['filename'])
                logging.debug('LINE: %s', event['line'])
                logging.debug('USER: %s', event['user'])
                logging.debug('MESSAGE: %s', event['message'])
                logging.debug('RAW_MESSAGE: %s', event['raw_message'])

                # We choose not to store debug-level log (there are too many)
                if event['level'] == 'debug':
                    continue
                # Also, ignore SWC-log
                if event['message'][0:2] == '0x': 
                    continue

                events.append(event)
            else:
                logging.error('Unable to match timestamp in %s at %d', infile, count)
                logging.error(line)
    return events


def write_events_to_csvfile(events, csvfile):
    '''
    '''
    with open(csvfile, 'w') as csvfile:
        fieldnames = ['timestamp', 'host', 'level', 'process', 'process_id', 'filename',
                      'line', 'message', 'raw_message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
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

    
def main():
    init_logger()

    parser = argparse.ArgumentParser(prog='rturep-loggr')
    parser.add_argument('--log', '-l', required=True, nargs='+', dest='logs')
    parser.add_argument('--server', '-s', required=False, dest='server')
    parser.add_argument('--csv', '-c', required=True, dest='csvfile')
    args = parser.parse_args()

    history = []
    for log in args.logs:
        events = parse_log(log, args.server)
        logging.info('Extracted %d events from %s', len(events), log)
        history.extend(events)

    if len(history):
        history.sort(key=lambda r: r['timestamp'])
        write_events_to_csvfile(history, args.csvfile)
    

if __name__ == "__main__":
    main()

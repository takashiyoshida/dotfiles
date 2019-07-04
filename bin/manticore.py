#!/usr/bin/env python

import argparse
import csv
import logging
import logging.handlers
import os
import re
import shutil
import subprocess
import tempfile
from time import time


class Cookies:
    def __init__(self):
        '''
        '''
        self._cookie_file = '%s/.manticore' % (os.environ['HOME'])
        self._cookies = []
        self.load_cookies()

    def load_cookies(self):
        '''
        '''
        try:
            with open(self._cookie_file, 'r') as cookies:
                for cookie in cookies:
                    self._cookies.append(cookie)
        except:
            pass

    def is_processed(self, filepath):
        '''
        '''
        return filepath in self._cookies

    def save_cookie(self, filepath):
        '''
        '''
        if not self.is_processed(filepath):
            self._cookies.append(cookie)
            with open(self._cookie_file, 'w+') as cookies:
                cookies.write(filepath)


def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    c = logging.StreamHandler()
    c_formatter = logging.Formatter(fmt='%(levelname)s %(message)s')
    c.setFormatter(c_formatter)
    c.setLevel(logging.INFO)

    f = logging.FileHandler('manticore.log')
    f_formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(message)s')
    f.setFormatter(f_formatter)
    f.setLevel(logging.INFO)

    logger.addHandler(c)
    logger.addHandler(f)
    return logger


def uncompress_tar(tarfile, destination):
    logging.info('Uncompressing a tarfile, %s to %s', tarfile, destination)
    return subprocess.call(['/bin/tar', 'xzf', tarfile, '-C', destination])


def uncompress_gzip(gzipfile, destination):
    logging.info('Uncompressing a gzipfile, %s to %s', gzipfile, destination)
    return subprocess.call(['/bin/gunzip', gzipfile])


def filter_nelrtu_logs(directory):
    '''
    '''
    result = -1
    logfiles = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith('nelrtu.log'):
                filename, ext = os.path.splitext(file)
                if ext.lower() == '.gz':
                    logging.info('Expanding %s ...', file)
                    gzipfile = '%s/%s' % (root, file)
                    result = uncompress_gzip(gzipfile, root)
                    if result != 0:
                        logging.error(
                            'Failed to expand %s successfully', gzipfile)
                        continue
                else:
                    filename = file
                logfile = '%s/%s' % (root, filename)
                logging.info('Adding %s to a list for processing', logfile)
                logfiles.append(logfile)
            else:
                logging.warning(
                    '%s does not match the expected filename', file)
    return logfiles


def purify_text(text):
    '''
    Remove non-ASCII characters from text
    '''
    clean = (c for c in text if 0 < ord(c) < 127)
    return ''.join(clean).strip()


def convert_level_num_to_name(text):
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


YEAR = r'\d{4}'
MONTH = r'[01]\d'
DAY = r'[0-3]\d'

HOUR = r'[0-2]\d'
MINUTE = r'[0-5]\d'
SECOND = r'[0-5]\d'
MSECOND = r'\d{3}'

TIMESTAMP = r'(?P<timestamp>%s-%s-%s %s:%s:%s\.%s)' % (YEAR, MONTH, DAY, HOUR, MINUTE,
                                                       SECOND, MSECOND)
HOSTNAME = r'(?P<host>[a-z]{3}rt[su][12]) '
LEVEL = r'(?P<level>[a-z0-9]+):'
PROCESS = r'(?P<process>nelrtuapp_[a-z]{3})\[(?P<process_id>\d+)\]:'

# <filename>:?(?<line number>)?:?
FILENAME1 = r'(?P<filename>[\w\-]+\.[a-z]+):?\(?(?P<line>\d+)\)?:?'
# <filename>:<function name:ignored>(<line number>):
FILENAME2 = r'(?P<filename>[\w\-]+\.[a-z]+):\w+[:\(]?(?P<line>\d+)\)?:?'
# <function name:ignored> - <filename>(<line number>)
FILENAME3 = r'.+ - (?P<filename>[\w\-\/]+\.[a-z]+)\((?P<line>\d+)\)'

USER_ACTION = r'(?P<user>[a-z]+):'


def process_nelrtu_log(infile, hostname='unknown'):
    '''
    Parses a given NELRTU log file and returns a list of events contained
    in the log file.
    - DEBUG level events are ignored
    - Hexdump events are also ignored
    '''

    logging.info('Processing file, %s ...', infile)
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
                         'host': hostname,  # use default hostname, first
                         'level': '',
                         'process': '',
                         'process_id': '',
                         'filename': '',
                         'line': '',
                         'user': '',
                         'message': ''}

                event['timestamp'] = match.group('timestamp')
                line = line[match.end():].strip()

                match = re.match(HOSTNAME, line)
                if match:
                    event['host'] = match.group('host')
                    line = line[match.end():].strip()

                match = re.match(LEVEL, line)
                if match:
                    event['level'] = convert_level_num_to_name(
                        match.group('level'))
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
                                    event['message'] = line[match.end()                                                            :].strip()
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
                    logging.error(
                        'Unable to match log level in %s at %d', infile, count)
                    logging.error(line)

                if event['level'] == 'debug':
                    continue

                # Only keep the SWC log with 0x000000: otherwise, drop all other SWC log
                # and event['message'].find('0x000000') == -1:
                if event['message'].find('0x') != -1:
                    continue

                logging.debug('timestamp: %s', event['timestamp'])
                logging.debug('host: %s', event['host'])
                logging.debug('level: %s', event['level'])
                logging.debug('process: %s', event['process'])
                logging.debug('process id: %s', event['process_id']),
                logging.debug('filename: %s', event['filename']),
                logging.debug('line: %s', event['line'])
                logging.debug('user: %s', event['user'])
                logging.debug('message: %s', event['message'])

                events.append(event)
            else:
                logging.error(
                    'Unable to match timestamp in %s at %d', infile, count)
                logging.error(line)

        t1 = time()
        logging.info('Extracted %d events from %s, took %.3f seconds',
                     len(events), infile, t1 - t0)
    return events


def write_events_to_csv(outfile, events):
    '''
    Writes a list of events to a CSV file
    '''
    with open(outfile, 'w') as csvfile:
        fieldnames = ['timestamp', 'host', 'level', 'process', 'process_id',
                      'filename', 'line', 'message']
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
                             'message': event['message']})


def cleanup(directory):
    logging.info('Removing the directory, %s ...', directory)
    shutil.rmtree(directory)


def do_work(root, file, dry_run=True, keep=False):
    '''
    Look for NELRTU log files and process the log files
    '''
    logging.info('Processing %s/%s ...', root, file)

    # We will only process tarballs created by our backup script
    if file.find('_DailyNELRTULog_') == -1:
        logging.warning('%s does not match the expected filename', file)
        return

    filename, ext = os.path.splitext(file)
    # We expect that the file to have '.gz' extension
    if ext.lower() != '.gz':
        logging.warning('Found unknown file type, %s, skipping ...', file)
        return

    tempdir = tempfile.mkdtemp()
    tarfile = '%s/%s' % (root, file)
    result = uncompress_tar(tarfile, tempdir)

    if result == 0:
        logdir = '%s/var/log' % (tempdir)
        logfiles = filter_nelrtu_logs(logdir)

        if len(logfiles) > 0:
            events = []
            for log in logfiles:
                ev = process_nelrtu_log(log)
                events.extend(ev)

            if len(events) > 0:
                # Remove the .tar from filename
                filename, _ = os.path.splitext(filename)
                csvfile = '%s/%s.csv' % (root, filename)
                write_events_to_csv(csvfile, events)

    if not keep:
        cleanup(tempdir)


def main():
    init_logging()

    parser = argparse.ArgumentParser(prog='manticore')
    parser.add_argument('--directory', '-d', required=True,
                        dest='directory', help='path to NELRTU log directory')
    parser.add_argument('--dry-run', '-r', required=False, action='store_true',
                        default=True, dest='dry_run',
                        help='Traverses the given directory, but does not process the discovered NELRTU log files')
    parser.add_argument('--keep', '-k', required=False, action='store_true',
                        default=False, dest='keep',
                        help='Keep temporary files for debugging purpose')
    args = parser.parse_args()

    cookies = Cookies()

    for root, _, files in os.walk(args.directory):
        for file in files:
            if not cookies.is_processed('%s/%s' % (root, file)):
                do_work(root, file, args.dry_run, args.keep)
                cookies.save_cookie('%s/%s' % (root, file))


if __name__ == "__main__":
    main()

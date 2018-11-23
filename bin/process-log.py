#!/usr/bin/env python

from __future__ import print_function
import argparse
import csv
import re

# 2018-11-10 02:41:34.254 err: nelrtuapp_lan[1948]: cse_erserver.c(1332):2:Unknown error -5519
# Regex patterns
YEAR = '\d{4}'
MONTH = '[01]\d'
DAY = '[0-3]\d'
HOUR = '[0-2]\d'
MINUTE = '[0-5]\d'
SECOND = '[0-5]\d'

TIMESTAMP = '%s-%s-%s %s:%s:%s\.\d{3}' % (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND)
LOG_LEVEL = '[a-z]{3,}'
PROCESS = 'nelrtuapp_[a-z]{3}'
PROCESS_ID = '\d+'
FILENAME = '\w+\.[a-z]{1,}'
LINE_NO = '\d+'
USER = '[a-z]+'
MESSAGE = '.+'

LOG_PATTERN_1 = '(?P<timestamp>%s) (?P<level>%s): (?P<process>%s)\[(?P<process_id>%s)\]: (?P<filename>%s):?\(?(?P<line_no>%s)\)?[:\s]?(?P<message>%s)' % (TIMESTAMP, LOG_LEVEL, PROCESS, PROCESS_ID, FILENAME, LINE_NO, MESSAGE)

LOG_PATTERN_2 = '(?P<timestamp>%s) (?P<level>%s): (?P<process>%s)\[(?P<process_id>%s)\]: (?P<message>%s)' % (TIMESTAMP, LOG_LEVEL, PROCESS, PROCESS_ID, MESSAGE)

LOG_PATTERN_3 = '(?P<timestamp>%s) (?P<level>%s): (?P<user>%s): (?P<message>%s)' % (TIMESTAMP, LOG_LEVEL, USER, MESSAGE)

def main():
    parser = argparse.ArgumentParser(prog='process-log.py')
    parser.add_argument('--log', '-l', nargs='+', required=True,
                        help='nelrtu.log', dest='logs')
    parser.add_argument('--csv', '-c', required=True, help='write logs to a CSV file',
                        dest='csv')
    parser.add_argument('--server', '-s', required=True, help='RTU host',
                        dest='server')
    args = parser.parse_args()

    events = []
    for infile in args.logs:
        with open(infile, 'r') as log:
            line_num = 0
            for line in log:
                line_num = line_num + 1
                event = {}

                match = re.match(LOG_PATTERN_1, line)
                if match:
                    event['timestamp'] = match.group('timestamp')
                    event['level'] = match.group('level')
                    event['process'] = match.group('process')
                    event['process_id'] = match.group('process_id')
                    event['filename'] = match.group('filename')
                    event['line_no'] = match.group('line_no')
                    event['message'] = match.group('message')
                else:
                    match = re.match(LOG_PATTERN_2, line)
                    if match:
                        event['timestamp'] = match.group('timestamp')
                        event['level'] = match.group('level')
                        event['process'] = match.group('process')
                        event['process_id'] = match.group('process_id')
                        event['filename'] = ''
                        event['line_no'] = ''
                        event['message'] = match.group('message')
                    else:
                        match = re.match(LOG_PATTERN_3, line)
                        if match:
                            event['timestamp'] = match.group('timestamp')
                            event['level'] = match.group('level')
                            event['process'] = match.group('user')
                            event['process_id'] = ''
                            event['filename'] = ''
                            event['line_no'] = ''
                            event['message'] = match.group('message')
                        else:
                            print('No match')
                            print(line)

                if event.has_key('message'):
                    if event['message'] == '[RECEIVE DATA]':
                        continue
                    if event['message'] == '[SEND DATA]':
                        continue
                    if event['message'] == 'Protocol data is NULL. Nothing to log':
                        continue
                    if event['message'][0:2] == '0x':
                        continue
                    event['host'] = args.server
                    events.append(event)
                else:
                    print('ERROR: %s - %d has no `message`' % (infile, line_num))
                    print(line)

    with open(args.csv, 'w') as csvfile:
        fieldnames = ['timestamp', 'level', 'process', 'process_id', 'filename', 'line_no', 'message', 'host']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        for e in events:
            writer.writerow({'timestamp': e['timestamp'],
                             'level': e['level'],
                             'process': e['process'],
                             'process_id': e['process_id'],
                             'filename': e['filename'],
                             'line_no': e['line_no'],
                             'message': e['message'],
                             'host': e['host']})
    
if __name__ == "__main__":
    main()

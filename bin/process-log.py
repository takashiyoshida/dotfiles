#!/usr/bin/env python

from __future__ import print_function
import argparse
import csv
import re

# 2018-11-10 02:41:34.254 err: nelrtuapp_lan[1948]: cse_erserver.c(1332):2:Unknown error -5519
# Regex patterns
YEAR = '[0-9]{4}'
MONTH = '[0-1][0-9]'
DAY = '[0-3][0-9]'
HOUR = '[0-2][0-9]'
MINUTE = '[0-5][0-9]'
SECOND = '[0-5][0-9]'

TIMESTAMP = '%s-%s-%s %s:%s:%s\.[0-9]{3}' % (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND)
LOG_LEVEL = '[a-z]{3,}'
PROCESS = 'nelrtuapp_[a-z]{3}'
PROCESS_ID = '[0-9]+'
FILENAME = '[A-Za-z0-9_]+\.[a-z]{1,3}'
LINE_NO = '[0-9]+'
USER = '[a-z]+'
MESSAGE = '.+'

LOG_PATTERN_1 = '(?P<timestamp>%s) (?P<level>%s): (?P<process>%s)\[(?P<process_id>%s)\]: (?P<filename>%s)\(?(?P<line_no>%s)\)?:?\s*(?P<message>%s)' % (TIMESTAMP, LOG_LEVEL, PROCESS, PROCESS_ID, FILENAME, LINE_NO, MESSAGE)

LOG_PATTERN_2 = '(?P<timestamp>%s) (?P<level>%s): (?P<process>%s)\[(?P<process_id>%s)\]: (?P<message>%s)' % (TIMESTAMP, LOG_LEVEL, PROCESS, PROCESS_ID, MESSAGE)

LOG_PATTERN_3 = '(?P<timestamp>%s) (?P<level>%s): (?P<user>%s): (?P<message>%s)' % (TIMESTAMP, LOG_LEVEL, USER, MESSAGE)


def main():
    parser = argparse.ArgumentParser(prog='process-log.py')
    parser.add_argument('--log', '-l', nargs='+', required=True,
                        help='nelrtu.log', dest='logs')
    parser.add_argument('--csv', '-c', required=True, help='write logs to a CSV file',
                        dest='csv')
    args = parser.parse_args()
    print(args)

    events = []
    for infile in args.logs:
        with open(infile, 'r') as log:
            for line in log:
                event = {}
                match = re.match(LOG_PATTERN_1, line)
                if match:
                    #print(match.groups())
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
                        #print(match.groups())
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
                            #print(match.groups())
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
                events.append(event)

    with open(args.csv, 'w') as csvfile:
        fieldnames = ['timestamp', 'level', 'process', 'process_id', 'filename', 'line_no', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for e in events:
            writer.writerow({'timestamp': e['timestamp'],
                             'level': e['level'],
                             'process': e['process'],
                             'process_id': e['process_id'],
                             'filename': e['filename'],
                             'line_no': e['line_no'],
                             'message': e['message']})
    
if __name__ == "__main__":
    main()

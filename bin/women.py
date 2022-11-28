#!/usr/bin/env python

import argparse
import csv
import re

DATE = r'[0-3][0-9]/[01][0-9]/\d{2}'
TIME = r'[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
TIMESTAMP = '%s %s' % (DATE, TIME)

LOG_PATTERN = r'(?P<timestamp>%s) - (?P<message>[\w\s]+) - (?P<filename>[\w\.]+) : (?P<line>\d+) - (?P<level>\d+)' % (
    TIMESTAMP)


def main():
    '''
    main function
    '''
    parser = argparse.ArgumentParser(prog='women')
    parser.add_argument('--log',
                        '-l',
                        nargs='+',
                        required=True,
                        dest='logfiles',
                        help='path to MEN RTU log files')
    parser.add_argument('--name',
                        '-n',
                        required=True,
                        dest='hostname',
                        help='name of RTU hardware')
    parser.add_argument('--csv',
                        '-c',
                        required=True,
                        dest='csvfile',
                        help='write RTU events to a CSV file')

    args = parser.parse_args()

    events = []
    for infile in args.logfiles:
        with open(infile, 'r') as logfile:
            for line in logfile:
                line = line.strip()

                match = re.match(LOG_PATTERN, line)
                if match:
                    # print(match.groups())
                    event = {
                        'timestamp': match.group('timestamp'),
                        'message': match.group('message'),
                        'filename': match.group('filename'),
                        'line': int(match.group('line')),
                        'level': int(match.group('level')),
                        'host': args.hostname
                    }
                    events.append(event)

    with open(args.csvfile, 'w') as csvfile:
        fieldnames = [
            'timestamp', 'message', 'filename', 'line', 'level', 'host'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for event in events:
            writer.writerow({
                'timestamp': event['timestamp'],
                'message': event['message'],
                'filename': event['filename'],
                'line': event['line'],
                'level': event['level'],
                'host': event['host']
            })


if __name__ == "__main__":
    main()

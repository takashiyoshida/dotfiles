#!/usr/bin/env python

import argparse
import logging
import logging.handlers
import re

BEGIN_MESSAGE = 1
BEGIN_PATH = 2
END_PATH = 3

def init_logging():
    ''' Initialize logging '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(console_formatter)
    console.setLevel(logging.DEBUG)
    logger.addHandler(console)

    logfile = logging.FileHandler('svn-diagram.log')
    logfile_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    logfile.setFormatter(logfile_formatter)
    logfile.setLevel(logging.DEBUG)
    logger.addHandler(logfile)

    return logger

def main():
    ''' Main function '''
    parser = argparse.ArgumentParser(description='Generate a diagram of SVN branches')
    parser.add_argument('--infile', '-i', required=True, help='text file containing Subversion log', dest='datafile')
    parser.add_argument('--outfile', '-o', required=False, help='output file name', dest='outfile')
    parser.add_argument('--rename', '-r', action='store_true' , required=False, help='rename trunk to main', dest='rename')
    args = parser.parse_args()


    init_logging()

    state = END_PATH

    events = []
    event = {'revision': '', 'message': '', 'checkout': '', 'branch': ''}

    with open(args.datafile, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()

            match = re.match(r'^Revision: (?P<revision>\d+)', line)
            if match:
                event['revision'] = match.group('revision').strip()
                logging.debug('commit id: "%s"', event['revision'])
                continue

            match = re.match(r'^Message:', line)
            if match:
                state = BEGIN_MESSAGE
                logging.debug('Next line is a commit message')
                continue

            match = re.match(r'^---', line)
            if match:
                logging.debug('End of commit message')
                state = BEGIN_PATH
                continue

            if state == BEGIN_MESSAGE:
                if line.strip() != '':
                    if event['message'] == '':
                        event['message'] = '# ' + line.strip()
                    else:
                        event['message'] += '\n' + '# ' + line.strip()
                    logging.debug('%s', event['message'])
                    # print(f'# {event['message']}')
            elif state == BEGIN_PATH:
                if line.strip() != '':
                    match = re.match(r'^Added : (?P<branch>.+) \(Copy from path: (?P<checkout>.+), Revision, \d+\)', line)
                    if match:
                        if len(match.group('branch').split('/')) <= 4:
                            event['checkout'] = '/'.join(match.group('checkout').split('/')[2:])
                            event['branch'] = '/'.join(match.group('branch').split('/')[2:])

                            if args.rename:
                                if event['branch'].startswith('trunk'):
                                    event['branch'] = 'main'
                                if event['checkout'].startswith('trunk'):
                                    event['checkout'] = 'main'
                                    
                            logging.debug('checkout: "%s"', event['checkout'])
                            logging.debug('branch: "%s"', event['branch'])
                else:
                    state = END_PATH
                    events.append(event)
                    event = {'revision': '', 'message': '', 'checkout': '', 'branch': ''}


    if len(events) > 0:
        if args.outfile:
            with open(args.outfile, 'w', encoding='utf-8') as outfile:
                outfile.write('gitGraph\n')
                for e in events:
                    if e['checkout'] != '':
                        outfile.write(f'checkout \"{e['checkout']}\"\n')
                    if e['branch'] != '':
                        outfile.write(f'branch \"{e['branch']}\"\n')
                    outfile.write(f'{e['message']}\n')
                    outfile.write(f'commit id: \"{e['revision']}\"\n')
        else:
            for e in events:
                if e['checkout'] != '':
                    print(f'checkout \"{e['checkout']}\"\n')
                if e['branch'] != '':
                    print(f'branch \"{e['branch']}\"\n')
                print(f'{e['message']}\n')
                print(f'commit id: \"{e['revision']}\"')
    else:
        print('No events were extracted from {args.datafile} ...')


if __name__ == '__main__':
    main()

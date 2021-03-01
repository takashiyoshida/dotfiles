#!/usr/bin/env python

import argparse
import re
import subprocess


def main():
    '''
    '''
    parser = argparse.ArgumentParser(prog='svn-find-branch',
                                     description='Find branches created from a given branch name',
                                     epilog='Use svn log -r <begin:end> -v <SVN_URL> > svn_log.txt to create a log file')
    parser.add_argument('--log', '-l', required=True, dest='logfile',
                        help='svn log file to parse')
    parser.add_argument('--parent', '-p', dest='parent',
                        help='parent branch')

    args = parser.parse_args()

    my_regexp = re.compile(
        r'(?P<revision>[0-9]+) \| (?P<author>.+) \| (?P<date>....-..-.. ..:..:.. \+....) \(.+\) \| [0-9]+ lines?\n'
        r'Changed paths:\n'
        r'\s*A (?P<branch>.+) \(from ' + args.parent +
        r'(?P<brevision>:[0-9]+)\)\n'
        r'\n'
        r'(?P<message>.+)\n')

    with open(args.logfile, 'r') as f:
        matches = my_regexp.finditer(f.read())

    for m in matches:
        print('%s created from %s%s on %s by %s' %
              (m.group('branch'), args.parent, m.group('brevision'), m.group('date'), m.group('author')))


if __name__ == '__main__':
    main()

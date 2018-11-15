#!/usr/bin/env python

from __future__ import print_function

import argparse
import feedparser
import os
import sys

def eprint(*args, **kwargs):
    '''
    Print to stderr
    '''
    print(*args, file=sys.stderr, **kwargs)
                                                                                

def main():
    parser = argparse.ArgumentParser(prog='download-jira-issues-rss-feed')
    parser.add_argument('--user', '-u', required=False, help='JIRA username', dest='username')
    parser.add_argument('--pass', '-p', required=False, help='JIRA password', dest='password')
    parser.add_argument('--filter-url', '-f', required=True, help='JIRA issue filter URL', dest='filter')
    parser.add_argument('--show-tasks', '-t', required=False, action='store_true',
                        help='A list of JIRA tasks found from a given filter', dest='tasks')

    args = parser.parse_args()
    if not args.username:
        if "JIRA_USER" in os.environ and os.environ['JIRA_USER'] != '':
            args.username = os.environ['JIRA_USER']
        else:
            eprint('Error: Missing JIRA username')
            eprint('Export JIRA_USER variable or use `--user` parameter to pass your JIRA username')
            sys.exit(1)

    if not args.password:
        if "JIRA_PASS" in os.environ and os.environ['JIRA_PASS'] != '':
            args.password = os.environ['JIRA_PASS']
        else:
            eprint('Error: Missing JIRA password')
            eprint('Export JIRA_PASS variable or use --user parameter to pass your JIRA password')
            sys.exit(1)

    credential = '%s:%s@' % (args.username, args.password)
    
    index = args.filter.index('jira')
    rss_feed = args.filter[:index] + credential + args.filter[index:]

    d = feedparser.parse(rss_feed)

    print(d.feed.title)
    print(d.feed.issue['total'])

    if args.tasks:
        for e in d.entries:
            print(e.title, e.link)

if __name__ == "__main__":
    main()

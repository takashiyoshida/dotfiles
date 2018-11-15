#!/usr/bin/env python

from __future__ import print_function
import sys

feed = ['http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-rss/15417/SearchRequest-15417.xml?tempMax=1000',
        'http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-rss/15418/SearchRequest-15418.xml?tempMax=1000']


def eprint(*args, **kwargs):
    '''
    Print to stderr
    '''
    print(*args, file=sys.stderr, **kwargs)


def main():
    parser = argparse.ArgumentParser(prog='dl-feature-progress')
    parser.add_argument('--user', '-u', required=False, help='JIRA username', dest='username')
    parser.add_argument('--pass', '-p', required=False, help='JIRA password', dest='password')

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

    credential = '%s:%s@' (args.username, args.password)

                                                                            
if __name__ == "__main__":
    main()

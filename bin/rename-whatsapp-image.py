#!/usr/bin/env python

import argparse
import re
from datetime import datetime
from os import path
import shutil

REGEX_DATE = r'[0-9]{4}-[01][0-9]-[0-3][0-9]'
REGEX_TIME = r'[0-9]{1,2}\.[0-5][0-9]\.[0-5][0-9] [AP]M'
REGEX_TIMESTAMP = r'(?P<timestamp>%s at %s)' % (REGEX_DATE, REGEX_TIME)


def main():
    parser = argparse.ArgumentParser(prog='rename-whatsapp-image.py')
    parser.add_argument('--image', '-i', required=True, dest='image',
                        help='Image file downloaded from WhatsApp application')
    args = parser.parse_args()

    # WhatsApp Image 2019-07-21 at 2.34.38 PM.jpeg
    # 2019-07-21-023438-WhatsApp-Image.jpg
    match = re.search(REGEX_TIMESTAMP, args.image)
    if match:
        ts = datetime.strptime(match.group('timestamp'),
                               '%Y-%m-%d at %I.%M.%S %p')
        prefix = ts.strftime('%Y-%m-%d-%H%M%S')
        new_name = prefix + '-WhatsApp-Image.jpg'
        dirname = path.dirname(args.image)
        shutil.move(args.image, dirname + '/' + new_name)


if __name__ == "__main__":
    main()

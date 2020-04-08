#!/usr/bin/env python

import argparse
import csv


def main():
    '''
    '''
    parser = argparse.ArgumentParser(prog='foobar')
    parser.add_argument('--input', '-i', required=True, dest='infile',
                        help='CVS file')
    parser.add_argument('--output', '-o', required=True, dest='outfile',
                        help='CSV file')
    args = parser.parse_args()

    new_data = []
    with open(args.infile, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            description = row[6]
            text = ''
            for ch in description:
                if ch.isdigit():
                    text += '\r\n'
                text += ch

            print(text.strip())

            new_row = [row[0], row[1], row[2], row[3],
                       row[4], row[5], text.strip(), row[7], row[8]]
            new_data.append(new_row)

    with open(args.outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        for row in new_data:
            writer.writerow(row)


if __name__ == "__main__":
    main()

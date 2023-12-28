#!/usr/bin/env python

import argparse
import sys

from bs4 import BeautifulSoup


def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
        prog="youtube-history", description="Youtube History Parser"
    )
    parser.add_argument(
        "--input", "-i", required=True, dest="infile", help="Youtube History HTML file"
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="outfile",
        help="Markdown file to write to (default: stdout)",
    )
    args = parser.parse_args()

    try:
        with open(args.infile, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            youtube_links = soup.find_all(
                "a", href=lambda href: href and "/watch?v=" in href
            )

            if args.outfile:
                with open(args.outfile, "w", encoding="utf-8") as out:
                    for link in youtube_links:
                        out.write(f"- [{link.string}]({link['href']})\n")
            else:
                for link in youtube_links:
                    print(f"- [{link.string}]({link['href']})")
    except FileNotFoundError:
        print(f"File {args.infile} not found")
        sys.exit(1)


if __name__ == "__main__":
    main()

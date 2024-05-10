#!/usr/bin/env python

import argparse
from datetime import datetime
import re

LOG_LEVEL = r"\[.+\]"
SCSENV_HOST = r"[A-Za-z]+@[A-Z]{6}_[a-z]{6}[12]a"
TIMESTAMP = r"\d{1,2}\/\d{1,2}\/\d{2} \d{1,2}:\d{1,2}:\d{1,2}\.\d{3}"
JUNK1 = r"<\d+/\d+>"
SRCFILE = r".+:\d+"
MESSAGE = r".+"

TRACE_PATTERN1 = r"^%s %s (?P<timestamp>%s) %s \((?P<srcfile>%s)\) (?P<message>%s)" % (
    LOG_LEVEL,
    SCSENV_HOST,
    TIMESTAMP,
    JUNK1,
    SRCFILE,
    MESSAGE,
)
TRACE_PATTERN2 = r"^%s %s (?P<timestamp>%s) \(%s\) %s \((?P<srcfile>%s)\)" % (
    LOG_LEVEL,
    SCSENV_HOST,
    TIMESTAMP,
    TIMESTAMP,
    JUNK1,
    SRCFILE,
)
TRACE_PATTERN3 = r"^(?P<message>%s)" % (MESSAGE)

CAR = r"Car[#N]?:?\W"


def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(description="tmc_foobar")
    parser.add_argument(
        "--log", "-l", required=True, nargs="*", dest="logfiles", help="tmc_log file"
    )
    parser.add_argument(
        "--output", "-o", required=False, dest="output", help="output file"
    )
    args = parser.parse_args()

    events = []
    timestamp = ""
    srcfile = ""
    message = ""

    for logfile in args.logfiles:
        with open(logfile, "r", encoding="utf-8") as infile:
            count = 0
            for line in infile:
                line = line.strip()
                count += 1
                match = re.match(TRACE_PATTERN1, line)
                if match:
                    timestamp = datetime.strptime(
                        match.group("timestamp"), "%m/%d/%y %H:%M:%S.%f"
                    )
                    srcfile = match.group("srcfile")
                    message = match.group("message")
                else:
                    match = re.match(TRACE_PATTERN2, line)
                    if match:
                        timestamp = datetime.strptime(
                            match.group("timestamp"), "%m/%d/%y %H:%M:%S.%f"
                        )
                        srcfile = match.group("srcfile")
                        message = ""
                    else:
                        match = re.match(TRACE_PATTERN3, line)
                        if match:
                            message = match.group("message")
                        else:
                            print(f"{logfile} at line {count}:")
                            print(f"          {line}")

                match = re.search(CAR, line)
                if match:
                    events.append(
                        {"timestamp": timestamp, "srcfile": srcfile, "message": message}
                    )

    if events:
        try:
            events.sort(key=lambda x: x["timestamp"])
            if args.output:
                with open(args.output, "w", encoding="utf-8") as outfile:
                    for event in events:
                        outfile.write(
                            f"{event['timestamp']}|{event['srcfile']}|{event['message']}\n"
                        )
                print(f"{len(events)} line(s) written to {args.output}.")
            else:
                for event in events:
                    print(f"{event['timestamp']}|{event['message']}")
        except TypeError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

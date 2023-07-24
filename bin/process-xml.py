#!/usr/bin/env python

import argparse
import logging
import logging.handlers
import xml.etree.ElementTree as ET


def init_logging():
    """
    Initialize logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    c = logging.StreamHandler()
    c_formatter = logging.Formatter(fmt="%(message)s")
    c.setFormatter(c_formatter)
    c.setLevel(logging.INFO)

    f = logging.FileHandler("process-xml.log")
    f_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s")
    f.setFormatter(f_formatter)
    f.setLevel(logging.DEBUG)

    logger.addHandler(c)
    logger.addHandler(f)
    return logger


def ignore_name(name):
    """
    Returns True when a given name is a member of (ignored) keywords
    """
    keywords = ["dac", "dal", "dco", "dco", "dfo", "sac", "sfo"]
    return name in keywords


def write_ssr_file(environ, system, points):
    """
    write ssr file
    """
    datfile = f"{environ.upper()}-{system.upper()}.dat"

    with open(datfile, "w") as outfile:
        # We still need a header
        outfile.write("ENVIRONMENT=\n")
        outfile.write("CONFIGURATION=\n")
        for p in points:
            outfile.write(f"POINT=<alias>{p}\n")


def main():
    """
    Main function
    """
    init_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        dest="input",
        help="path to instancesHierarchy.xml file",
    )
    parser.add_argument(
        "--environment",
        "-e",
        required=True,
        dest="environ",
        help="environment (e.g., HBF)",
    )
    parser.add_argument(
        "--system", "-s", required=True, dest="system", help="system (e.g., BMF)"
    )

    args = parser.parse_args()
    logging.debug(f"args: {args}")

    root = ET.parse(args.input)

    # Use XPath to find nodes under 'BNK'
    # tag = f".//HierarchyItem[@name='{args.environ}']//HiearchyItem"
    result = root.findall(
        f".//HierarchyItem[@name='{args.environ}']//HierarchyItem[@name='{args.system}']//HierarchyItem"
    )

    points = []
    prefix = ""

    for item in result:
        alias = item.get("alias")
        name = item.get("name")

        # alias: BNK_ACMA_0001 == {args.system}_ACMA_0001
        if alias == f"{args.environ}_{name}":
            prefix = alias
            continue

        if not ignore_name(name):
            if prefix != "":
                logging.info(f"POINT=<alias>{prefix}:{name}")
                points.append(f"{prefix}:{name}")
            else:
                logging.info(f"Alias: {alias}, Name: {name}")

    logging.info(f"No. of points discovered: {len(points)}")
    write_ssr_file(args.environ, args.system, points)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import argparse
import logging
import logging.handlers
import os.path
import sys
import xml.etree.ElementTree as ET

ENVIRON_LIST = [
    "BGK",
    "BNK",
    "CNT",
    "CQY",
    "DBG",
    "FRP",
    "HBF",
    "HGN",
    "KVN",
    "LTI",
    "NED",
    "ATS",
    "CMS",
    "ECS",
    "OTP",
    "PGC",
    "PGL",
    "PTP",
    "SER",
    "SKG",
    "WLH",
]


SWC_MAPPING = {
    "BMF": {"node": "BMF", "filename": "BMF"},
    "DNG": {"node": "DNG__0001", "filename": "DNG"},
    "ECS": {"node": "ECS", "filename": "ECS"},
    "FPS": {"node": "FPS__0001", "filename": "FPS"},
}

IGNORE_LIST = [
    "aac",
    "aal",
    "afo",
    "aio",
    "dac",
    "dal",
    "dco",
    "dfo",
    "dio",
    "dov",
    "sac",
    "sfo",
    "sio",
    "usr",
]


def init_logging():
    """
    Initialize logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    cons = logging.StreamHandler()
    cons_formatter = logging.Formatter(fmt="%(message)s")
    cons.setFormatter(cons_formatter)
    cons.setLevel(logging.INFO)

    logger.addHandler(cons)
    return logger


def validate_environment(environ):
    """
    Returns True if a given environ is a member of environment list
    """
    return environ in ENVIRON_LIST


def validate_swc(swc):
    """
    Returns True if a given environment is a member of SWC mapping list
    """
    return swc in SWC_MAPPING


def get_swc_node(swc):
    """
    Returns a node text to search for
    """
    data = SWC_MAPPING.get(swc)
    return data.get("node")


def validate_output_dir(output_dir):
    """
    Returns True when output_dir exists
    """
    return os.path.isdir(output_dir)


def ignore_name(name):
    """
    Returns True when a given name is a member of ignore_list
    """
    for word in IGNORE_LIST:
        match = name.startswith(word)
        if match:
            return True
    return False


def get_swc_outfile(environ, swc, output_dir):
    """
    Returns an output filename, given an environment and a SWC (e.g., BNK-BMF.dat)
    """
    data = SWC_MAPPING.get(swc)
    return f"{output_dir}/{environ}-{data.get('filename')}.dat"


def write_ssr(environ, points, filename):
    """
    Writes SSR for GWS
    """
    logging.info(f"Writing database points to {filename} ...")
    with open(filename, "w") as outfile:
        # SSR file still needs comments at the top of the file
        # ENVIRONEMENT needs six-letter environment name (e.g., BNKSMS)
        outfile.write(f"ENVIRONEMENT={environ}\n")
        outfile.write("CONFIGURATION=\n")

        for p in points:
            logging.debug(f"POINT=<alias>{p}")
            outfile.write(f"POINT=<alias>{p}\n")
        logging.info(f"No. of database points written to {filename}: {len(points)}")


def main():
    """
    Main function
    """
    init_logging()

    parser = argparse.ArgumentParser(prog="generate-ssr.py")
    parser.add_argument(
        "--xml",
        "-x",
        required=True,
        dest="xmlFile",
        help="path to instancesHierarchy.xml",
    )
    parser.add_argument(
        "--environ",
        "-e",
        required=True,
        dest="environ",
        help=f"valid environment is one of {ENVIRON_LIST}",
    )
    parser.add_argument(
        "--swc",
        "-w",
        required=True,
        dest="swc",
        help="SWC",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        dest="output_dir",
        help="path to output directory of SSR file",
    )

    args = parser.parse_args()
    logging.debug(f"args: {args}")

    swc = "BMF"

    if not validate_environment(args.environ):
        logging.error(f"Invalid environment, {args.environ}.")
        logging.error(f"Valid environment is one of {ENVIRON_LIST}.")
        sys.exit(1)

    if not validate_swc(args.swc):
        logging.error(f"Invalid SWC, {args.swc}.")
        sys.exit(1)

    if not validate_output_dir(args.output_dir):
        logging.error(f"{args.output_dir} does not exist.")
        sys.exit(1)

    nodeName = get_swc_node(args.swc)
    outfile = get_swc_outfile(args.environ, args.swc, args.output_dir)

    root = ET.parse(args.xmlFile)

    prefix = ""
    points = []

    result = root.findall(
        f".//HierarchyItem[@name='{args.environ}']//HierarchyItem[@name='{nodeName}']//HierarchyItem"
    )

    for item in result:
        alias = item.get("alias")
        name = item.get("name")

        if alias == f"{args.environ}_{name}":
            prefix = alias
            continue

        if not ignore_name(name):
            if prefix != "":
                points.append(f"{prefix}:{name}")
            else:
                logging.debug(f"Alias: {alias}, Name: {name}")
                logging.debug(f"Length: {len(item)}")

    if len(points) > 0:
        sorted_points = sorted(points)

        logging.info(
            f"No. of discovered points for {args.environ}:{nodeName}: {len(sorted_points)}"
        )
        write_ssr(args.environ, sorted_points, outfile)
    else:
        logging.error(
            f"No database points were discovered for {args.environ}:{nodeName}"
        )


if __name__ == "__main__":
    main()

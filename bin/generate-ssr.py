#!/usr/bin/env python

import argparse
import locale
from functools import cmp_to_key
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
    "CCTV": {"node": "CCTS_0001", "filename": "COM-CCTV"},
    "PAS": {"node": "PASS_0001", "filename": "COM-PAS"},
    "PIS": {"node": "PISS_0001", "filename": "COM-PIS"},
    "DNG": {"node": "DNG__0001", "filename": "DNG"},
    "ECS": {"node": "ECS", "filename": "ECS"},
    "FPS": {"node": "FPS__0001", "filename": "FPS"},
    "LNE": {"node": "LNE__0001", "filename": "LNE"},
    "DC": {"node": "DC___0001", "filename": "POW-DC"},
    "ETSB": {"node": "ETSB_0001", "filename": "POW-ETSB"},
    "HV": {"node": "HV___0001", "filename": "POW-HV"},
    "LIG": {"node": "LIG__0001", "filename": "POW-LIG"},
    "LV": {"node": "LV___0001", "filename": "POW-LV"},
    # TODO At terminus station, node is TRAT instead of TRAS
    "SIG": {"node": "TRAS", "filename": "SIG"},
}

IGNORE_LIST = [
    "aac",
    "aal",
    "aco",
    "afo",
    "aio",
    "dac",
    "dal",
    "dco",
    "dfo",
    "dio",
    "dov",
    "sac",
    "sco",
    "sfo",
    "sii",
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
    if len(name) < 3:
        return True
    return name[0:3] in IGNORE_LIST


def get_swc_outfile(environ, swc, output_dir):
    """
    Returns an output filename, given an environment and a SWC (e.g., BNK-BMF.dat)
    """
    data = SWC_MAPPING.get(swc)
    return f"{output_dir}/{environ}-{data.get('filename')}.dat"


def set_environment_name(environ):
    """
    Corrects the given three-letter environment name to six-letter environment name (e.g., BGK -> BGKSMS)
    """
    stations = [
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
        "OTP",
        "PGC",
        "PGL",
        "PTP",
        "SER",
        "SKG",
        "WLH",
    ]

    occ = [
        "ATS",
        "CMS",
        "ECS",
    ]

    if environ in stations:
        return f"{environ}SMS"
    if environ in occ:
        return f"OCC{environ}"


def write_ssr(environ, points, filename):
    """
    Writes SSR for GWS
    """
    logging.info(f"Writing database points to {filename} ...")
    with open(filename, "w") as outfile:
        # SSR file still needs comments at the top of the file
        # ENVIRONEMENT needs six-letter environment name (e.g., BNKSMS)
        environ = set_environment_name(environ)
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
    # parser.add_argument(
    #     "--swc",
    #     "-w",
    #     required=True,
    #     dest="swc",
    #     help="SWC",
    # )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        dest="output_dir",
        help="path to output directory of SSR file",
    )

    args = parser.parse_args()
    logging.debug(f"args: {args}")

    if not validate_environment(args.environ):
        logging.error(f"Invalid environment, {args.environ}.")
        logging.error(f"Valid environment is one of {ENVIRON_LIST}.")
        sys.exit(1)

    # if not validate_swc(args.swc):
    #     logging.error(f"Invalid SWC, {args.swc}.")
    #     sys.exit(1)

    if not validate_output_dir(args.output_dir):
        logging.error(f"{args.output_dir} does not exist.")
        sys.exit(1)

    root = ET.parse(args.xmlFile)

    for swc in SWC_MAPPING.keys():
        logging.info(f"SWC: {swc}")

        nodeName = get_swc_node(swc)
        outfile = get_swc_outfile(args.environ, swc, args.output_dir)

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
                parent = root.findall(f".//HierarchyItem[@alias='{alias}']/..")
                if len(parent) == 1:
                    prefix = parent[0].get("alias")
                    points.append(f"{prefix}:{name}")
                else:
                    logging.warn(f"Unexpected number of parents for alias {alias}")

        if len(points) > 0:
            # To match the sorting behavior with `sort` in shell
            locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))
            points.sort(key=cmp_to_key(locale.strcoll))

            logging.info(
                f"No. of discovered points for {args.environ}:{nodeName}: {len(points)}"
            )
            write_ssr(args.environ, points, outfile)
        else:
            logging.error(
                f"No database points were discovered for {args.environ}:{nodeName}"
            )


if __name__ == "__main__":
    main()

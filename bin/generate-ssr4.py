#!/usr/bin/env python

import argparse
import locale
import logging
import logging.handlers
import multiprocessing
import os
import os.path
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from functools import cmp_to_key

databases = [
    {
        # BGK-BMF.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to BGK-BMF.dat file
        "location": "BGK",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-BMF.dat to be written to this directory
        "output": "BGK-BMF",
    },
    {
        # BGK-COM-CCTV.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "BGKSMS",  # data written to BGK-COM-CCTV.dat file
        "location": "BGK",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-COM-CCTV.dat to be written to this directory
        "output": "BGK-COM-CCTV",
    },
    {
        # BGK-COM-PAS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "BGKSMS",  # data written to BGK-COM-PAS.dat file
        "location": "BGK",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-COM-PAS.dat to be written to this directory
        "output": "BGK-COM-PAS",
    },
    {
        # BGK-COM-PIS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "BGKSMS",  # data written to BGK-COM-PIS.dat file
        "location": "BGK",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-COM-PIS.dat to be written to this directory
        "output": "BGK-COM-PIS",
    },
    #
    {
        # BNK-BMF.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to BNK-BMF.dat file
        "location": "BNK",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-BMF.dat to be written to this directory
        "output": "BNK-BMF",
    },
    {
        # BNK-COM-CCTV.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "BNKSMS",  # data written to BNK-COM-CCTV.dat file
        "location": "BNK",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-COM-CCTV.dat to be written to this directory
        "output": "BNK-COM-CCTV",
    },
    {
        # BNK-COM-PAS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "BNKSMS",  # data written to BNK-COM-PAS.dat file
        "location": "BNK",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-COM-PAS.dat to be written to this directory
        "output": "BNK-COM-PAS",
    },
    {
        # BNK-COM-PIS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "BNKSMS",  # data written to BNK-COM-PIS.dat file
        "location": "BNK",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-COM-PIS.dat to be written to this directory
        "output": "BNK-COM-PIS",
    },
    #
    {
        # CNT-BMF.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to CNT-BMF.dat file
        "location": "CNT",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-BMF.dat to be written to this directory
        "output": "CNT-BMF",
    },
    {
        # CNT-COM-CCTV.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "CNTSMS",  # data written to CNT-COM-CCTV.dat file
        "location": "CNT",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-COM-CCTV.dat to be written to this directory
        "output": "CNT-COM-CCTV",
    },
    {
        # CNT-COM-PAS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "CNTSMS",  # data written to CNT-COM-PAS.dat file
        "location": "CNT",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-COM-PAS.dat to be written to this directory
        "output": "CNT-COM-PAS",
    },
    {
        # CNT-COM-PIS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "CNTSMS",  # data written to CNT-COM-PIS.dat file
        "location": "CNT",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-COM-PIS.dat to be written to this directory
        "output": "CNT-COM-PIS",
    },
    #
    {
        # CQY-BMF.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to CQY-BMF.dat file
        "location": "CQY",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-BMF.dat to be written to this directory
        "output": "CQY-BMF",
    },
    {
        # CQY-COM-CCTV.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "CQYSMS",  # data written to CQY-COM-CCTV.dat file
        "location": "CQY",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-COM-CCTV.dat to be written to this directory
        "output": "CQY-COM-CCTV",
    },
    {
        # CQY-COM-PAS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "CQYSMS",  # data written to CQY-COM-PAS.dat file
        "location": "CQY",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-COM-PAS.dat to be written to this directory
        "output": "CQY-COM-PAS",
    },
    {
        # CQY-COM-PIS.dat file from OCCCMS database
        "source": "CMS",  # xml_DB_CMS
        "environ": "CQYSMS",  # data written to CQY-COM-PIS.dat file
        "location": "CQY",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-COM-PIS.dat to be written to this directory
        "output": "CQY-COM-PIS",
    },
]


def init_logger():
    """
    Initialize logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    c = logging.StreamHandler()
    c_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s")
    c.setFormatter(c_formatter)
    c.setLevel(logging.DEBUG)

    f = logging.FileHandler("generate-ssr4.log")
    f_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s")
    f.setFormatter(f_formatter)
    f.setLevel(logging.DEBUG)

    logger.addHandler(c)
    logger.addHandler(f)
    return logger


def is_valid_dir(dir_name):
    """
    Returns True when dir_name is a valid directory
    """
    return os.path.isdir(dir_name)


def is_input_point(name):
    """
    Returns True when a given name is input point
    """
    if len(name) >= 3:
        # Ignore structured input (sii)
        return name[0:3] in ["aii", "dii"]
    return False


def write_ssr_file(db_points, environ, ssr_dat):
    """
    Write SSR file from given database points
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    header = f"""###########################################################
#  /home/dbs/SumReport/{environ}/{os.path.basename(ssr_dat)}                 #
#  Status Summary Report configuration file               #
#  generated automatically on {timestamp}         #
#                                                         #
###########################################################"""

    with open(ssr_dat, "w") as outfile:
        outfile.write(f"{header}\n")
        outfile.write(f"ENVIRONEMENT={environ}\n")
        outfile.write("CONFIGURATION=\n")

        for point in db_points:
            outfile.write(f"POINT=<alias>{point}\n")

    logging.info(f"{len(db_points)} points written to {ssr_dat}")


def do_work(xml_dir, dir_name, db):
    """
    Performs work to create a SSR file from database data
    """
    db_points = []

    # temporary variables
    source = db.get("source")  # xml_DB_XXX
    location = db.get("location")  # BGK, BNK, ..., NDI, NPS, etc
    system = db.get("system")  # BMF, CCTS_0001, ..., SIG, etc

    start_work = time.perf_counter()
    logging.info(f"Processing {location}:{system} in {source} database ...")

    xml_file = f"{xml_dir}/xml_DB_{source}/instancesHierarchy.xml"
    logging.info(f"Parsing {xml_file} ...")
    root = ET.parse(xml_file)

    results = root.findall(
        f".//HierarchyItem[@name='{location}']//HierarchyItem[@name='{system}']//HierarchyItem"
    )
    for item in results:
        alias = item.get("alias")
        name = item.get("name")

        if alias == f"{location}_{name}":
            continue
        if not is_input_point(name):
            continue

        parent = root.findall(f".//HierarchyItem[@alias='{alias}']/..")
        if len(parent) != 1:
            logging.warning(f"Unexpected number of parents ({len(parent)}) for {alias}")
            continue

        prefix = parent[0].get("alias")
        point = f"{prefix}:{name}"
        db_points.append(point)

    if len(db_points) > 0:
        db_points.sort(key=cmp_to_key(locale.strcoll))
        output_dir = f"{dir_name}/{db.get('output_dir')}"
        if not is_valid_dir(output_dir):
            try:
                logging.info(f"Creating directory: {output_dir}")
                os.mkdir(output_dir)
            except OSError:
                logging.error(f"Creation of the directory {output_dir} failed")
        ssr_dat = f"{output_dir}/{db.get('output')}.dat"
        environ = db.get("environ")
        write_ssr_file(db_points, environ, ssr_dat)

    end_work = time.perf_counter()
    logging.info(
        f"Processing {location}:{system} in {source} database ... DONE ({end_work - start_work:0.4f}s)"
    )


def main():
    """
    main function
    """
    init_logger()

    parser = argparse.ArgumentParser(prog="generate-ssr4")
    parser.add_argument(
        "--xml-dir",
        "-x",
        required=True,
        dest="xml_dir",
        help="path to XML directories",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        dest="output_dir",
        help="path to output directory",
    )
    parser.add_argument(
        "--pool",
        "-p",
        required=False,
        type=int,
        default=1,
        dest="pool",
        help="Number of worker processes to be used",
    )

    args = parser.parse_args()
    # logging.debug(f"args: {args}")

    if not is_valid_dir(args.xml_dir):
        logging.error(f"{args.xml_dir} is not a valid directory")
        return

    if not is_valid_dir(args.output_dir):
        logging.error(f"{args.output_dir} is not a valid directory")
        try:
            os.mkdir(args.output_dir)
        except OSError:
            logging.error(f"Creation of the directory {args.output_dir} failed")
            return

    start = time.perf_counter()

    pool = multiprocessing.Pool(args.pool)
    for db in databases:
        pool.apply_async(do_work, [args.xml_dir, args.output_dir, db])
    pool.close()
    pool.join()

    # for db in databases:
    #     db_points = []

    #     source = db.get("source")  # xml_DB_XXX
    #     location = db.get("location")  # e.g., BGK, BNK, NDI, NPS, NTS, etc
    #     system = db.get("system")  # BMF, CCTS_0001, ..., SIG, etc

    #     start_db = time.perf_counter()
    #     logging.info(f"Processing {location}:{system} in {source} database ...")

    #     # Create a path to xml_DB_XXX/instancesHierarchy.xml
    #     xml_file = f"{args.xml_dir}/xml_DB_{source}/instancesHierarchy.xml"
    #     logging.info(f"Parsing {xml_file} ...")
    #     root = ET.parse(xml_file)

    #     results = root.findall(
    #         f".//HierarchyItem[@name='{location}']//HierarchyItem[@name='{system}']//HierarchyItem"
    #     )
    #     # logging.debug(f"No. of results: {len(results)}")

    #     for item in results:
    #         alias = item.get("alias")
    #         name = item.get("name")

    #         if alias == f"{location}_{name}":
    #             continue
    #         if not is_input_point(name):
    #             continue

    #         parent = root.findall(f".//HierarchyItem[@alias='{alias}']/..")
    #         if len(parent) != 1:
    #             logging.warning(
    #                 f"Unexpected number of parents ({len(parent)}) for {alias}"
    #             )
    #             continue

    #         prefix = parent[0].get("alias")
    #         point = f"{prefix}:{name}"
    #         db_points.append(point)

    #     if len(db_points) > 0:
    #         db_points.sort(key=cmp_to_key(locale.strcoll))
    #         output_dir = f"{args.output_dir}/{db.get('output_dir')}"
    #         if not is_valid_dir(output_dir):
    #             try:
    #                 logging.info(f"Creating directory: {output_dir}")
    #                 os.mkdir(output_dir)
    #             except OSError:
    #                 logging.error(f"Creation of the directory {output_dir} failed")

    #         ssr_dat = f"{output_dir}/{db.get('output')}.dat"
    #         environ = db.get("environ")
    #         write_ssr_file(db_points, environ, ssr_dat)

    #     end_db = time.perf_counter()
    #     logging.info(
    #         f"Processing {location}:{system} in {source} database ... DONE ({end_db - start_db:0.4f}s)"
    #     )

    end = time.perf_counter()
    logging.info(f"Total processing time: {end - start:0.4f} seconds")


if __name__ == "__main__":
    main()

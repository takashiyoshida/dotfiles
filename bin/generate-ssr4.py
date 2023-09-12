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
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to BGK-BMF.dat file
        "location": "BGK",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-BMF.dat to be written to this directorybin/generate-ssr4.py
        "output": "BGK-BMF",
    },
    {
        # BGK-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "BGKSMS",  # data written to BGK-COM-CCTV.dat file
        "location": "BGK",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-COM-CCTV.dat to be written to this directory
        "output": "BGK-COM-CCTV",
    },
    {
        # BGK-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "BGKSMS",  # data written to BGK-COM-PAS.dat file
        "location": "BGK",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-COM-PAS.dat to be written to this directory
        "output": "BGK-COM-PAS",
    },
    {
        # BGK-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "BGKSMS",  # data written to BGK-COM-PIS.dat file
        "location": "BGK",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-COM-PIS.dat to be written to this directory
        "output": "BGK-COM-PIS",
    },
    #
    {
        # BNK-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to BNK-BMF.dat file
        "location": "BNK",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-BMF.dat to be written to this directory
        "output": "BNK-BMF",
    },
    {
        # BNK-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "BNKSMS",  # data written to BNK-COM-CCTV.dat file
        "location": "BNK",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-COM-CCTV.dat to be written to this directory
        "output": "BNK-COM-CCTV",
    },
    {
        # BNK-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "BNKSMS",  # data written to BNK-COM-PAS.dat file
        "location": "BNK",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-COM-PAS.dat to be written to this directory
        "output": "BNK-COM-PAS",
    },
    {
        # BNK-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "BNKSMS",  # data written to BNK-COM-PIS.dat file
        "location": "BNK",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # BNK-COM-PIS.dat to be written to this directory
        "output": "BNK-COM-PIS",
    },
    #
    {
        # CNT-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to CNT-BMF.dat file
        "location": "CNT",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-BMF.dat to be written to this directory
        "output": "CNT-BMF",
    },
    {
        # CNT-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "CNTSMS",  # data written to CNT-COM-CCTV.dat file
        "location": "CNT",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-COM-CCTV.dat to be written to this directory
        "output": "CNT-COM-CCTV",
    },
    {
        # CNT-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "CNTSMS",  # data written to CNT-COM-PAS.dat file
        "location": "CNT",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-COM-PAS.dat to be written to this directory
        "output": "CNT-COM-PAS",
    },
    {
        # CNT-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "CNTSMS",  # data written to CNT-COM-PIS.dat file
        "location": "CNT",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CNT-COM-PIS.dat to be written to this directory
        "output": "CNT-COM-PIS",
    },
    #
    {
        # CQY-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to CQY-BMF.dat file
        "location": "CQY",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-BMF.dat to be written to this directory
        "output": "CQY-BMF",
    },
    {
        # CQY-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "CQYSMS",  # data written to CQY-COM-CCTV.dat file
        "location": "CQY",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-COM-CCTV.dat to be written to this directory
        "output": "CQY-COM-CCTV",
    },
    {
        # CQY-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "CQYSMS",  # data written to CQY-COM-PAS.dat file
        "location": "CQY",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-COM-PAS.dat to be written to this directory
        "output": "CQY-COM-PAS",
    },
    {
        # CQY-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "CQYSMS",  # data written to CQY-COM-PIS.dat file
        "location": "CQY",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # CQY-COM-PIS.dat to be written to this directory
        "output": "CQY-COM-PIS",
    },
    #
    {
        # DBG-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to DBG-BMF.dat file
        "location": "DBG",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # DBG-BMF.dat to be written to this directory
        "output": "DBG-BMF",
    },
    {
        # DBG-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "DBGSMS",  # data written to DBG-COM-CCTV.dat file
        "location": "DBG",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # DBG-COM-CCTV.dat to be written to this directory
        "output": "DBG-COM-CCTV",
    },
    {
        # DBG-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "DBGSMS",  # data written to DBG-COM-PAS.dat file
        "location": "DBG",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # DBG-COM-PAS.dat to be written to this directory
        "output": "DBG-COM-PAS",
    },
    {
        # DBG-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "DBGSMS",  # data written to DBG-COM-PIS.dat file
        "location": "DBG",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # DBG-COM-PIS.dat to be written to this directory
        "output": "DBG-COM-PIS",
    },
    #
    {
        # FRP-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to FRP-BMF.dat file
        "location": "FRP",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # FRP-BMF.dat to be written to this directory
        "output": "FRP-BMF",
    },
    {
        # FRP-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "FRPSMS",  # data written to FRP-COM-CCTV.dat file
        "location": "FRP",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # FRP-COM-CCTV.dat to be written to this directory
        "output": "FRP-COM-CCTV",
    },
    {
        # FRP-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "FRPSMS",  # data written to FRP-COM-PAS.dat file
        "location": "FRP",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # FRP-COM-PAS.dat to be written to this directory
        "output": "FRP-COM-PAS",
    },
    {
        # FRP-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "FRPSMS",  # data written to FRP-COM-PIS.dat file
        "location": "FRP",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # FRP-COM-PIS.dat to be written to this directory
        "output": "FRP-COM-PIS",
    },
    #
    {
        # HBF-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to HBF-BMF.dat file
        "location": "HBF",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # HBF-BMF.dat to be written to this directory
        "output": "HBF-BMF",
    },
    {
        # HBF-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "HBFSMS",  # data written to HBF-COM-CCTV.dat file
        "location": "HBF",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # HBF-COM-CCTV.dat to be written to this directory
        "output": "HBF-COM-CCTV",
    },
    {
        # HBF-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "HBFSMS",  # data written to HBF-COM-PAS.dat file
        "location": "HBF",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # HBF-COM-PAS.dat to be written to this directory
        "output": "HBF-COM-PAS",
    },
    {
        # HBF-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "HBFSMS",  # data written to HBF-COM-PIS.dat file
        "location": "HBF",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # HBF-COM-PIS.dat to be written to this directory
        "output": "HBF-COM-PIS",
    },
    #
    {
        # HGN-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to HGN-BMF.dat file
        "location": "HGN",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # HGN-BMF.dat to be written to this directory
        "output": "HGN-BMF",
    },
    {
        # HGN-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "HGNSMS",  # data written to HGN-COM-CCTV.dat file
        "location": "HGN",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # HGN-COM-CCTV.dat to be written to this directory
        "output": "HGN-COM-CCTV",
    },
    {
        # HGN-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "HGNSMS",  # data written to HGN-COM-PAS.dat file
        "location": "HGN",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # HGN-COM-PAS.dat to be written to this directory
        "output": "HGN-COM-PAS",
    },
    {
        # HGN-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "HGNSMS",  # data written to HGN-COM-PIS.dat file
        "location": "HGN",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # HGN-COM-PIS.dat to be written to this directory
        "output": "HGN-COM-PIS",
    },
    #
    {
        # KVN-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to KVN-BMF.dat file
        "location": "KVN",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # KVN-BMF.dat to be written to this directory
        "output": "KVN-BMF",
    },
    {
        # KVN-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "KVNSMS",  # data written to KVN-COM-CCTV.dat file
        "location": "KVN",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # KVN-COM-CCTV.dat to be written to this directory
        "output": "KVN-COM-CCTV",
    },
    {
        # KVN-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "KVNSMS",  # data written to KVN-COM-PAS.dat file
        "location": "KVN",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # KVN-COM-PAS.dat to be written to this directory
        "output": "KVN-COM-PAS",
    },
    {
        # KVN-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "KVNSMS",  # data written to KVN-COM-PIS.dat file
        "location": "KVN",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # KVN-COM-PIS.dat to be written to this directory
        "output": "KVN-COM-PIS",
    },
    #
    {
        # LTI-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to LTI-BMF.dat file
        "location": "LTI",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # LTI-BMF.dat to be written to this directory
        "output": "LTI-BMF",
    },
    {
        # LTI-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "LTISMS",  # data written to LTI-COM-CCTV.dat file
        "location": "LTI",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # LTI-COM-CCTV.dat to be written to this directory
        "output": "LTI-COM-CCTV",
    },
    {
        # LTI-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "LTISMS",  # data written to LTI-COM-PAS.dat file
        "location": "LTI",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # LTI-COM-PAS.dat to be written to this directory
        "output": "LTI-COM-PAS",
    },
    {
        # LTI-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "LTISMS",  # data written to LTI-COM-PIS.dat file
        "location": "LTI",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # LTI-COM-PIS.dat to be written to this directory
        "output": "LTI-COM-PIS",
    },
    #
    {
        # OTP-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to OTP-BMF.dat file
        "location": "OTP",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # OTP-BMF.dat to be written to this directory
        "output": "OTP-BMF",
    },
    {
        # OTP-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OTPSMS",  # data written to OTP-COM-CCTV.dat file
        "location": "OTP",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # OTP-COM-CCTV.dat to be written to this directory
        "output": "OTP-COM-CCTV",
    },
    {
        # OTP-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OTPSMS",  # data written to OTP-COM-PAS.dat file
        "location": "OTP",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # OTP-COM-PAS.dat to be written to this directory
        "output": "OTP-COM-PAS",
    },
    {
        # OTP-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OTPSMS",  # data written to OTP-COM-PIS.dat file
        "location": "OTP",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # OTP-COM-PIS.dat to be written to this directory
        "output": "OTP-COM-PIS",
    },
    #
    {
        # PGC-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to PGC-BMF.dat file
        "location": "PGC",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGC-BMF.dat to be written to this directory
        "output": "PGC-BMF",
    },
    {
        # PGC-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PGCSMS",  # data written to PGC-COM-CCTV.dat file
        "location": "PGC",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGC-COM-CCTV.dat to be written to this directory
        "output": "PGC-COM-CCTV",
    },
    {
        # PGC-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PGCSMS",  # data written to PGC-COM-PAS.dat file
        "location": "PGC",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGC-COM-PAS.dat to be written to this directory
        "output": "PGC-COM-PAS",
    },
    {
        # PGC-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PGCSMS",  # data written to PGC-COM-PIS.dat file
        "location": "PGC",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGC-COM-PIS.dat to be written to this directory
        "output": "PGC-COM-PIS",
    },
    #
    {
        # PGL-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to PGL-BMF.dat file
        "location": "PGL",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGL-BMF.dat to be written to this directory
        "output": "PGL-BMF",
    },
    {
        # PGL-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PGLSMS",  # data written to PGL-COM-CCTV.dat file
        "location": "PGL",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGL-COM-CCTV.dat to be written to this directory
        "output": "PGL-COM-CCTV",
    },
    {
        # PGL-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PGLSMS",  # data written to PGL-COM-PAS.dat file
        "location": "PGL",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGL-COM-PAS.dat to be written to this directory
        "output": "PGL-COM-PAS",
    },
    {
        # PGL-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PGLSMS",  # data written to PGL-COM-PIS.dat file
        "location": "PGL",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PGL-COM-PIS.dat to be written to this directory
        "output": "PGL-COM-PIS",
    },
    #
    {
        # PTP-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to PTP-BMF.dat file
        "location": "PTP",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # PTP-BMF.dat to be written to this directory
        "output": "PTP-BMF",
    },
    {
        # PTP-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PTPSMS",  # data written to PTP-COM-CCTV.dat file
        "location": "PTP",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PTP-COM-CCTV.dat to be written to this directory
        "output": "PTP-COM-CCTV",
    },
    {
        # PTP-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PTPSMS",  # data written to PTP-COM-PAS.dat file
        "location": "PTP",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PTP-COM-PAS.dat to be written to this directory
        "output": "PTP-COM-PAS",
    },
    {
        # PTP-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "PTPSMS",  # data written to PTP-COM-PIS.dat file
        "location": "PTP",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # PTP-COM-PIS.dat to be written to this directory
        "output": "PTP-COM-PIS",
    },
    #
    {
        # SER-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to SER-BMF.dat file
        "location": "SER",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # SER-BMF.dat to be written to this directory
        "output": "SER-BMF",
    },
    {
        # SER-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "SERSMS",  # data written to SER-COM-CCTV.dat file
        "location": "SER",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # SER-COM-CCTV.dat to be written to this directory
        "output": "SER-COM-CCTV",
    },
    {
        # SER-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "SERSMS",  # data written to SER-COM-PAS.dat file
        "location": "SER",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # SER-COM-PAS.dat to be written to this directory
        "output": "SER-COM-PAS",
    },
    {
        # SER-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "SERSMS",  # data written to SER-COM-PIS.dat file
        "location": "SER",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # SER-COM-PIS.dat to be written to this directory
        "output": "SER-COM-PIS",
    },
    #
    {
        # SKG-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to SKG-BMF.dat file
        "location": "SKG",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # SKG-BMF.dat to be written to this directory
        "output": "SKG-BMF",
    },
    {
        # SKG-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "SKGSMS",  # data written to SKG-COM-CCTV.dat file
        "location": "SKG",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # SKG-COM-CCTV.dat to be written to this directory
        "output": "SKG-COM-CCTV",
    },
    {
        # SKG-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "SKGSMS",  # data written to SKG-COM-PAS.dat file
        "location": "SKG",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # SKG-COM-PAS.dat to be written to this directory
        "output": "SKG-COM-PAS",
    },
    {
        # SKG-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "SKGSMS",  # data written to SKG-COM-PIS.dat file
        "location": "SKG",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # SKG-COM-PIS.dat to be written to this directory
        "output": "SKG-COM-PIS",
    },
    #
    {
        # WLH-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to WLH-BMF.dat file
        "location": "WLH",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # WLH-BMF.dat to be written to this directory
        "output": "WLH-BMF",
    },
    {
        # WLH-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "WLHSMS",  # data written to WLH-COM-CCTV.dat file
        "location": "WLH",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # WLH-COM-CCTV.dat to be written to this directory
        "output": "WLH-COM-CCTV",
    },
    {
        # WLH-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "WLHSMS",  # data written to WLH-COM-PAS.dat file
        "location": "WLH",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # WLH-COM-PAS.dat to be written to this directory
        "output": "WLH-COM-PAS",
    },
    {
        # WLH-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "WLHSMS",  # data written to WLH-COM-PIS.dat file
        "location": "WLH",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # WLH-COM-PIS.dat to be written to this directory
        "output": "WLH-COM-PIS",
    },
    #
    {
        # NED-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to NED-BMF.dat file
        "location": "NED",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # NED-BMF.dat to be written to this directory
        "output": "NED-BMF",
    },
    {
        # NED-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to NED-COM-CCTV.dat file
        "location": "NED",
        "system": "CCTS_0001",  # search for CCTS_0001 in the xml file
        "output_dir": "occcms",  # NED-COM-CCTV.dat to be written to this directory
        "output": "NED-COM-CCTV",
    },
    {
        # NED-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "NEDSMS",  # data written to NED-COM-PAS.dat file
        "location": "NED",
        "system": "PASS_0001",  # search for PASS_0001 in the xml file
        "output_dir": "occcms",  # NED-COM-PAS.dat to be written to this directory
        "output": "NED-COM-PAS",
    },
    # NDI = North East Line Depot Intake Substation
    {
        # NDI-POW-DC.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "NEDSMS",  # data written to NDI-POW-DC.dat file
        "location": "NDI",
        "system": "DC___0001",  # search for DC____0001 in the xml file
        "output_dir": "occcms",  # NDI-POW-DC.dat to be written to this directory
        "output": "NDI-POW-DC",
    },
    {
        # NDI-POW-HV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "NEDSMS",  # data written to NDI-POW-HV.dat file
        "location": "NDI",
        "system": "HV___0001",  # search for HV____0001 in the xml file
        "output_dir": "occcms",  # NDI-POW-HV.dat to be written to this directory
        "output": "NDI-POW-HV",
    },
    # NPS: NEL Depot Paintshop Substation
    {
        # NPS-POW-HV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "NEDSMS",  # data written to NPS-POW-HV.dat file
        "location": "NPS",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "occcms",  # NPS-POW-HV.dat to be written to this directory
        "output": "NPS-POW-HV",
    },
    # NTS = North East Line Depot Traction Substation
    {
        # NTS-POW-DC.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "NEDSMS",  # data written to NTS-POW-DC.dat file
        "location": "NTS",
        "system": "DC___0001",  # search for DC____0001 in the xml file
        "output_dir": "occcms",  # NTS-POW-DC.dat to be written to this directory
        "output": "NTS-POW-DC",
    },
    {
        # NTS-POW-HV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "NEDSMS",  # data written to NTS-POW-HV.dat file
        "location": "NDI",
        "system": "HV___0001",  # search for HV____0001 in the xml file
        "output_dir": "occcms",  # NTS-POW-HV.dat to be written to this directory
        "output": "NTS-POW-HV",
    },
    #
    {
        # OCC-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to OCC-BMF.dat file
        "location": "OCC",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # OCC-BMF.dat to be written to this directory
        "output": "OCC-BMF",
    },
    {
        # OCC-COM-CCTV.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCSMS",  # data written to OCC-COM-CCTV.dat file
        "location": "OCC",
        "system": "CCTS_0001",  # search for CCTS_0001 in the xml file
        "output_dir": "occcms",  # OCC-COM-CCTV.dat to be written to this directory
        "output": "OCC-COM-CCTV",
    },
    {
        # OCC-COM-PAS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCSMS",  # data written to OCC-COM-PAS.dat file
        "location": "OCC",
        "system": "PASS_0001",  # search for PASS_0001 in the xml file
        "output_dir": "occcms",  # OCC-COM-PAS.dat to be written to this directory
        "output": "OCC-COM-PAS",
    },
    {
        # OCC-COM-PIS.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCSMS",  # data written to OCC-COM-PIS.dat file
        "location": "OCC",
        "system": "PISS_0001",  # search for PISS_0001 in the xml file
        "output_dir": "occcms",  # OCC-COM-PIS.dat to be written to this directory
        "output": "OCC-COM-PIS",
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
    database = db.get("database")  # xml_DB_XXX
    location = db.get("location")  # BGK, BNK, ..., NDI, NPS, etc
    system = db.get("system")  # BMF, CCTS_0001, ..., SIG, etc

    start_work = time.perf_counter()
    logging.info(f"Processing {location}:{system} in {database} database ...")

    xml_file = f"{xml_dir}/xml_DB_{database}/instancesHierarchy.xml"
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
        f"Processing {location}:{system} in {database} database ... DONE ({end_work - start_work:0.4f}s)"
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

    #     source = db.get("database")  # xml_DB_XXX
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

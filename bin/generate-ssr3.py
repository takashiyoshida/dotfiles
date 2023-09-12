#!/usr/bin/env python

import argparse
import locale
import logging
import logging.handlers
import os
import os.path
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from functools import cmp_to_key


_databases = {
    # This script uses the key to load instancesHierarchy.xml file from xml_DB_BGK directory
    "BGK": {
        # output for BGK database is written to 'bgksms' directory
        "output_dir": "bgksms",
        "environment": {
            # a dictionary with key as environment name and value as a list of sub-systems
            "BGK": [
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "BMF",
                    # output of this sub-system is written to `bgksms/BGK-BMF.dat`
                    "output": "BGK-BMF",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "CCTS_0001",
                    # output of this sub-system is written to 'bgksms/BGK-COM-CCTV.dat'
                    "output": "BGK-COM-CCTV",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "PASS_0001",
                    # output of this sub-system is written to 'bgksms/BGK-COM-PAS.dat'
                    "output": "BGK-COM-PAS",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "PISS_0001",
                    # output of this sub-system is written to 'bgksms/BGK-COM-PIS.dat'
                    "output": "BGK-COM-PIS",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "DNG__0001",
                    # output of this sub-system is written to 'bgksms/BGK-DNG.dat'
                    "output": "BGK-DNG",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "ECS",
                    # output of this sub-system is written to 'bgksms/BGK-ECS.dat'
                    "output": "BGK-ECS",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "FPS__0001",
                    # output of this sub-system is written to 'bgksms/BGK-FPS.dat'
                    "output": "BGK-FPS",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "LNE__0001",
                    # output of this sub-system is written to 'bgksms/BGK-LNE.dat'
                    "output": "BGK-LNE",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "DC___0001",
                    # output of this sub-system is written to 'bgksms/BGK-POW-DC.dat'
                    "output": "BGK-POW-DC",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "ETSB_0001",
                    # output of this sub-system is written to 'bgksms/BGK-POW-ETSB.dat'
                    "output": "BGK-POW-ETSB",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "HV___0001",
                    # output of this sub-system is written to 'bgksms/BGK-POW-HV.dat'
                    "output": "BGK-POW-HV",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "LIG__0001",
                    # output of this sub-system is written to 'bgksms/BGK-POW-LIG.dat'
                    "output": "BGK-POW-LIG",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "LV___0001",
                    # output of this sub-system is written to 'bgksms/BGK-POW-LV.dat'
                    "output": "BGK-POW-LV",
                },
                {
                    # name is written in the SSR file as ENVIRONEMENT; see write_ssr_file()
                    "name": "BGKSMS",
                    # search for this node within the database file, instancesHierarchy.xml
                    "input": "TRAS",
                    # output of this sub-system is written to 'bgksms/BGK-SIG.dat'
                    "output": "BGK-SIG",
                },
            ]
        },
    },
    "BNK": {
        "output_dir": "bnksms",
        "environment": {
            "BNK": [
                {
                    "name": "BNKSMS",
                    "input": "BMF",
                    "output": "BNK-BMF",
                },
                {
                    "name": "BNKSMS",
                    "input": "CCTS_0001",
                    "output": "BNK-COM-CCTV",
                },
                {
                    "name": "BNKSMS",
                    "input": "PASS_0001",
                    "output": "BNK-COM-PAS",
                },
                {
                    "name": "BNKSMS",
                    "input": "PISS_0001",
                    "output": "BNK-COM-PIS",
                },
                {
                    "name": "BNKSMS",
                    "input": "DNG__0001",
                    "output": "BNK-DNG",
                },
                {
                    "name": "BNKSMS",
                    "input": "ECS",
                    "output": "BNK-ECS",
                },
                {
                    "name": "BNKSMS",
                    "input": "FPS__0001",
                    "output": "BNK-FPS",
                },
                {
                    "name": "BNKSMS",
                    "input": "LNE__0001",
                    "output": "BNK-LNE",
                },
                {
                    "name": "BNKSMS",
                    "input": "DC___0001",
                    "output": "BNK-POW-DC",
                },
                {
                    "name": "BNKSMS",
                    "input": "ETSB_0001",
                    "output": "BNK-POW-ETSB",
                },
                {
                    "name": "BNKSMS",
                    "input": "HV___0001",
                    "output": "BNK-POW-HV",
                },
                {
                    "name": "BNKSMS",
                    "input": "LIG__0001",
                    "output": "BNK-POW-LIG",
                },
                {
                    "name": "BNKSMS",
                    "input": "LV___0001",
                    "output": "BNK-POW-LV",
                },
                {
                    "name": "BNKSMS",
                    "input": "TRAS",
                    "output": "BNK-SIG",
                },
            ]
        },
    },
    "CNT": {
        "output_dir": "cntsms",
        "environment": {
            "CNT": [
                {
                    "name": "CNT",
                    "input": "BMF",
                    "output": "CNT-BMF",
                },
                {
                    "name": "CNT",
                    "input": "CCTS_0001",
                    "output": "CNT-COM-CCTV",
                },
                {
                    "name": "CNT",
                    "input": "PASS_0001",
                    "output": "CNT-COM-PAS",
                },
                {
                    "name": "CNT",
                    "input": "PISS_0001",
                    "output": "CNT-COM-PIS",
                },
                {
                    "name": "CNT",
                    "input": "DNG__0001",
                    "output": "CNT-DNG",
                },
                {
                    "name": "CNT",
                    "input": "ECS",
                    "output": "CNT-ECS",
                },
                {
                    "name": "CNT",
                    "input": "FPS__0001",
                    "output": "CNT-FPS",
                },
                {
                    "name": "CNT",
                    "input": "LNE__0001",
                    "output": "CNT-LNE",
                },
                {
                    "name": "CNT",
                    "input": "DC___0001",
                    "output": "CNT-POW-DC",
                },
                {
                    "name": "CNT",
                    "input": "ETSB_0001",
                    "output": "CNT-POW-ETSB",
                },
                {
                    "name": "CNT",
                    "input": "HV___0001",
                    "output": "CNT-POW-HV",
                },
                {
                    "name": "CNT",
                    "input": "LIG__0001",
                    "output": "CNT-POW-LIG",
                },
                {
                    "name": "CNT",
                    "input": "LV___0001",
                    "output": "CNT-POW-LV",
                },
                {
                    "name": "CNT",
                    "input": "TRAS",
                    "output": "CNT-SIG",
                },
            ]
        },
    },
    "CQY": {
        "output_dir": "cqysms",
        "environment": {
            "CQY": [
                {
                    "name": "CQYSMS",
                    "input": "BMF",
                    "output": "CQY-BMF",
                },
                {
                    "name": "CQYSMS",
                    "input": "CCTS_0001",
                    "output": "CQY-COM-CCTV",
                },
                {
                    "name": "CQYSMS",
                    "input": "PASS_0001",
                    "output": "CQY-COM-PAS",
                },
                {
                    "name": "CQYSMS",
                    "input": "PISS_0001",
                    "output": "CQY-COM-PIS",
                },
                {
                    "name": "CQYSMS",
                    "input": "DNG__0001",
                    "output": "CQY-DNG",
                },
                {
                    "name": "CQYSMS",
                    "input": "ECS",
                    "output": "CQY-ECS",
                },
                {
                    "name": "CQYSMS",
                    "input": "FPS__0001",
                    "output": "CQY-FPS",
                },
                {
                    "name": "CQYSMS",
                    "input": "LNE__0001",
                    "output": "CQY-LNE",
                },
                {
                    "name": "CQYSMS",
                    "input": "DC___0001",
                    "output": "CQY-POW-DC",
                },
                {
                    "name": "CQYSMS",
                    "input": "ETSB_0001",
                    "output": "CQY-POW-ETSB",
                },
                {
                    "name": "CQYSMS",
                    "input": "HV___0001",
                    "output": "CQY-POW-HV",
                },
                {
                    "name": "CQYSMS",
                    "input": "LIG__0001",
                    "output": "CQY-POW-LIG",
                },
                {
                    "name": "CQYSMS",
                    "input": "LV___0001",
                    "output": "CQY-POW-LV",
                },
                {
                    "name": "CQYSMS",
                    "input": "TRAS",
                    "output": "CQY-SIG",
                },
            ]
        },
    },
    "DBG": {
        "output_dir": "dbgsms",
        "environment": {
            "DBG": [
                {
                    "name": "DBGSMS",
                    "input": "BMF",
                    "output": "DBG-BMF",
                },
                {
                    "name": "DBGSMS",
                    "input": "CCTS_0001",
                    "output": "DBG-COM-CCTV",
                },
                {
                    "name": "DBGSMS",
                    "input": "PASS_0001",
                    "output": "DBG-COM-PAS",
                },
                {
                    "name": "DBGSMS",
                    "input": "PISS_0001",
                    "output": "DBG-COM-PIS",
                },
                {
                    "name": "DBGSMS",
                    "input": "DNG__0001",
                    "output": "DBG-DNG",
                },
                {
                    "name": "DBGSMS",
                    "input": "ECS",
                    "output": "DBG-ECS",
                },
                {
                    "name": "DBGSMS",
                    "input": "FPS__0001",
                    "output": "DBG-FPS",
                },
                {
                    "name": "DBGSMS",
                    "input": "LNE__0001",
                    "output": "DBG-LNE",
                },
                {
                    "name": "DBGSMS",
                    "input": "DC___0001",
                    "output": "DBG-POW-DC",
                },
                {
                    "name": "DBGSMS",
                    "input": "ETSB_0001",
                    "output": "DBG-POW-ETSB",
                },
                {
                    "name": "DBGSMS",
                    "input": "HV___0001",
                    "output": "DBG-POW-HV",
                },
                {
                    "name": "DBGSMS",
                    "input": "LIG__0001",
                    "output": "DBG-POW-LIG",
                },
                {
                    "name": "DBGSMS",
                    "input": "LV___0001",
                    "output": "DBG-POW-LV",
                },
                {
                    "name": "DBGSMS",
                    "input": "TRAS",
                    "output": "DBG-SIG",
                },
            ]
        },
    },
    "FRP": {
        "output_dir": "frpsms",
        "environment": {
            "FRP": [
                {
                    "name": "FRPSMS",
                    "input": "BMF",
                    "output": "FRP-BMF",
                },
                {
                    "name": "FRPSMS",
                    "input": "CCTS_0001",
                    "output": "FRP-COM-CCTV",
                },
                {
                    "name": "FRPSMS",
                    "input": "PASS_0001",
                    "output": "FRP-COM-PAS",
                },
                {
                    "name": "FRPSMS",
                    "input": "PISS_0001",
                    "output": "FRP-COM-PIS",
                },
                {
                    "name": "FRPSMS",
                    "input": "DNG__0001",
                    "output": "FRP-DNG",
                },
                {
                    "name": "FRPSMS",
                    "input": "ECS",
                    "output": "FRP-ECS",
                },
                {
                    "name": "FRPSMS",
                    "input": "FPS__0001",
                    "output": "FRP-FPS",
                },
                {
                    "name": "FRPSMS",
                    "input": "LNE__0001",
                    "output": "FRP-LNE",
                },
                {
                    "name": "FRPSMS",
                    "input": "DC___0001",
                    "output": "FRP-POW-DC",
                },
                {
                    "name": "FRPSMS",
                    "input": "ETSB_0001",
                    "output": "FRP-POW-ETSB",
                },
                {
                    "name": "FRPSMS",
                    "input": "HV___0001",
                    "output": "FRP-POW-HV",
                },
                {
                    "name": "FRPSMS",
                    "input": "LIG__0001",
                    "output": "FRP-POW-LIG",
                },
                {
                    "name": "FRPSMS",
                    "input": "LV___0001",
                    "output": "FRP-POW-LV",
                },
                {
                    "name": "FRPSMS",
                    "input": "TRAS",
                    "output": "FRP-SIG",
                },
            ]
        },
    },
    "HBF": {
        "output_dir": "hbfsms",
        "environment": {
            "HBF": [
                {
                    "name": "HBFSMS",
                    "input": "BMF",
                    "output": "HBF-BMF",
                },
                {
                    "name": "HBFSMS",
                    "input": "CCTS_0001",
                    "output": "HBF-COM-CCTV",
                },
                {
                    "name": "HBFSMS",
                    "input": "PASS_0001",
                    "output": "HBF-COM-PAS",
                },
                {
                    "name": "HBFSMS",
                    "input": "PISS_0001",
                    "output": "HBF-COM-PIS",
                },
                {
                    "name": "HBFSMS",
                    "input": "DNG__0001",
                    "output": "HBF-DNG",
                },
                {
                    "name": "HBFSMS",
                    "input": "ECS",
                    "output": "HBF-ECS",
                },
                {
                    "name": "HBFSMS",
                    "input": "FPS__0001",
                    "output": "HBF-FPS",
                },
                {
                    "name": "HBFSMS",
                    "input": "LNE__0001",
                    "output": "HBF-LNE",
                },
                {
                    "name": "HBFSMS",
                    "input": "DC___0001",
                    "output": "HBF-POW-DC",
                },
                {
                    "name": "HBFSMS",
                    "input": "ETSB_0001",
                    "output": "HBF-POW-ETSB",
                },
                {
                    "name": "HBFSMS",
                    "input": "HV___0001",
                    "output": "HBF-POW-HV",
                },
                {
                    "name": "HBFSMS",
                    "input": "LIG__0001",
                    "output": "HBF-POW-LIG",
                },
                {
                    "name": "HBFSMS",
                    "input": "LV___0001",
                    "output": "HBF-POW-LV",
                },
                {
                    "name": "HBFSMS",
                    "input": "TRAT",
                    "output": "HBF-SIG",
                },
            ]
        },
    },
    "HGN": {
        "output_dir": "hgnsms",
        "environment": {
            "HGN": [
                {
                    "name": "HGNSMS",
                    "input": "BMF",
                    "output": "HGN-BMF",
                },
                {
                    "name": "HGNSMS",
                    "input": "CCTS_0001",
                    "output": "HGN-COM-CCTV",
                },
                {
                    "name": "HGNSMS",
                    "input": "PASS_0001",
                    "output": "HGN-COM-PAS",
                },
                {
                    "name": "HGNSMS",
                    "input": "PISS_0001",
                    "output": "HGN-COM-PIS",
                },
                {
                    "name": "HGNSMS",
                    "input": "DNG__0001",
                    "output": "HGN-DNG",
                },
                {
                    "name": "HGNSMS",
                    "input": "ECS",
                    "output": "HGN-ECS",
                },
                {
                    "name": "HGNSMS",
                    "input": "FPS__0001",
                    "output": "HGN-FPS",
                },
                {
                    "name": "HGNSMS",
                    "input": "LNE__0001",
                    "output": "HGN-LNE",
                },
                {
                    "name": "HGNSMS",
                    "input": "DC___0001",
                    "output": "HGN-POW-DC",
                },
                {
                    "name": "HGNSMS",
                    "input": "ETSB_0001",
                    "output": "HGN-POW-ETSB",
                },
                {
                    "name": "HGNSMS",
                    "input": "HV___0001",
                    "output": "HGN-POW-HV",
                },
                {
                    "name": "HGNSMS",
                    "input": "LIG__0001",
                    "output": "HGN-POW-LIG",
                },
                {
                    "name": "HGNSMS",
                    "input": "LV___0001",
                    "output": "HGN-POW-LV",
                },
                {
                    "name": "HGNSMS",
                    "input": "TRAS",
                    "output": "HGN-SIG",
                },
            ]
        },
    },
    "KVN": {
        "output_dir": "kvnsms",
        "environment": {
            "KVN": [
                {
                    "name": "KVNSMS",
                    "input": "BMF",
                    "output": "KVN-BMF",
                },
                {
                    "name": "KVNSMS",
                    "input": "CCTS_0001",
                    "output": "KVN-COM-CCTV",
                },
                {
                    "name": "KVNSMS",
                    "input": "PASS_0001",
                    "output": "KVN-COM-PAS",
                },
                {
                    "name": "KVNSMS",
                    "input": "PISS_0001",
                    "output": "KVN-COM-PIS",
                },
                {
                    "name": "KVNSMS",
                    "input": "DNG__0001",
                    "output": "KVN-DNG",
                },
                {
                    "name": "KVNSMS",
                    "input": "ECS",
                    "output": "KVN-ECS",
                },
                {
                    "name": "KVNSMS",
                    "input": "FPS__0001",
                    "output": "KVN-FPS",
                },
                {
                    "name": "KVNSMS",
                    "input": "LNE__0001",
                    "output": "KVN-LNE",
                },
                {
                    "name": "KVNSMS",
                    "input": "DC___0001",
                    "output": "KVN-POW-DC",
                },
                {
                    "name": "KVNSMS",
                    "input": "ETSB_0001",
                    "output": "KVN-POW-ETSB",
                },
                {
                    "name": "KVNSMS",
                    "input": "HV___0001",
                    "output": "KVN-POW-HV",
                },
                {
                    "name": "KVNSMS",
                    "input": "LIG__0001",
                    "output": "KVN-POW-LIG",
                },
                {
                    "name": "KVNSMS",
                    "input": "LV___0001",
                    "output": "KVN-POW-LV",
                },
                {
                    "name": "KVNSMS",
                    "input": "TRAS",
                    "output": "KVN-SIG",
                },
            ]
        },
    },
    "LTI": {
        "output_dir": "ltisms",
        "environment": {
            "LTI": [
                {
                    "name": "LTISMS",
                    "input": "BMF",
                    "output": "LTI-BMF",
                },
                {
                    "name": "LTISMS",
                    "input": "CCTS_0001",
                    "output": "LTI-COM-CCTV",
                },
                {
                    "name": "LTISMS",
                    "input": "PASS_0001",
                    "output": "LTI-COM-PAS",
                },
                {
                    "name": "LTISMS",
                    "input": "PISS_0001",
                    "output": "LTI-COM-PIS",
                },
                {
                    "name": "LTISMS",
                    "input": "DNG__0001",
                    "output": "LTI-DNG",
                },
                {
                    "name": "LTISMS",
                    "input": "ECS",
                    "output": "LTI-ECS",
                },
                {
                    "name": "LTISMS",
                    "input": "FPS__0001",
                    "output": "LTI-FPS",
                },
                {
                    "name": "LTISMS",
                    "input": "LNE__0001",
                    "output": "LTI-LNE",
                },
                {
                    "name": "LTISMS",
                    "input": "DC___0001",
                    "output": "LTI-POW-DC",
                },
                {
                    "name": "LTISMS",
                    "input": "ETSB_0001",
                    "output": "LTI-POW-ETSB",
                },
                {
                    "name": "LTISMS",
                    "input": "HV___0001",
                    "output": "LTI-POW-HV",
                },
                {
                    "name": "LTISMS",
                    "input": "LIG__0001",
                    "output": "LTI-POW-LIG",
                },
                {
                    "name": "LTISMS",
                    "input": "LV___0001",
                    "output": "LTI-POW-LV",
                },
                {
                    "name": "LTISMS",
                    "input": "TRAS",
                    "output": "LTI-SIG",
                },
            ]
        },
    },
    "OTP": {
        "output_dir": "otpsms",
        "environment": {
            "OTP": [
                {
                    "name": "OTPSMS",
                    "input": "BMF",
                    "output": "OTP-BMF",
                },
                {
                    "name": "OTPSMS",
                    "input": "CCTS_0001",
                    "output": "OTP-COM-CCTV",
                },
                {
                    "name": "OTPSMS",
                    "input": "PASS_0001",
                    "output": "OTP-COM-PAS",
                },
                {
                    "name": "OTPSMS",
                    "input": "PISS_0001",
                    "output": "OTP-COM-PIS",
                },
                {
                    "name": "OTPSMS",
                    "input": "DNG__0001",
                    "output": "OTP-DNG",
                },
                {
                    "name": "OTPSMS",
                    "input": "ECS",
                    "output": "OTP-ECS",
                },
                {
                    "name": "OTPSMS",
                    "input": "FPS__0001",
                    "output": "OTP-FPS",
                },
                {
                    "name": "OTPSMS",
                    "input": "LNE__0001",
                    "output": "OTP-LNE",
                },
                {
                    "name": "OTPSMS",
                    "input": "DC___0001",
                    "output": "OTP-POW-DC",
                },
                {
                    "name": "OTPSMS",
                    "input": "ETSB_0001",
                    "output": "OTP-POW-ETSB",
                },
                {
                    "name": "OTPSMS",
                    "input": "HV___0001",
                    "output": "OTP-POW-HV",
                },
                {
                    "name": "OTPSMS",
                    "input": "LIG__0001",
                    "output": "OTP-POW-LIG",
                },
                {
                    "name": "OTPSMS",
                    "input": "LV___0001",
                    "output": "OTP-POW-LV",
                },
                {
                    "name": "OTPSMS",
                    "input": "TRAS",
                    "output": "OTP-SIG",
                },
            ]
        },
    },
    "PGC": {
        "output_dir": "pgcsms",
        "environment": {
            "PGC": [
                {
                    "name": "PGCSMS",
                    "input": "BMF",
                    "output": "PGC-BMF",
                },
                {
                    "name": "PGCSMS",
                    "input": "CCTS_0001",
                    "output": "PGC-COM-CCTV",
                },
                {
                    "name": "PGCSMS",
                    "input": "PASS_0001",
                    "output": "PGC-COM-PAS",
                },
                {
                    "name": "PGCSMS",
                    "input": "PISS_0001",
                    "output": "PGC-COM-PIS",
                },
                {
                    "name": "PGCSMS",
                    "input": "DNG__0001",
                    "output": "PGC-DNG",
                },
                {
                    "name": "PGCSMS",
                    "input": "ECS",
                    "output": "PGC-ECS",
                },
                {
                    "name": "PGCSMS",
                    "input": "FPS__0001",
                    "output": "PGC-FPS",
                },
                {
                    "name": "PGCSMS",
                    "input": "LNE__0001",
                    "output": "PGC-LNE",
                },
                {
                    "name": "PGCSMS",
                    "input": "DC___0001",
                    "output": "PGC-POW-DC",
                },
                {
                    "name": "PGCSMS",
                    "input": "ETSB_0001",
                    "output": "PGC-POW-ETSB",
                },
                {
                    "name": "PGCSMS",
                    "input": "HV___0001",
                    "output": "PGC-POW-HV",
                },
                {
                    "name": "PGCSMS",
                    "input": "LIG__0001",
                    "output": "PGC-POW-LIG",
                },
                {
                    "name": "PGCSMS",
                    "input": "LV___0001",
                    "output": "PGC-POW-LV",
                },
                {
                    "name": "PGCSMS",
                    "input": "TRAT",
                    "output": "PGC-SIG",
                },
            ]
        },
    },
    "PGL": {
        "output_dir": "pglsms",
        "environment": {
            "PGL": [
                {
                    "name": "PGLSMS",
                    "input": "BMF",
                    "output": "PGL-BMF",
                },
                {
                    "name": "PGLSMS",
                    "input": "CCTS_0001",
                    "output": "PGL-COM-CCTV",
                },
                {
                    "name": "PGLSMS",
                    "input": "PASS_0001",
                    "output": "PGL-COM-PAS",
                },
                {
                    "name": "PGLSMS",
                    "input": "PISS_0001",
                    "output": "PGL-COM-PIS",
                },
                {
                    "name": "PGLSMS",
                    "input": "DNG__0001",
                    "output": "PGL-DNG",
                },
                {
                    "name": "PGLSMS",
                    "input": "ECS",
                    "output": "PGL-ECS",
                },
                {
                    "name": "PGLSMS",
                    "input": "FPS__0001",
                    "output": "PGL-FPS",
                },
                {
                    "name": "PGLSMS",
                    "input": "LNE__0001",
                    "output": "PGL-LNE",
                },
                {
                    "name": "PGLSMS",
                    "input": "DC___0001",
                    "output": "PGL-POW-DC",
                },
                {
                    "name": "PGLSMS",
                    "input": "ETSB_0001",
                    "output": "PGL-POW-ETSB",
                },
                {
                    "name": "PGLSMS",
                    "input": "HV___0001",
                    "output": "PGL-POW-HV",
                },
                {
                    "name": "PGLSMS",
                    "input": "LIG__0001",
                    "output": "PGL-POW-LIG",
                },
                {
                    "name": "PGLSMS",
                    "input": "LV___0001",
                    "output": "PGL-POW-LV",
                },
                {
                    "name": "PGLSMS",
                    "input": "TRAS",
                    "output": "PGL-SIG",
                },
            ]
        },
    },
    "PTP": {
        "output_dir": "ptpsms",
        "environment": {
            "PTP": [
                {
                    "name": "PTPSMS",
                    "input": "BMF",
                    "output": "PTP-BMF",
                },
                {
                    "name": "PTPSMS",
                    "input": "CCTS_0001",
                    "output": "PTP-COM-CCTV",
                },
                {
                    "name": "PTPSMS",
                    "input": "PASS_0001",
                    "output": "PTP-COM-PAS",
                },
                {
                    "name": "PTPSMS",
                    "input": "PISS_0001",
                    "output": "PTP-COM-PIS",
                },
                {
                    "name": "PTPSMS",
                    "input": "DNG__0001",
                    "output": "PTP-DNG",
                },
                {
                    "name": "PTPSMS",
                    "input": "ECS",
                    "output": "PTP-ECS",
                },
                {
                    "name": "PTPSMS",
                    "input": "FPS__0001",
                    "output": "PTP-FPS",
                },
                {
                    "name": "PTPSMS",
                    "input": "LNE__0001",
                    "output": "PTP-LNE",
                },
                {
                    "name": "PTPSMS",
                    "input": "DC___0001",
                    "output": "PTP-POW-DC",
                },
                {
                    "name": "PTPSMS",
                    "input": "ETSB_0001",
                    "output": "PTP-POW-ETSB",
                },
                {
                    "name": "PTPSMS",
                    "input": "HV___0001",
                    "output": "PTP-POW-HV",
                },
                {
                    "name": "PTPSMS",
                    "input": "LIG__0001",
                    "output": "PTP-POW-LIG",
                },
                {
                    "name": "PTPSMS",
                    "input": "LV___0001",
                    "output": "PTP-POW-LV",
                },
                {
                    "name": "PTPSMS",
                    "input": "TRAS",
                    "output": "PTP-SIG",
                },
            ]
        },
    },
    "SER": {
        "output_dir": "sersms",
        "environment": {
            "SER": [
                {
                    "name": "SERSMS",
                    "input": "BMF",
                    "output": "SER-BMF",
                },
                {
                    "name": "SERSMS",
                    "input": "CCTS_0001",
                    "output": "SER-COM-CCTV",
                },
                {
                    "name": "SERSMS",
                    "input": "PASS_0001",
                    "output": "SER-COM-PAS",
                },
                {
                    "name": "SERSMS",
                    "input": "PISS_0001",
                    "output": "SER-COM-PIS",
                },
                {
                    "name": "SERSMS",
                    "input": "DNG__0001",
                    "output": "SER-DNG",
                },
                {
                    "name": "SERSMS",
                    "input": "ECS",
                    "output": "SER-ECS",
                },
                {
                    "name": "SERSMS",
                    "input": "FPS__0001",
                    "output": "SER-FPS",
                },
                {
                    "name": "SERSMS",
                    "input": "LNE__0001",
                    "output": "SER-LNE",
                },
                {
                    "name": "SERSMS",
                    "input": "DC___0001",
                    "output": "SER-POW-DC",
                },
                {
                    "name": "SERSMS",
                    "input": "ETSB_0001",
                    "output": "SER-POW-ETSB",
                },
                {
                    "name": "SERSMS",
                    "input": "HV___0001",
                    "output": "SER-POW-HV",
                },
                {
                    "name": "SERSMS",
                    "input": "LIG__0001",
                    "output": "SER-POW-LIG",
                },
                {
                    "name": "SERSMS",
                    "input": "LV___0001",
                    "output": "SER-POW-LV",
                },
                {
                    "name": "SERSMS",
                    "input": "TRAS",
                    "output": "SER-SIG",
                },
            ]
        },
    },
    "SKG": {
        "output_dir": "skgsms",
        "environment": {
            "SKG": [
                {
                    "name": "SKGSMS",
                    "input": "BMF",
                    "output": "SKG-BMF",
                },
                {
                    "name": "SKGSMS",
                    "input": "CCTS_0001",
                    "output": "SKG-COM-CCTV",
                },
                {
                    "name": "SKGSMS",
                    "input": "PASS_0001",
                    "output": "SKG-COM-PAS",
                },
                {
                    "name": "SKGSMS",
                    "input": "PISS_0001",
                    "output": "SKG-COM-PIS",
                },
                {
                    "name": "SKGSMS",
                    "input": "DNG__0001",
                    "output": "SKG-DNG",
                },
                {
                    "name": "SKGSMS",
                    "input": "ECS",
                    "output": "SKG-ECS",
                },
                {
                    "name": "SKGSMS",
                    "input": "FPS__0001",
                    "output": "SKG-FPS",
                },
                {
                    "name": "SKGSMS",
                    "input": "LNE__0001",
                    "output": "SKG-LNE",
                },
                {
                    "name": "SKGSMS",
                    "input": "DC___0001",
                    "output": "SKG-POW-DC",
                },
                {
                    "name": "SKGSMS",
                    "input": "ETSB_0001",
                    "output": "SKG-POW-ETSB",
                },
                {
                    "name": "SKGSMS",
                    "input": "HV___0001",
                    "output": "SKG-POW-HV",
                },
                {
                    "name": "SKGSMS",
                    "input": "LIG__0001",
                    "output": "SKG-POW-LIG",
                },
                {
                    "name": "SKGSMS",
                    "input": "LV___0001",
                    "output": "SKG-POW-LV",
                },
                {
                    "name": "SKGSMS",
                    "input": "TRAS",
                    "output": "SKG-SIG",
                },
            ]
        },
    },
    "WLH": {
        "output_dir": "wlhsms",
        "environment": {
            "WLH": [
                {
                    "name": "WLHSMS",
                    "input": "BMF",
                    "output": "WLH-BMF",
                },
                {
                    "name": "WLHSMS",
                    "input": "CCTS_0001",
                    "output": "WLH-COM-CCTV",
                },
                {
                    "name": "WLHSMS",
                    "input": "PASS_0001",
                    "output": "WLH-COM-PAS",
                },
                {
                    "name": "WLHSMS",
                    "input": "PISS_0001",
                    "output": "WLH-COM-PIS",
                },
                {
                    "name": "WLHSMS",
                    "input": "DNG__0001",
                    "output": "WLH-DNG",
                },
                {
                    "name": "WLHSMS",
                    "input": "ECS",
                    "output": "WLH-ECS",
                },
                {
                    "name": "WLHSMS",
                    "input": "FPS__0001",
                    "output": "WLH-FPS",
                },
                {
                    "name": "WLHSMS",
                    "input": "LNE__0001",
                    "output": "WLH-LNE",
                },
                {
                    "name": "WLHSMS",
                    "input": "DC___0001",
                    "output": "WLH-POW-DC",
                },
                {
                    "name": "WLHSMS",
                    "input": "ETSB_0001",
                    "output": "WLH-POW-ETSB",
                },
                {
                    "name": "WLHSMS",
                    "input": "HV___0001",
                    "output": "WLH-POW-HV",
                },
                {
                    "name": "WLHSMS",
                    "input": "LIG__0001",
                    "output": "WLH-POW-LIG",
                },
                {
                    "name": "WLHSMS",
                    "input": "LV___0001",
                    "output": "WLH-POW-LV",
                },
                {
                    "name": "WLHSMS",
                    "input": "TRAS",
                    "output": "WLH-SIG",
                },
            ]
        },
    },
    "NED": {
        "output_dir": "nedsms",
        "environment": {
            "NED": [
                {
                    "name": "NEDSMS",
                    "input": "BMF",
                    "output": "NED-BMF",
                },
                {
                    "name": "NEDSMS",
                    "input": "CCTS_0001",
                    "output": "NED-COM-CCTV",
                },
                {
                    "name": "NEDSMS",
                    "input": "PASS_0001",
                    "output": "NED-COM-PAS",
                },
                {
                    "name": "NEDSMS",
                    "input": "FPSD_0001",
                    "output": "NED-FPS",
                },
                {
                    "name": "NEDSMS",
                    "input": "TRAD",
                    "output": "NED-SIG",
                },
                {
                    "name": "NEDSMS",
                    "input": "AMS__0001",
                    "output": "NED-AMS",
                },
            ],
            # The following files do not require NED prefix in names
            "NDI": [
                {
                    "name": "NEDSMS",
                    "input": "DC___0001",
                    "output": "NDI-POW-DC",
                },
                {
                    "name": "NEDSMS",
                    "input": "HV___0001",
                    "output": "NDI-POW-HV",
                },
            ],
            "NPS": [
                {
                    "name": "NEDSMS",
                    "input": "HV___0001",
                    "output": "NPS-POW-HV",
                },
            ],
            "NTS": [
                {
                    "name": "NEDSMS",
                    "input": "DC___0001",
                    "output": "NTS-POW-DC",
                },
                {
                    "name": "NEDSMS",
                    "input": "HV___0001",
                    "output": "NTS-POW-HV",
                },
            ],
        },
    },
    "ATS": {
        "output_dir": "occats",
        "environment": {
            "BGK": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "BGK-SIG",
                },
            ],
            "BNK": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "BNK-SIG",
                },
            ],
            "CNT": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "CNT-SIG",
                },
            ],
            "CQY": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "CQY-SIG",
                },
            ],
            "DBG": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "DBG-SIG",
                },
            ],
            "FRP": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "FRP-SIG",
                },
            ],
            "HBF": [
                {
                    "name": "OCCATS",
                    "input": "TRAT",
                    "output": "HBF-SIG",
                },
            ],
            "HGN": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "HGN-SIG",
                },
            ],
            "KVN": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "KVN-SIG",
                },
            ],
            "LTI": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "LTI-SIG",
                },
            ],
            "OTP": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "OTP-SIG",
                },
            ],
            "PGC": [
                {
                    "name": "OCCATS",
                    "input": "TRAT",
                    "output": "PGC-SIG",
                },
            ],
            "PGL": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "PGL-SIG",
                },
            ],
            "PTP": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "PTP-SIG",
                },
            ],
            "SER": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "SER-SIG",
                },
            ],
            "SKG": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "SKG-SIG",
                },
            ],
            "WLH": [
                {
                    "name": "OCCATS",
                    "input": "TRAS",
                    "output": "WLH-SIG",
                },
            ],
        },
    },
    "CMS": {
        "output_dir": "occcms",
        "environment": {
            "BGK": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "BGK-BMF",
                },
                {
                    "name": "BGKSMS",
                    "input": "CCTS_0001",
                    # FIXME The content of this file is the same as the one from 'bgksms/BGK-COM-CCTV.dat'
                    # I am not sure whether this is always the case or not though.
                    "output": "BGK-COM-CCTV",
                },
                {
                    "name": "BGKSMS",
                    "input": "PASS_0001",
                    # FIXME The content of this file is the same as the one from 'bgksms/BGK-COM-PAS.dat'
                    "output": "BGK-COM-PAS",
                },
                {
                    "name": "BGKSMS",
                    "input": "PISS_0001",
                    # FIXME The content of this file is the same as the one from 'bgksms/BGK-COM-PIS.dat'
                    "output": "BGK-COM-PIS",
                },
            ],
            "BNK": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "BNK-BMF",
                },
                {
                    "name": "BNKSMS",
                    "input": "CCTS_0001",
                    "output": "BNK-COM-CCTV",
                },
                {
                    "name": "BNKSMS",
                    "input": "PASS_0001",
                    "output": "BNK-COM-PAS",
                },
                {
                    "name": "BNKSMS",
                    "input": "PISS_0001",
                    "output": "BNK-COM-PIS",
                },
            ],
            "CNT": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "CNT-BMF",
                },
                {
                    "name": "CNTSMS",
                    "input": "CCTS_0001",
                    "output": "CNT-COM-CCTV",
                },
                {
                    "name": "CNTSMS",
                    "input": "PASS_0001",
                    "output": "CNT-COM-PAS",
                },
                {
                    "name": "CNTSMS",
                    "input": "PISS_0001",
                    "output": "CNT-COM-PIS",
                },
            ],
            "CQY": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "CQY-BMF",
                },
                {
                    "name": "CQYSMS",
                    "input": "CCTS_0001",
                    "output": "CQY-COM-CCTV",
                },
                {
                    "name": "CQYSMS",
                    "input": "PASS_0001",
                    "output": "CQY-COM-PAS",
                },
                {
                    "name": "CQYSMS",
                    "input": "PISS_0001",
                    "output": "CQY-COM-PIS",
                },
            ],
            "DBG": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "DBG-BMF",
                },
                {
                    "name": "DBGSMS",
                    "input": "CCTS_0001",
                    "output": "DBG-COM-CCTV",
                },
                {
                    "name": "DBGSMS",
                    "input": "PASS_0001",
                    "output": "DBG-COM-PAS",
                },
                {
                    "name": "DBGSMS",
                    "input": "PISS_0001",
                    "output": "DBG-COM-PIS",
                },
            ],
            "FRP": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "FRP-BMF",
                },
                {
                    "name": "FRPSMS",
                    "input": "CCTS_0001",
                    "output": "FRP-COM-CCTV",
                },
                {
                    "name": "FRPSMS",
                    "input": "PASS_0001",
                    "output": "FRP-COM-PAS",
                },
                {
                    "name": "FRPSMS",
                    "input": "PISS_0001",
                    "output": "FRP-COM-PIS",
                },
            ],
            "HBF": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "HBF-BMF",
                },
                {
                    "name": "HBFSMS",
                    "input": "CCTS_0001",
                    "output": "HBF-COM-CCTV",
                },
                {
                    "name": "HBFSMS",
                    "input": "PASS_0001",
                    "output": "HBF-COM-PAS",
                },
                {
                    "name": "HBFSMS",
                    "input": "PISS_0001",
                    "output": "HBF-COM-PIS",
                },
            ],
            "HGN": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "HGN-BMF",
                },
                {
                    "name": "HGNSMS",
                    "input": "CCTS_0001",
                    "output": "HGN-COM-CCTV",
                },
                {
                    "name": "HGNSMS",
                    "input": "PASS_0001",
                    "output": "HGN-COM-PAS",
                },
                {
                    "name": "HGNSMS",
                    "input": "PISS_0001",
                    "output": "HGN-COM-PIS",
                },
            ],
            "KVN": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "KVN-BMF",
                },
                {
                    "name": "KVNSMS",
                    "input": "CCTS_0001",
                    "output": "KVN-COM-CCTV",
                },
                {
                    "name": "KVNSMS",
                    "input": "PASS_0001",
                    "output": "KVN-COM-PAS",
                },
                {
                    "name": "KVNSMS",
                    "input": "PISS_0001",
                    "output": "KVN-COM-PIS",
                },
            ],
            "LTI": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "LTI-BMF",
                },
                {
                    "name": "LTISMS",
                    "input": "CCTS_0001",
                    "output": "LTI-COM-CCTV",
                },
                {
                    "name": "LTISMS",
                    "input": "PASS_0001",
                    "output": "LTI-COM-PAS",
                },
                {
                    "name": "LTISMS",
                    "input": "PISS_0001",
                    "output": "LTI-COM-PIS",
                },
            ],
            "OTP": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "OTP-BMF",
                },
                {
                    "name": "OTPSMS",
                    "input": "CCTS_0001",
                    "output": "OTP-COM-CCTV",
                },
                {
                    "name": "OTPSMS",
                    "input": "PASS_0001",
                    "output": "OTP-COM-PAS",
                },
                {
                    "name": "OTPSMS",
                    "input": "PISS_0001",
                    "output": "OTP-COM-PIS",
                },
            ],
            "PGC": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "PGC-BMF",
                },
                {
                    "name": "PGCSMS",
                    "input": "CCTS_0001",
                    "output": "PGC-COM-CCTV",
                },
                {
                    "name": "PGCSMS",
                    "input": "PASS_0001",
                    "output": "PGC-COM-PAS",
                },
                {
                    "name": "PGCSMS",
                    "input": "PISS_0001",
                    "output": "PGC-COM-PIS",
                },
            ],
            "PGL": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "PGL-BMF",
                },
                {
                    "name": "PGLSMS",
                    "input": "CCTS_0001",
                    "output": "PGL-COM-CCTV",
                },
                {
                    "name": "PGLSMS",
                    "input": "PASS_0001",
                    "output": "PGL-COM-PAS",
                },
                {
                    "name": "PGLSMS",
                    "input": "PISS_0001",
                    "output": "PGL-COM-PIS",
                },
            ],
            "PTP": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "PTP-BMF",
                },
                {
                    "name": "PTPSMS",
                    "input": "CCTS_0001",
                    "output": "PTP-COM-CCTV",
                },
                {
                    "name": "PTPSMS",
                    "input": "PASS_0001",
                    "output": "PTP-COM-PAS",
                },
                {
                    "name": "PTPSMS",
                    "input": "PISS_0001",
                    "output": "PTP-COM-PIS",
                },
            ],
            "SER": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "SER-BMF",
                },
                {
                    "name": "SERSMS",
                    "input": "CCTS_0001",
                    "output": "SER-COM-CCTV",
                },
                {
                    "name": "SERSMS",
                    "input": "PASS_0001",
                    "output": "SER-COM-PAS",
                },
                {
                    "name": "SERSMS",
                    "input": "PISS_0001",
                    "output": "SER-COM-PIS",
                },
            ],
            "SKG": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "SKG-BMF",
                },
                {
                    "name": "SKGSMS",
                    "input": "CCTS_0001",
                    "output": "SKG-COM-CCTV",
                },
                {
                    # FIXME For some reason, the existing SKG-COM-PAS.dat file sets ENVIRONEMENT to OCCCMS
                    # even though other station files set it to XXXSMS. The content of the SKG-COM-PAS.dat is also different.
                    "name": "SKGSMS",
                    "input": "PASS_0001",
                    "output": "SKG-COM-PAS",
                },
                {
                    "name": "SKGSMS",
                    "input": "PISS_0001",
                    "output": "SKG-COM-PIS",
                },
            ],
            "WLH": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "WLH-BMF",
                },
                {
                    "name": "WLHSMS",
                    "input": "CCTS_0001",
                    "output": "WLH-COM-CCTV",
                },
                {
                    "name": "WLHSMS",
                    "input": "PASS_0001",
                    "output": "WLH-COM-PAS",
                },
                {
                    "name": "WLHSMS",
                    "input": "PISS_0001",
                    "output": "WLH-COM-PIS",
                },
            ],
            "NED": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "NED-BMF",
                },
                {
                    "name": "OCCCMS",
                    "input": "CCTS_0001",
                    "output": "NED-COM-CCTV",
                },
                {
                    "name": "NEDSMS",
                    "input": "PASS_0001",
                    "output": "NED-COM-PAS",
                },
            ],
            "NDI": [
                {
                    "name": "NEDSMS",
                    "input": "DC___0001",
                    # NOTE The content of this file is the same as the one from 'nedsms/NDI-POW-DC.dat'
                    "output": "NDI-POW-DC",
                },
                {
                    "name": "NEDSMS",
                    "input": "HV___0001",
                    # NOTE The content of this file is the same as the one from 'nedsms/NDI-POW-HV.dat'
                    "output": "NDI-POW-HV",
                },
            ],
            "NPS": [
                {
                    "name": "NEDSMS",
                    "input": "HV___0001",
                    # NOTE The content of this file is the same as the one from 'nedsms/NDI-POW-HV.dat'
                    "output": "NPS-POW-HV",
                },
            ],
            "NTS": [
                {
                    "name": "NEDSMS",
                    "input": "DC___0001",
                    # NOTE: Content of this file is different from 'nedsms/NTS-POW-DC.dat'
                    "output": "NTS-POW-DC",
                },
                {
                    "name": "NEDSMS",
                    "input": "HV___0001",
                    # NOTE: Content of this file is the same as the one from 'nedsms/NTS-POW-HV.dat'
                    "output": "NTS-POW-HV",
                },
            ],
            "OCC": [
                {
                    "name": "OCCCMS",
                    "input": "BMF",
                    "output": "OCC-BMF",
                },
                {
                    "name": "OCCCMS",
                    "input": "CCTS_0001",
                    "output": "OCC-COM-CCTV",
                },
                {
                    "name": "OCCCMS",
                    "input": "PASS_0001",
                    "output": "OCC-COM-PAS",
                },
                {
                    "name": "OCCCMS",
                    "input": "PISS_0001",
                    "output": "OCC-COM-PIS",
                },
            ],
        },
    },
    "ECS": {
        "output_dir": "occecs",
        "environment": {
            "BGK": [
                {
                    "name": "BGKSMS",
                    "input": "ECS",
                    "output": "BGK-ECS",
                },
                {
                    "name": "BGKSMS",
                    "input": "FPS__0001",
                    "output": "BGK-FPS",
                },
                {
                    "name": "BGKSMS",
                    "input": "LNE__0001",
                    "output": "BGK-LNE",
                },
            ],
            "BNK": [
                {
                    "name": "BNKSMS",
                    "input": "ECS",
                    "output": "BNK-ECS",
                },
                {
                    "name": "BNKSMS",
                    "input": "FPS__0001",
                    "output": "BNK-FPS",
                },
                {
                    "name": "BNKSMS",
                    "input": "LNE__0001",
                    "output": "BNK-LNE",
                },
            ],
            "CNT": [
                {
                    "name": "CNTSMS",
                    "input": "ECS",
                    "output": "CNT-ECS",
                },
                {
                    "name": "CNTSMS",
                    "input": "FPS__0001",
                    "output": "CNT-FPS",
                },
                {
                    "name": "CNTSMS",
                    "input": "LNE__0001",
                    "output": "CNT-LNE",
                },
            ],
            "CQY": [
                {
                    "name": "CQYSMS",
                    "input": "ECS",
                    "output": "CQY-ECS",
                },
                {
                    "name": "CQYSMS",
                    "input": "FPS__0001",
                    "output": "CQY-FPS",
                },
                {
                    "name": "CQYSMS",
                    "input": "LNE__0001",
                    "output": "CQY-LNE",
                },
            ],
            "DBG": [
                {
                    "name": "DBGSMS",
                    "input": "ECS",
                    "output": "DBG-ECS",
                },
                {
                    "name": "DBGSMS",
                    "input": "FPS__0001",
                    "output": "DBG-FPS",
                },
                {
                    "name": "DBGSMS",
                    "input": "LNE__0001",
                    "output": "DBG-LNE",
                },
            ],
            "FRP": [
                {
                    "name": "FRPSMS",
                    "input": "ECS",
                    "output": "FRP-ECS",
                },
                {
                    "name": "FRPSMS",
                    "input": "FPS__0001",
                    "output": "FRP-FPS",
                },
                {
                    "name": "FRPSMS",
                    "input": "LNE__0001",
                    "output": "FRP-LNE",
                },
            ],
            "HBF": [
                {
                    "name": "HBFSMS",
                    "input": "ECS",
                    "output": "HBF-ECS",
                },
                {
                    "name": "HBFSMS",
                    "input": "FPS__0001",
                    "output": "HBF-FPS",
                },
                {
                    "name": "HBFSMS",
                    "input": "LNE__0001",
                    "output": "HBF-LNE",
                },
            ],
            "HGN": [
                {
                    "name": "HGNSMS",
                    "input": "ECS",
                    "output": "HGN-ECS",
                },
                {
                    "name": "HGNSMS",
                    "input": "FPS__0001",
                    "output": "HGN-FPS",
                },
                {
                    "name": "HGNSMS",
                    "input": "LNE__0001",
                    "output": "HGN-LNE",
                },
            ],
            "KVN": [
                {
                    "name": "KVNSMS",
                    "input": "ECS",
                    "output": "KVN-ECS",
                },
                {
                    "name": "KVNSMS",
                    "input": "FPS__0001",
                    "output": "KVN-FPS",
                },
                {
                    "name": "KVNSMS",
                    "input": "LNE__0001",
                    "output": "KVN-LNE",
                },
            ],
            "LTI": [
                {
                    "name": "LTISMS",
                    "input": "ECS",
                    "output": "LTI-ECS",
                },
                {
                    "name": "LTISMS",
                    "input": "FPS__0001",
                    "output": "LTI-FPS",
                },
                {
                    "name": "LTISMS",
                    "input": "LNE__0001",
                    "output": "LTI-LNE",
                },
            ],
            "OTP": [
                {
                    "name": "OTPSMS",
                    "input": "ECS",
                    "output": "OTP-ECS",
                },
                {
                    "name": "OTPSMS",
                    "input": "FPS__0001",
                    "output": "OTP-FPS",
                },
                {
                    "name": "OTPSMS",
                    "input": "LNE__0001",
                    "output": "OTP-LNE",
                },
            ],
            "PGC": [
                {
                    "name": "PGCSMS",
                    "input": "ECS",
                    "output": "PGC-ECS",
                },
                {
                    "name": "PGCSMS",
                    "input": "FPS",
                    "output": "PGC-FPS",
                },
                {
                    "name": "PGCSMS",
                    "input": "LNE",
                    "output": "PGC-LNE",
                },
            ],
            "PGL": [
                {
                    "name": "PGLSMS",
                    "input": "ECS",
                    "output": "PGL-ECS",
                },
                {
                    "name": "PGLSMS",
                    "input": "FPS__0001",
                    "output": "PGL-FPS",
                },
                {
                    "name": "PGLSMS",
                    "input": "LNE__0001",
                    "output": "PGL-LNE",
                },
            ],
            "PTP": [
                {
                    "name": "PTPSMS",
                    "input": "ECS",
                    "output": "PTP-ECS",
                },
                {
                    "name": "PTPSMS",
                    "input": "FPS__0001",
                    "output": "PTP-FPS",
                },
                {
                    "name": "PTPSMS",
                    "input": "LNE__0001",
                    "output": "PTP-LNE",
                },
            ],
            "SER": [
                {
                    "name": "SERSMS",
                    "input": "ECS",
                    "output": "SER-ECS",
                },
                {
                    "name": "SERSMS",
                    "input": "FPS__0001",
                    "output": "SER-FPS",
                },
                {
                    "name": "SERSMS",
                    "input": "LNE__0001",
                    "output": "SER-LNE",
                },
            ],
            "SKG": [
                {
                    "name": "SKGSMS",
                    "input": "ECS",
                    "output": "SKG-ECS",
                },
                {
                    "name": "SKGSMS",
                    "input": "FPS__0001",
                    "output": "SKG-FPS",
                },
                {
                    "name": "SKGSMS",
                    "input": "LNE__0001",
                    "output": "SKG-LNE",
                },
            ],
            "WLH": [
                {
                    "name": "WLHSMS",
                    "input": "ECS",
                    "output": "WLH-ECS",
                },
                {
                    "name": "WLHSMS",
                    "input": "FPS__0001",
                    "output": "WLH-FPS",
                },
                {
                    "name": "WLHSMS",
                    "input": "LNE__0001",
                    "output": "WLH-LNE",
                },
            ],
        },
    },
}


def init_logger():
    """
    Initialize logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    c = logging.StreamHandler()
    c_formatter = logging.Formatter(fmt="%(message)s")
    c.setFormatter(c_formatter)
    c.setLevel(logging.INFO)

    f = logging.FileHandler("generate-ssr3.log")
    f_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s")
    f.setFormatter(f_formatter)
    f.setLevel(logging.DEBUG)

    logger.addHandler(c)
    logger.addHandler(f)
    return logger


def valid_dir(xml_dir):
    """
    Returns True when the given xml_dir is a directory
    """
    return os.path.isdir(xml_dir)


def valid_xml_file(xml_file):
    """
    Returns True when a given xml_file is a file
    """
    return os.path.isfile(xml_file)


def is_input_point(name):
    """
    Returns True when a given name is an input point
    """
    if len(name) >= 3:
        return name[0:3] in ["aii", "dii"]
    return False


def write_ssr_file(db_points, environ, ssr_file):
    """
    Write SSR file from given database points
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(ssr_file, "w") as outfile:
        header = f"""###########################################################
#  /home/dbs/SumReport/{environ}/{os.path.basename(ssr_file)}                 #
#  Status Summary Report configuration file               #
#  generated automatically on {timestamp}         #
#                                                         #
###########################################################"""

        outfile.write(f"{header}\n")
        outfile.write(f"ENVIRONEMENT={environ}\n")
        outfile.write("CONFIGURATION=\n")

        for point in db_points:
            outfile.write(f"POINT=<alias>{point}\n")

        logging.info(
            f"No. of database points written to {os.path.basename(ssr_file)}: {len(db_points)}"
        )


def main():
    """
    main function
    """
    init_logger()

    parser = argparse.ArgumentParser(prog="generate-ssr3")
    parser.add_argument(
        "--xml-dir",
        "-x",
        required=True,
        dest="xml_dir",
        help="path to xml_DB_XXX directories",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        dest="output_dir",
        help="path to output directory",
    )
    args = parser.parse_args()
    logging.debug(f"    args: {args}")

    if not valid_dir(args.output_dir):
        logging.error(f"{args.output_dir} is not a valid directory")
        return

    start = time.perf_counter()
    for db_name in _databases.keys():
        # Begin processing each database data ... (e.g., HBF, CMS, etc)
        _db_mapping = _databases.get(db_name)
        if _db_mapping is None:
            logging.warning(f"{db_name} database is not supported")
            continue

        # Check if necessary input directory exists
        xml_dir = f"{args.xml_dir}/xml_DB_{db_name}"
        if not valid_dir(xml_dir):
            logging.warning(f"{xml_dir} is not a valid directory")
            continue

        # Check if necessary output directory exists
        dir_name = _db_mapping.get("output_dir")
        if dir_name is None:
            logging.warning(
                f"{db_name} database does not have output directory defined"
            )
            continue

        # Check if output subdirectory (e.g., occcms, hbfsms) exists
        output_dir = f"{args.output_dir}/{dir_name}"
        if not valid_dir(output_dir):
            try:
                logging.info(f"Creating a new directory: {output_dir}")
                os.mkdir(output_dir)
                logging.info(f"Creating a new directory: {output_dir} ... DONE")
            except OSError:
                logging.error(f"Failed to create a new directory: {output_dir}")
                continue

        start_db = time.perf_counter()
        logging.info(f"Processing {db_name} database ...")

        _environments = _db_mapping.get("environment")
        if _environments is None:
            logging.error(
                f"{db_name} database does not have any environment defined ..."
            )
            continue

        for env_name in _environments:
            # Each database comes with one or more environments
            # Typically, SMS database only contains on environment (e.g. HBF)
            # However, OCC and NED databases contain more than one environment (e.g., stations and)
            start_environ = time.perf_counter()
            logging.info(f"Processing {env_name} environment in {db_name} ...")

            _systems = _environments.get(env_name)
            if _systems is None:
                logging.warning(
                    f"{db_name} database does not have any subsystem defined under {env_name} environment"
                )
                continue

            xml_file = f"{xml_dir}/instancesHierarchy.xml"
            if not valid_xml_file(xml_file):
                logging.error(f"{xml_file} is not a valid file")
                continue

            logging.info(f"Parsing {xml_file} ...")
            _root = ET.parse(xml_file)

            for system in _systems:
                # Process each subsystem within an environment (e.g., BMF, COM-CCTS, LNE, etc)
                start_subsystem = time.perf_counter()
                db_points = []
                input_name = system.get("input")
                logging.info(
                    f"Processing {input_name} in {db_name}-{env_name} environment ..."
                )
                filename = system.get("output")
                if filename is None:
                    logging.warning(
                        f"{input_name} in {db_name}-{env_name} environment does not have output file defined"
                    )
                    continue

                _results = _root.findall(
                    f".//HierarchyItem[@name='{env_name}']//HierarchyItem[@name='{input_name}']//HierarchyItem"
                )
                logging.debug(f"    No. of results: {len(_results)}")
                for item in _results:
                    alias = item.get("alias")
                    name = item.get("name")

                    if alias == f"{env_name}_{name}":
                        continue

                    if not is_input_point(name):
                        continue

                    parent = _root.findall(f".//HierarchyItem[@alias='{alias}']/..")
                    if len(parent) == 1:
                        prefix = parent[0].get("alias")
                        point = f"{prefix}:{name}"
                        db_points.append(point)
                    else:
                        logging.warning(
                            f"Unexpected number of parents for alias {alias}"
                        )

                if len(db_points) > 0:
                    logging.debug(
                        f"    Sorting database points for {input_name} in {db_name}-{env_name} environment"
                    )
                    start_sort = time.perf_counter()
                    db_points.sort(
                        key=cmp_to_key(locale.strcoll)  # This is a locale-aware sort
                    )
                    end_sort = time.perf_counter()
                    logging.debug(
                        f"    Sorting database points for {input_name} in {db_name}-{env_name} environment ... DONE ({end_sort - start_sort:.4f}s)"
                    )

                    ssr_file = f"{output_dir}/{filename}.dat"
                    environ = system.get("name")
                    write_ssr_file(db_points, environ, ssr_file)

                end_subsystem = time.perf_counter()
                logging.info(
                    f"Processing {input_name} in {db_name}-{env_name} environment ... DONE ({end_subsystem - start_subsystem:.4f}s)"
                )

            end_environ = time.perf_counter()
            logging.info(
                f"Processing {env_name} environment in {db_name} ... DONE ({end_environ - start_environ:.4f}s)"
            )

        end_db = time.perf_counter()
        logging.info(
            f"Processing {db_name} database ... DONE ({end_db - start_db:.4f}s)"
        )

    end = time.perf_counter()
    logging.info(f"Total processing time: {end - start:.4f}s")


if __name__ == "__main__":
    main()

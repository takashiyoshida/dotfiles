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

_databases = [
    #
    # BGK database
    #
    {
        # BGK-BMF.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-BMF.dat file
        "location": "BGK",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-BMF.dat to be written to this directory
        "output": "BGK-BMF",
    },
    {
        # BGK-COM-CCTV.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-COM-CCTV.dat file
        "location": "BGK",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-COM-CCTV.dat to be written to this directory
        "output": "BGK-COM-CCTV",
    },
    {
        # BGK-COM-PAS.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-COM-PAS.dat file
        "location": "BGK",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-COM-PAS.dat to be written to this directory
        "output": "BGK-COM-PAS",
    },
    {
        # BGK-COM-PIS.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-COM-PIS.dat file
        "location": "BGK",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-COM-PIS.dat to be written to this directory
        "output": "BGK-COM-PIS",
    },
    {
        # BGK-DNG.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-DNG.dat file
        "location": "BGK",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-DNG.dat to be written to this directory
        "output": "BGK-DNG",
    },
    {
        # BGK-ECS.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-ECS.dat file
        "location": "BGK",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-ECS.dat to be written to this directory
        "output": "BGK-ECS",
    },
    {
        # BGK-FPS.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-FPS.dat file
        "location": "BGK",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-FPS.dat to be written to this directory
        "output": "BGK-FPS",
    },
    {
        # BGK-LNE.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-LNE.dat file
        "location": "BGK",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-LNE.dat to be written to this directory
        "output": "BGK-LNE",
    },
    {
        # BGK-POW-DC.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-POW-DC.dat file
        "location": "BGK",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-POW-DC.dat to be written to this directory
        "output": "BGK-POW-DC",
    },
    {
        # BGK-POW-ETSB.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-POW-ETSB.dat file
        "location": "BGK",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-ETSB.dat to be written to this directory
        "output": "BGK-POW-ETSB",
    },
    {
        # BGK-POW-HV.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-POW-HV.dat file
        "location": "BGK",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-POW-HV.dat to be written to this directory
        "output": "BGK-POW-HV",
    },
    {
        # BGK-POW-LIG.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-POW-LIG.dat file
        "location": "BGK",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-POW-LIG.dat to be written to this directory
        "output": "BGK-POW-LIG",
    },
    {
        # BGK-POW-LV.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-POW-LV.dat file
        "location": "BGK",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-POW-LV.dat to be written to this directory
        "output": "BGK-POW-LV",
    },
    {
        # BGK-SIG.dat file from BGKSMS database
        "database": "BGK",  # xml_DB_BGK
        "environ": "BGKSMS",  # data written to BGK-SIG.dat file
        "location": "BGK",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "bgksms",  # BGK-SIG.dat to be written to this directory
        "output": "BGK-SIG",
    },
    #
    # BNK database
    #
    {
        # BNK-BMF.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-BMF.dat file
        "location": "BNK",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-BMF.dat to be written to this directory
        "output": "BNK-BMF",
    },
    {
        # BNK-COM-CCTV.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-COM-CCTV.dat file
        "location": "BNK",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-COM-CCTV.dat to be written to this directory
        "output": "BNK-COM-CCTV",
    },
    {
        # BNK-COM-PAS.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-COM-PAS.dat file
        "location": "BNK",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-COM-PAS.dat to be written to this directory
        "output": "BNK-COM-PAS",
    },
    {
        # BNK-COM-PIS.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-COM-PIS.dat file
        "location": "BNK",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-COM-PIS.dat to be written to this directory
        "output": "BNK-COM-PIS",
    },
    {
        # BNK-DNG.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-DNG.dat file
        "location": "BNK",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-DNG.dat to be written to this directory
        "output": "BNK-DNG",
    },
    {
        # BNK-ECS.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-ECS.dat file
        "location": "BNK",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-ECS.dat to be written to this directory
        "output": "BNK-ECS",
    },
    {
        # BNK-FPS.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-FPS.dat file
        "location": "BNK",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-FPS.dat to be written to this directory
        "output": "BNK-FPS",
    },
    {
        # BNK-LNE.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-LNE.dat file
        "location": "BNK",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-LNE.dat to be written to this directory
        "output": "BNK-LNE",
    },
    {
        # BNK-POW-DC.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-POW-DC.dat file
        "location": "BNK",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-POW-DC.dat to be written to this directory
        "output": "BNK-POW-DC",
    },
    {
        # BNK-POW-ETSB.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-POW-ETSB.dat file
        "location": "BNK",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-ETSB.dat to be written to this directory
        "output": "BNK-POW-ETSB",
    },
    {
        # BNK-POW-HV.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-POW-HV.dat file
        "location": "BNK",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-POW-HV.dat to be written to this directory
        "output": "BNK-POW-HV",
    },
    {
        # BNK-POW-LIG.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-POW-LIG.dat file
        "location": "BNK",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-POW-LIG.dat to be written to this directory
        "output": "BNK-POW-LIG",
    },
    {
        # BNK-POW-LV.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-POW-LV.dat file
        "location": "BNK",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-POW-LV.dat to be written to this directory
        "output": "BNK-POW-LV",
    },
    {
        # BNK-SIG.dat file from BNKSMS database
        "database": "BNK",  # xml_DB_BNK
        "environ": "BNKSMS",  # data written to BNK-SIG.dat file
        "location": "BNK",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "bnksms",  # BNK-SIG.dat to be written to this directory
        "output": "BNK-SIG",
    },
    #
    # CNT database
    #
    {
        # CNT-BMF.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-BMF.dat file
        "location": "CNT",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-BMF.dat to be written to this directory
        "output": "CNT-BMF",
    },
    {
        # CNT-COM-CCTV.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-COM-CCTV.dat file
        "location": "CNT",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-COM-CCTV.dat to be written to this directory
        "output": "CNT-COM-CCTV",
    },
    {
        # CNT-COM-PAS.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-COM-PAS.dat file
        "location": "CNT",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-COM-PAS.dat to be written to this directory
        "output": "CNT-COM-PAS",
    },
    {
        # CNT-COM-PIS.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-COM-PIS.dat file
        "location": "CNT",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-COM-PIS.dat to be written to this directory
        "output": "CNT-COM-PIS",
    },
    {
        # CNT-DNG.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-DNG.dat file
        "location": "CNT",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-DNG.dat to be written to this directory
        "output": "CNT-DNG",
    },
    {
        # CNT-ECS.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-ECS.dat file
        "location": "CNT",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-ECS.dat to be written to this directory
        "output": "CNT-ECS",
    },
    {
        # CNT-FPS.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-FPS.dat file
        "location": "CNT",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-FPS.dat to be written to this directory
        "output": "CNT-FPS",
    },
    {
        # CNT-LNE.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-LNE.dat file
        "location": "CNT",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-LNE.dat to be written to this directory
        "output": "CNT-LNE",
    },
    {
        # CNT-POW-DC.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-POW-DC.dat file
        "location": "CNT",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-POW-DC.dat to be written to this directory
        "output": "CNT-POW-DC",
    },
    {
        # CNT-POW-ETSB.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-POW-ETSB.dat file
        "location": "CNT",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-ETSB.dat to be written to this directory
        "output": "CNT-POW-ETSB",
    },
    {
        # CNT-POW-HV.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-POW-HV.dat file
        "location": "CNT",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-POW-HV.dat to be written to this directory
        "output": "CNT-POW-HV",
    },
    {
        # CNT-POW-LIG.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-POW-LIG.dat file
        "location": "CNT",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-POW-LIG.dat to be written to this directory
        "output": "CNT-POW-LIG",
    },
    {
        # CNT-POW-LV.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-POW-LV.dat file
        "location": "CNT",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-POW-LV.dat to be written to this directory
        "output": "CNT-POW-LV",
    },
    {
        # CNT-SIG.dat file from CNTSMS database
        "database": "CNT",  # xml_DB_CNT
        "environ": "CNTSMS",  # data written to CNT-SIG.dat file
        "location": "CNT",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "cntsms",  # CNT-SIG.dat to be written to this directory
        "output": "CNT-SIG",
    },
    #
    # CQY database
    #
    {
        # CQY-BMF.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-BMF.dat file
        "location": "CQY",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-BMF.dat to be written to this directory
        "output": "CQY-BMF",
    },
    {
        # CQY-COM-CCTV.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-COM-CCTV.dat file
        "location": "CQY",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-COM-CCTV.dat to be written to this directory
        "output": "CQY-COM-CCTV",
    },
    {
        # CQY-COM-PAS.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-COM-PAS.dat file
        "location": "CQY",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-COM-PAS.dat to be written to this directory
        "output": "CQY-COM-PAS",
    },
    {
        # CQY-COM-PIS.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-COM-PIS.dat file
        "location": "CQY",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-COM-PIS.dat to be written to this directory
        "output": "CQY-COM-PIS",
    },
    {
        # CQY-DNG.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-DNG.dat file
        "location": "CQY",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-DNG.dat to be written to this directory
        "output": "CQY-DNG",
    },
    {
        # CQY-ECS.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-ECS.dat file
        "location": "CQY",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-ECS.dat to be written to this directory
        "output": "CQY-ECS",
    },
    {
        # CQY-FPS.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-FPS.dat file
        "location": "CQY",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-FPS.dat to be written to this directory
        "output": "CQY-FPS",
    },
    {
        # CQY-LNE.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-LNE.dat file
        "location": "CQY",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-LNE.dat to be written to this directory
        "output": "CQY-LNE",
    },
    {
        # CQY-POW-DC.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-POW-DC.dat file
        "location": "CQY",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-POW-DC.dat to be written to this directory
        "output": "CQY-POW-DC",
    },
    {
        # CQY-POW-ETSB.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-POW-ETSB.dat file
        "location": "CQY",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-ETSB.dat to be written to this directory
        "output": "CQY-POW-ETSB",
    },
    {
        # CQY-POW-HV.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-POW-HV.dat file
        "location": "CQY",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-POW-HV.dat to be written to this directory
        "output": "CQY-POW-HV",
    },
    {
        # CQY-POW-LIG.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-POW-LIG.dat file
        "location": "CQY",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-POW-LIG.dat to be written to this directory
        "output": "CQY-POW-LIG",
    },
    {
        # CQY-POW-LV.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-POW-LV.dat file
        "location": "CQY",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-POW-LV.dat to be written to this directory
        "output": "CQY-POW-LV",
    },
    {
        # CQY-SIG.dat file from CQYSMS database
        "database": "CQY",  # xml_DB_CQY
        "environ": "CQYSMS",  # data written to CQY-SIG.dat file
        "location": "CQY",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "cqysms",  # CQY-SIG.dat to be written to this directory
        "output": "CQY-SIG",
    },
    #
    # DBG database
    #
    {
        # DBG-BMF.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-BMF.dat file
        "location": "DBG",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-BMF.dat to be written to this directory
        "output": "DBG-BMF",
    },
    {
        # DBG-COM-CCTV.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-COM-CCTV.dat file
        "location": "DBG",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-COM-CCTV.dat to be written to this directory
        "output": "DBG-COM-CCTV",
    },
    {
        # DBG-COM-PAS.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-COM-PAS.dat file
        "location": "DBG",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-COM-PAS.dat to be written to this directory
        "output": "DBG-COM-PAS",
    },
    {
        # DBG-COM-PIS.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-COM-PIS.dat file
        "location": "DBG",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-COM-PIS.dat to be written to this directory
        "output": "DBG-COM-PIS",
    },
    {
        # DBG-DNG.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-DNG.dat file
        "location": "DBG",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-DNG.dat to be written to this directory
        "output": "DBG-DNG",
    },
    {
        # DBG-ECS.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-ECS.dat file
        "location": "DBG",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-ECS.dat to be written to this directory
        "output": "DBG-ECS",
    },
    {
        # DBG-FPS.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-FPS.dat file
        "location": "DBG",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-FPS.dat to be written to this directory
        "output": "DBG-FPS",
    },
    {
        # DBG-LNE.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-LNE.dat file
        "location": "DBG",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-LNE.dat to be written to this directory
        "output": "DBG-LNE",
    },
    {
        # DBG-POW-DC.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-POW-DC.dat file
        "location": "DBG",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-POW-DC.dat to be written to this directory
        "output": "DBG-POW-DC",
    },
    {
        # DBG-POW-ETSB.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-POW-ETSB.dat file
        "location": "DBG",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-ETSB.dat to be written to this directory
        "output": "DBG-POW-ETSB",
    },
    {
        # DBG-POW-HV.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-POW-HV.dat file
        "location": "DBG",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-POW-HV.dat to be written to this directory
        "output": "DBG-POW-HV",
    },
    {
        # DBG-POW-LIG.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-POW-LIG.dat file
        "location": "DBG",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-POW-LIG.dat to be written to this directory
        "output": "DBG-POW-LIG",
    },
    {
        # DBG-POW-LV.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-POW-LV.dat file
        "location": "DBG",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-POW-LV.dat to be written to this directory
        "output": "DBG-POW-LV",
    },
    {
        # DBG-SIG.dat file from DBGSMS database
        "database": "DBG",  # xml_DB_DBG
        "environ": "DBGSMS",  # data written to DBG-SIG.dat file
        "location": "DBG",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "dbgsms",  # DBG-SIG.dat to be written to this directory
        "output": "DBG-SIG",
    },
    #
    # FRP database
    #
    {
        # FRP-BMF.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-BMF.dat file
        "location": "FRP",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-BMF.dat to be written to this directory
        "output": "FRP-BMF",
    },
    {
        # FRP-COM-CCTV.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-COM-CCTV.dat file
        "location": "FRP",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-COM-CCTV.dat to be written to this directory
        "output": "FRP-COM-CCTV",
    },
    {
        # FRP-COM-PAS.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-COM-PAS.dat file
        "location": "FRP",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-COM-PAS.dat to be written to this directory
        "output": "FRP-COM-PAS",
    },
    {
        # FRP-COM-PIS.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-COM-PIS.dat file
        "location": "FRP",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-COM-PIS.dat to be written to this directory
        "output": "FRP-COM-PIS",
    },
    {
        # FRP-DNG.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-DNG.dat file
        "location": "FRP",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-DNG.dat to be written to this directory
        "output": "FRP-DNG",
    },
    {
        # FRP-ECS.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-ECS.dat file
        "location": "FRP",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-ECS.dat to be written to this directory
        "output": "FRP-ECS",
    },
    {
        # FRP-FPS.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-FPS.dat file
        "location": "FRP",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-FPS.dat to be written to this directory
        "output": "FRP-FPS",
    },
    {
        # FRP-LNE.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-LNE.dat file
        "location": "FRP",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-LNE.dat to be written to this directory
        "output": "FRP-LNE",
    },
    {
        # FRP-POW-DC.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-POW-DC.dat file
        "location": "FRP",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-POW-DC.dat to be written to this directory
        "output": "FRP-POW-DC",
    },
    {
        # FRP-POW-ETSB.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-POW-ETSB.dat file
        "location": "FRP",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-ETSB.dat to be written to this directory
        "output": "FRP-POW-ETSB",
    },
    {
        # FRP-POW-HV.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-POW-HV.dat file
        "location": "FRP",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-POW-HV.dat to be written to this directory
        "output": "FRP-POW-HV",
    },
    {
        # FRP-POW-LIG.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-POW-LIG.dat file
        "location": "FRP",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-POW-LIG.dat to be written to this directory
        "output": "FRP-POW-LIG",
    },
    {
        # FRP-POW-LV.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-POW-LV.dat file
        "location": "FRP",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-POW-LV.dat to be written to this directory
        "output": "FRP-POW-LV",
    },
    {
        # FRP-SIG.dat file from FRPSMS database
        "database": "FRP",  # xml_DB_FRP
        "environ": "FRPSMS",  # data written to FRP-SIG.dat file
        "location": "FRP",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "frpsms",  # FRP-SIG.dat to be written to this directory
        "output": "FRP-SIG",
    },
    #
    # HBF database
    #
    {
        # HBF-BMF.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-BMF.dat file
        "location": "HBF",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-BMF.dat to be written to this directory
        "output": "HBF-BMF",
    },
    {
        # HBF-COM-CCTV.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-COM-CCTV.dat file
        "location": "HBF",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-COM-CCTV.dat to be written to this directory
        "output": "HBF-COM-CCTV",
    },
    {
        # HBF-COM-PAS.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-COM-PAS.dat file
        "location": "HBF",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-COM-PAS.dat to be written to this directory
        "output": "HBF-COM-PAS",
    },
    {
        # HBF-COM-PIS.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-COM-PIS.dat file
        "location": "HBF",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-COM-PIS.dat to be written to this directory
        "output": "HBF-COM-PIS",
    },
    {
        # HBF-DNG.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-DNG.dat file
        "location": "HBF",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-DNG.dat to be written to this directory
        "output": "HBF-DNG",
    },
    {
        # HBF-ECS.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-ECS.dat file
        "location": "HBF",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-ECS.dat to be written to this directory
        "output": "HBF-ECS",
    },
    {
        # HBF-FPS.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-FPS.dat file
        "location": "HBF",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-FPS.dat to be written to this directory
        "output": "HBF-FPS",
    },
    {
        # HBF-LNE.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-LNE.dat file
        "location": "HBF",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-LNE.dat to be written to this directory
        "output": "HBF-LNE",
    },
    {
        # HBF-POW-DC.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-POW-DC.dat file
        "location": "HBF",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-POW-DC.dat to be written to this directory
        "output": "HBF-POW-DC",
    },
    {
        # HBF-POW-ETSB.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-POW-ETSB.dat file
        "location": "HBF",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-ETSB.dat to be written to this directory
        "output": "HBF-POW-ETSB",
    },
    {
        # HBF-POW-HV.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-POW-HV.dat file
        "location": "HBF",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-POW-HV.dat to be written to this directory
        "output": "HBF-POW-HV",
    },
    {
        # HBF-POW-LIG.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-POW-LIG.dat file
        "location": "HBF",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-POW-LIG.dat to be written to this directory
        "output": "HBF-POW-LIG",
    },
    {
        # HBF-POW-LV.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-POW-LV.dat file
        "location": "HBF",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-POW-LV.dat to be written to this directory
        "output": "HBF-POW-LV",
    },
    {
        # HBF-SIG.dat file from HBFSMS database
        "database": "HBF",  # xml_DB_HBF
        "environ": "HBFSMS",  # data written to HBF-SIG.dat file
        "location": "HBF",
        "system": "TRAT",  # search for BMF in the xml file
        "output_dir": "hbfsms",  # HBF-SIG.dat to be written to this directory
        "output": "HBF-SIG",
    },
    #
    # HGN database
    #
    {
        # HGN-BMF.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-BMF.dat file
        "location": "HGN",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-BMF.dat to be written to this directory
        "output": "HGN-BMF",
    },
    {
        # HGN-COM-CCTV.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-COM-CCTV.dat file
        "location": "HGN",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-COM-CCTV.dat to be written to this directory
        "output": "HGN-COM-CCTV",
    },
    {
        # HGN-COM-PAS.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-COM-PAS.dat file
        "location": "HGN",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-COM-PAS.dat to be written to this directory
        "output": "HGN-COM-PAS",
    },
    {
        # HGN-COM-PIS.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-COM-PIS.dat file
        "location": "HGN",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-COM-PIS.dat to be written to this directory
        "output": "HGN-COM-PIS",
    },
    {
        # HGN-DNG.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-DNG.dat file
        "location": "HGN",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-DNG.dat to be written to this directory
        "output": "HGN-DNG",
    },
    {
        # HGN-ECS.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-ECS.dat file
        "location": "HGN",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-ECS.dat to be written to this directory
        "output": "HGN-ECS",
    },
    {
        # HGN-FPS.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-FPS.dat file
        "location": "HGN",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-FPS.dat to be written to this directory
        "output": "HGN-FPS",
    },
    {
        # HGN-LNE.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-LNE.dat file
        "location": "HGN",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-LNE.dat to be written to this directory
        "output": "HGN-LNE",
    },
    {
        # HGN-POW-DC.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-POW-DC.dat file
        "location": "HGN",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-POW-DC.dat to be written to this directory
        "output": "HGN-POW-DC",
    },
    {
        # HGN-POW-ETSB.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-POW-ETSB.dat file
        "location": "HGN",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-ETSB.dat to be written to this directory
        "output": "HGN-POW-ETSB",
    },
    {
        # HGN-POW-HV.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-POW-HV.dat file
        "location": "HGN",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-POW-HV.dat to be written to this directory
        "output": "HGN-POW-HV",
    },
    {
        # HGN-POW-LIG.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-POW-LIG.dat file
        "location": "HGN",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-POW-LIG.dat to be written to this directory
        "output": "HGN-POW-LIG",
    },
    {
        # HGN-POW-LV.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-POW-LV.dat file
        "location": "HGN",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-POW-LV.dat to be written to this directory
        "output": "HGN-POW-LV",
    },
    {
        # HGN-SIG.dat file from HGNSMS database
        "database": "HGN",  # xml_DB_HGN
        "environ": "HGNSMS",  # data written to HGN-SIG.dat file
        "location": "HGN",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "hgnsms",  # HGN-SIG.dat to be written to this directory
        "output": "HGN-SIG",
    },
    #
    # KVN database
    #
    {
        # KVN-BMF.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-BMF.dat file
        "location": "KVN",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-BMF.dat to be written to this directory
        "output": "KVN-BMF",
    },
    {
        # KVN-COM-CCTV.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-COM-CCTV.dat file
        "location": "KVN",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-COM-CCTV.dat to be written to this directory
        "output": "KVN-COM-CCTV",
    },
    {
        # KVN-COM-PAS.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-COM-PAS.dat file
        "location": "KVN",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-COM-PAS.dat to be written to this directory
        "output": "KVN-COM-PAS",
    },
    {
        # KVN-COM-PIS.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-COM-PIS.dat file
        "location": "KVN",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-COM-PIS.dat to be written to this directory
        "output": "KVN-COM-PIS",
    },
    {
        # KVN-DNG.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-DNG.dat file
        "location": "KVN",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-DNG.dat to be written to this directory
        "output": "KVN-DNG",
    },
    {
        # KVN-ECS.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-ECS.dat file
        "location": "KVN",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-ECS.dat to be written to this directory
        "output": "KVN-ECS",
    },
    {
        # KVN-FPS.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-FPS.dat file
        "location": "KVN",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-FPS.dat to be written to this directory
        "output": "KVN-FPS",
    },
    {
        # KVN-LNE.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-LNE.dat file
        "location": "KVN",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-LNE.dat to be written to this directory
        "output": "KVN-LNE",
    },
    {
        # KVN-POW-DC.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-POW-DC.dat file
        "location": "KVN",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-POW-DC.dat to be written to this directory
        "output": "KVN-POW-DC",
    },
    {
        # KVN-POW-ETSB.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-POW-ETSB.dat file
        "location": "KVN",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-ETSB.dat to be written to this directory
        "output": "KVN-POW-ETSB",
    },
    {
        # KVN-POW-HV.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-POW-HV.dat file
        "location": "KVN",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-POW-HV.dat to be written to this directory
        "output": "KVN-POW-HV",
    },
    {
        # KVN-POW-LIG.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-POW-LIG.dat file
        "location": "KVN",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-POW-LIG.dat to be written to this directory
        "output": "KVN-POW-LIG",
    },
    {
        # KVN-POW-LV.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-POW-LV.dat file
        "location": "KVN",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-POW-LV.dat to be written to this directory
        "output": "KVN-POW-LV",
    },
    {
        # KVN-SIG.dat file from KVNSMS database
        "database": "KVN",  # xml_DB_KVN
        "environ": "KVNSMS",  # data written to KVN-SIG.dat file
        "location": "KVN",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "kvnsms",  # KVN-SIG.dat to be written to this directory
        "output": "KVN-SIG",
    },
    #
    # LTI database
    #
    {
        # LTI-BMF.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-BMF.dat file
        "location": "LTI",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-BMF.dat to be written to this directory
        "output": "LTI-BMF",
    },
    {
        # LTI-COM-CCTV.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-COM-CCTV.dat file
        "location": "LTI",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-COM-CCTV.dat to be written to this directory
        "output": "LTI-COM-CCTV",
    },
    {
        # LTI-COM-PAS.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-COM-PAS.dat file
        "location": "LTI",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-COM-PAS.dat to be written to this directory
        "output": "LTI-COM-PAS",
    },
    {
        # LTI-COM-PIS.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-COM-PIS.dat file
        "location": "LTI",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-COM-PIS.dat to be written to this directory
        "output": "LTI-COM-PIS",
    },
    {
        # LTI-DNG.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-DNG.dat file
        "location": "LTI",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-DNG.dat to be written to this directory
        "output": "LTI-DNG",
    },
    {
        # LTI-ECS.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-ECS.dat file
        "location": "LTI",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-ECS.dat to be written to this directory
        "output": "LTI-ECS",
    },
    {
        # LTI-FPS.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-FPS.dat file
        "location": "LTI",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-FPS.dat to be written to this directory
        "output": "LTI-FPS",
    },
    {
        # LTI-LNE.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-LNE.dat file
        "location": "LTI",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-LNE.dat to be written to this directory
        "output": "LTI-LNE",
    },
    {
        # LTI-POW-DC.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-POW-DC.dat file
        "location": "LTI",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-POW-DC.dat to be written to this directory
        "output": "LTI-POW-DC",
    },
    {
        # LTI-POW-ETSB.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-POW-ETSB.dat file
        "location": "LTI",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-ETSB.dat to be written to this directory
        "output": "LTI-POW-ETSB",
    },
    {
        # LTI-POW-HV.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-POW-HV.dat file
        "location": "LTI",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-POW-HV.dat to be written to this directory
        "output": "LTI-POW-HV",
    },
    {
        # LTI-POW-LIG.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-POW-LIG.dat file
        "location": "LTI",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-POW-LIG.dat to be written to this directory
        "output": "LTI-POW-LIG",
    },
    {
        # LTI-POW-LV.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-POW-LV.dat file
        "location": "LTI",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-POW-LV.dat to be written to this directory
        "output": "LTI-POW-LV",
    },
    {
        # LTI-SIG.dat file from LTISMS database
        "database": "LTI",  # xml_DB_LTI
        "environ": "LTISMS",  # data written to LTI-SIG.dat file
        "location": "LTI",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "ltisms",  # LTI-SIG.dat to be written to this directory
        "output": "LTI-SIG",
    },
    #
    # OTP database
    #
    {
        # OTP-BMF.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-BMF.dat file
        "location": "OTP",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-BMF.dat to be written to this directory
        "output": "OTP-BMF",
    },
    {
        # OTP-COM-CCTV.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-COM-CCTV.dat file
        "location": "OTP",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-COM-CCTV.dat to be written to this directory
        "output": "OTP-COM-CCTV",
    },
    {
        # OTP-COM-PAS.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-COM-PAS.dat file
        "location": "OTP",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-COM-PAS.dat to be written to this directory
        "output": "OTP-COM-PAS",
    },
    {
        # OTP-COM-PIS.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-COM-PIS.dat file
        "location": "OTP",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-COM-PIS.dat to be written to this directory
        "output": "OTP-COM-PIS",
    },
    {
        # OTP-DNG.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-DNG.dat file
        "location": "OTP",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-DNG.dat to be written to this directory
        "output": "OTP-DNG",
    },
    {
        # OTP-ECS.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-ECS.dat file
        "location": "OTP",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-ECS.dat to be written to this directory
        "output": "OTP-ECS",
    },
    {
        # OTP-FPS.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-FPS.dat file
        "location": "OTP",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-FPS.dat to be written to this directory
        "output": "OTP-FPS",
    },
    {
        # OTP-LNE.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-LNE.dat file
        "location": "OTP",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-LNE.dat to be written to this directory
        "output": "OTP-LNE",
    },
    {
        # OTP-POW-DC.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-POW-DC.dat file
        "location": "OTP",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-POW-DC.dat to be written to this directory
        "output": "OTP-POW-DC",
    },
    {
        # OTP-POW-ETSB.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-POW-ETSB.dat file
        "location": "OTP",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-ETSB.dat to be written to this directory
        "output": "OTP-POW-ETSB",
    },
    {
        # OTP-POW-HV.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-POW-HV.dat file
        "location": "OTP",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-POW-HV.dat to be written to this directory
        "output": "OTP-POW-HV",
    },
    {
        # OTP-POW-LIG.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-POW-LIG.dat file
        "location": "OTP",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-POW-LIG.dat to be written to this directory
        "output": "OTP-POW-LIG",
    },
    {
        # OTP-POW-LV.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-POW-LV.dat file
        "location": "OTP",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-POW-LV.dat to be written to this directory
        "output": "OTP-POW-LV",
    },
    {
        # OTP-SIG.dat file from OTPSMS database
        "database": "OTP",  # xml_DB_OTP
        "environ": "OTPSMS",  # data written to OTP-SIG.dat file
        "location": "OTP",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "otpsms",  # OTP-SIG.dat to be written to this directory
        "output": "OTP-SIG",
    },
    #
    # PGC database
    #
    {
        # PGC-BMF.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-BMF.dat file
        "location": "PGC",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-BMF.dat to be written to this directory
        "output": "PGC-BMF",
    },
    {
        # PGC-COM-CCTV.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-COM-CCTV.dat file
        "location": "PGC",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-COM-CCTV.dat to be written to this directory
        "output": "PGC-COM-CCTV",
    },
    {
        # PGC-COM-PAS.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-COM-PAS.dat file
        "location": "PGC",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-COM-PAS.dat to be written to this directory
        "output": "PGC-COM-PAS",
    },
    {
        # PGC-COM-PIS.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-COM-PIS.dat file
        "location": "PGC",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-COM-PIS.dat to be written to this directory
        "output": "PGC-COM-PIS",
    },
    {
        # PGC-DNG.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-DNG.dat file
        "location": "PGC",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-DNG.dat to be written to this directory
        "output": "PGC-DNG",
    },
    {
        # PGC-ECS.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-ECS.dat file
        "location": "PGC",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-ECS.dat to be written to this directory
        "output": "PGC-ECS",
    },
    {
        # PGC-FPS.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-FPS.dat file
        "location": "PGC",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-FPS.dat to be written to this directory
        "output": "PGC-FPS",
    },
    {
        # PGC-LNE.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-LNE.dat file
        "location": "PGC",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-LNE.dat to be written to this directory
        "output": "PGC-LNE",
    },
    {
        # PGC-POW-DC.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-POW-DC.dat file
        "location": "PGC",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-POW-DC.dat to be written to this directory
        "output": "PGC-POW-DC",
    },
    {
        # PGC-POW-ETSB.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-POW-ETSB.dat file
        "location": "PGC",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-ETSB.dat to be written to this directory
        "output": "PGC-POW-ETSB",
    },
    {
        # PGC-POW-HV.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-POW-HV.dat file
        "location": "PGC",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-POW-HV.dat to be written to this directory
        "output": "PGC-POW-HV",
    },
    {
        # PGC-POW-LIG.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-POW-LIG.dat file
        "location": "PGC",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-POW-LIG.dat to be written to this directory
        "output": "PGC-POW-LIG",
    },
    {
        # PGC-POW-LV.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-POW-LV.dat file
        "location": "PGC",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-POW-LV.dat to be written to this directory
        "output": "PGC-POW-LV",
    },
    {
        # PGC-SIG.dat file from PGCSMS database
        "database": "PGC",  # xml_DB_PGC
        "environ": "PGCSMS",  # data written to PGC-SIG.dat file
        "location": "PGC",
        "system": "TRAT",  # search for BMF in the xml file
        "output_dir": "pgcsms",  # PGC-SIG.dat to be written to this directory
        "output": "PGC-SIG",
    },
    #
    # PGL database
    #
    {
        # PGL-BMF.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-BMF.dat file
        "location": "PGL",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-BMF.dat to be written to this directory
        "output": "PGL-BMF",
    },
    {
        # PGL-COM-CCTV.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-COM-CCTV.dat file
        "location": "PGL",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-COM-CCTV.dat to be written to this directory
        "output": "PGL-COM-CCTV",
    },
    {
        # PGL-COM-PAS.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-COM-PAS.dat file
        "location": "PGL",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-COM-PAS.dat to be written to this directory
        "output": "PGL-COM-PAS",
    },
    {
        # PGL-COM-PIS.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-COM-PIS.dat file
        "location": "PGL",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-COM-PIS.dat to be written to this directory
        "output": "PGL-COM-PIS",
    },
    {
        # PGL-DNG.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-DNG.dat file
        "location": "PGL",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-DNG.dat to be written to this directory
        "output": "PGL-DNG",
    },
    {
        # PGL-ECS.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-ECS.dat file
        "location": "PGL",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-ECS.dat to be written to this directory
        "output": "PGL-ECS",
    },
    {
        # PGL-FPS.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-FPS.dat file
        "location": "PGL",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-FPS.dat to be written to this directory
        "output": "PGL-FPS",
    },
    {
        # PGL-LNE.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-LNE.dat file
        "location": "PGL",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-LNE.dat to be written to this directory
        "output": "PGL-LNE",
    },
    {
        # PGL-POW-DC.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-POW-DC.dat file
        "location": "PGL",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-POW-DC.dat to be written to this directory
        "output": "PGL-POW-DC",
    },
    {
        # PGL-POW-ETSB.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-POW-ETSB.dat file
        "location": "PGL",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-ETSB.dat to be written to this directory
        "output": "PGL-POW-ETSB",
    },
    {
        # PGL-POW-HV.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-POW-HV.dat file
        "location": "PGL",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-POW-HV.dat to be written to this directory
        "output": "PGL-POW-HV",
    },
    {
        # PGL-POW-LIG.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-POW-LIG.dat file
        "location": "PGL",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-POW-LIG.dat to be written to this directory
        "output": "PGL-POW-LIG",
    },
    {
        # PGL-POW-LV.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-POW-LV.dat file
        "location": "PGL",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-POW-LV.dat to be written to this directory
        "output": "PGL-POW-LV",
    },
    {
        # PGL-SIG.dat file from PGLSMS database
        "database": "PGL",  # xml_DB_PGL
        "environ": "PGLSMS",  # data written to PGL-SIG.dat file
        "location": "PGL",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "pglsms",  # PGL-SIG.dat to be written to this directory
        "output": "PGL-SIG",
    },
    #
    # PTP database
    #
    {
        # PTP-BMF.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-BMF.dat file
        "location": "PTP",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-BMF.dat to be written to this directory
        "output": "PTP-BMF",
    },
    {
        # PTP-COM-CCTV.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-COM-CCTV.dat file
        "location": "PTP",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-COM-CCTV.dat to be written to this directory
        "output": "PTP-COM-CCTV",
    },
    {
        # PTP-COM-PAS.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-COM-PAS.dat file
        "location": "PTP",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-COM-PAS.dat to be written to this directory
        "output": "PTP-COM-PAS",
    },
    {
        # PTP-COM-PIS.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-COM-PIS.dat file
        "location": "PTP",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-COM-PIS.dat to be written to this directory
        "output": "PTP-COM-PIS",
    },
    {
        # PTP-DNG.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-DNG.dat file
        "location": "PTP",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-DNG.dat to be written to this directory
        "output": "PTP-DNG",
    },
    {
        # PTP-ECS.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-ECS.dat file
        "location": "PTP",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-ECS.dat to be written to this directory
        "output": "PTP-ECS",
    },
    {
        # PTP-FPS.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-FPS.dat file
        "location": "PTP",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-FPS.dat to be written to this directory
        "output": "PTP-FPS",
    },
    {
        # PTP-LNE.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-LNE.dat file
        "location": "PTP",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-LNE.dat to be written to this directory
        "output": "PTP-LNE",
    },
    {
        # PTP-POW-DC.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-POW-DC.dat file
        "location": "PTP",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-POW-DC.dat to be written to this directory
        "output": "PTP-POW-DC",
    },
    {
        # PTP-POW-ETSB.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-POW-ETSB.dat file
        "location": "PTP",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-ETSB.dat to be written to this directory
        "output": "PTP-POW-ETSB",
    },
    {
        # PTP-POW-HV.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-POW-HV.dat file
        "location": "PTP",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-POW-HV.dat to be written to this directory
        "output": "PTP-POW-HV",
    },
    {
        # PTP-POW-LIG.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-POW-LIG.dat file
        "location": "PTP",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-POW-LIG.dat to be written to this directory
        "output": "PTP-POW-LIG",
    },
    {
        # PTP-POW-LV.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-POW-LV.dat file
        "location": "PTP",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-POW-LV.dat to be written to this directory
        "output": "PTP-POW-LV",
    },
    {
        # PTP-SIG.dat file from PTPSMS database
        "database": "PTP",  # xml_DB_PTP
        "environ": "PTPSMS",  # data written to PTP-SIG.dat file
        "location": "PTP",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "ptpsms",  # PTP-SIG.dat to be written to this directory
        "output": "PTP-SIG",
    },
    #
    # SER database
    #
    {
        # SER-BMF.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-BMF.dat file
        "location": "SER",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-BMF.dat to be written to this directory
        "output": "SER-BMF",
    },
    {
        # SER-COM-CCTV.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-COM-CCTV.dat file
        "location": "SER",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-COM-CCTV.dat to be written to this directory
        "output": "SER-COM-CCTV",
    },
    {
        # SER-COM-PAS.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-COM-PAS.dat file
        "location": "SER",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-COM-PAS.dat to be written to this directory
        "output": "SER-COM-PAS",
    },
    {
        # SER-COM-PIS.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-COM-PIS.dat file
        "location": "SER",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-COM-PIS.dat to be written to this directory
        "output": "SER-COM-PIS",
    },
    {
        # SER-DNG.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-DNG.dat file
        "location": "SER",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-DNG.dat to be written to this directory
        "output": "SER-DNG",
    },
    {
        # SER-ECS.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-ECS.dat file
        "location": "SER",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-ECS.dat to be written to this directory
        "output": "SER-ECS",
    },
    {
        # SER-FPS.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-FPS.dat file
        "location": "SER",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-FPS.dat to be written to this directory
        "output": "SER-FPS",
    },
    {
        # SER-LNE.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-LNE.dat file
        "location": "SER",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-LNE.dat to be written to this directory
        "output": "SER-LNE",
    },
    {
        # SER-POW-DC.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-POW-DC.dat file
        "location": "SER",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-POW-DC.dat to be written to this directory
        "output": "SER-POW-DC",
    },
    {
        # SER-POW-ETSB.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-POW-ETSB.dat file
        "location": "SER",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-ETSB.dat to be written to this directory
        "output": "SER-POW-ETSB",
    },
    {
        # SER-POW-HV.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-POW-HV.dat file
        "location": "SER",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-POW-HV.dat to be written to this directory
        "output": "SER-POW-HV",
    },
    {
        # SER-POW-LIG.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-POW-LIG.dat file
        "location": "SER",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-POW-LIG.dat to be written to this directory
        "output": "SER-POW-LIG",
    },
    {
        # SER-POW-LV.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-POW-LV.dat file
        "location": "SER",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-POW-LV.dat to be written to this directory
        "output": "SER-POW-LV",
    },
    {
        # SER-SIG.dat file from SERSMS database
        "database": "SER",  # xml_DB_SER
        "environ": "SERSMS",  # data written to SER-SIG.dat file
        "location": "SER",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "sersms",  # SER-SIG.dat to be written to this directory
        "output": "SER-SIG",
    },
    #
    # SKG database
    #
    {
        # SKG-BMF.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-BMF.dat file
        "location": "SKG",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-BMF.dat to be written to this directory
        "output": "SKG-BMF",
    },
    {
        # SKG-COM-CCTV.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-COM-CCTV.dat file
        "location": "SKG",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-COM-CCTV.dat to be written to this directory
        "output": "SKG-COM-CCTV",
    },
    {
        # SKG-COM-PAS.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-COM-PAS.dat file
        "location": "SKG",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-COM-PAS.dat to be written to this directory
        "output": "SKG-COM-PAS",
    },
    {
        # SKG-COM-PIS.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-COM-PIS.dat file
        "location": "SKG",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-COM-PIS.dat to be written to this directory
        "output": "SKG-COM-PIS",
    },
    {
        # SKG-DNG.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-DNG.dat file
        "location": "SKG",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-DNG.dat to be written to this directory
        "output": "SKG-DNG",
    },
    {
        # SKG-ECS.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-ECS.dat file
        "location": "SKG",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-ECS.dat to be written to this directory
        "output": "SKG-ECS",
    },
    {
        # SKG-FPS.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-FPS.dat file
        "location": "SKG",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-FPS.dat to be written to this directory
        "output": "SKG-FPS",
    },
    {
        # SKG-LNE.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-LNE.dat file
        "location": "SKG",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-LNE.dat to be written to this directory
        "output": "SKG-LNE",
    },
    {
        # SKG-POW-DC.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-POW-DC.dat file
        "location": "SKG",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-POW-DC.dat to be written to this directory
        "output": "SKG-POW-DC",
    },
    {
        # SKG-POW-ETSB.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-POW-ETSB.dat file
        "location": "SKG",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-ETSB.dat to be written to this directory
        "output": "SKG-POW-ETSB",
    },
    {
        # SKG-POW-HV.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-POW-HV.dat file
        "location": "SKG",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-POW-HV.dat to be written to this directory
        "output": "SKG-POW-HV",
    },
    {
        # SKG-POW-LIG.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-POW-LIG.dat file
        "location": "SKG",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-POW-LIG.dat to be written to this directory
        "output": "SKG-POW-LIG",
    },
    {
        # SKG-POW-LV.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-POW-LV.dat file
        "location": "SKG",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-POW-LV.dat to be written to this directory
        "output": "SKG-POW-LV",
    },
    {
        # SKG-SIG.dat file from SKGSMS database
        "database": "SKG",  # xml_DB_SKG
        "environ": "SKGSMS",  # data written to SKG-SIG.dat file
        "location": "SKG",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "skgsms",  # SKG-SIG.dat to be written to this directory
        "output": "SKG-SIG",
    },
    #
    # WLH database
    #
    {
        # WLH-BMF.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-BMF.dat file
        "location": "WLH",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-BMF.dat to be written to this directory
        "output": "WLH-BMF",
    },
    {
        # WLH-COM-CCTV.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-COM-CCTV.dat file
        "location": "WLH",
        "system": "CCTS_0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-COM-CCTV.dat to be written to this directory
        "output": "WLH-COM-CCTV",
    },
    {
        # WLH-COM-PAS.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-COM-PAS.dat file
        "location": "WLH",
        "system": "PASS_0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-COM-PAS.dat to be written to this directory
        "output": "WLH-COM-PAS",
    },
    {
        # WLH-COM-PIS.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-COM-PIS.dat file
        "location": "WLH",
        "system": "PISS_0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-COM-PIS.dat to be written to this directory
        "output": "WLH-COM-PIS",
    },
    {
        # WLH-DNG.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-DNG.dat file
        "location": "WLH",
        "system": "DNG__0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-DNG.dat to be written to this directory
        "output": "WLH-DNG",
    },
    {
        # WLH-ECS.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-ECS.dat file
        "location": "WLH",
        "system": "ECS",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-ECS.dat to be written to this directory
        "output": "WLH-ECS",
    },
    {
        # WLH-FPS.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-FPS.dat file
        "location": "WLH",
        "system": "FPS__0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-FPS.dat to be written to this directory
        "output": "WLH-FPS",
    },
    {
        # WLH-LNE.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-LNE.dat file
        "location": "WLH",
        "system": "LNE__0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-LNE.dat to be written to this directory
        "output": "WLH-LNE",
    },
    {
        # WLH-POW-DC.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-POW-DC.dat file
        "location": "WLH",
        "system": "DC___0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-POW-DC.dat to be written to this directory
        "output": "WLH-POW-DC",
    },
    {
        # WLH-POW-ETSB.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-POW-ETSB.dat file
        "location": "WLH",
        "system": "ETSB_0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-ETSB.dat to be written to this directory
        "output": "WLH-POW-ETSB",
    },
    {
        # WLH-POW-HV.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-POW-HV.dat file
        "location": "WLH",
        "system": "HV___0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-POW-HV.dat to be written to this directory
        "output": "WLH-POW-HV",
    },
    {
        # WLH-POW-LIG.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-POW-LIG.dat file
        "location": "WLH",
        "system": "LIG__0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-POW-LIG.dat to be written to this directory
        "output": "WLH-POW-LIG",
    },
    {
        # WLH-POW-LV.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-POW-LV.dat file
        "location": "WLH",
        "system": "LV___0001",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-POW-LV.dat to be written to this directory
        "output": "WLH-POW-LV",
    },
    {
        # WLH-SIG.dat file from WLHSMS database
        "database": "WLH",  # xml_DB_WLH
        "environ": "WLHSMS",  # data written to WLH-SIG.dat file
        "location": "WLH",
        "system": "TRAS",  # search for BMF in the xml file
        "output_dir": "wlhsms",  # WLH-SIG.dat to be written to this directory
        "output": "WLH-SIG",
    },
    #
    # NED database
    #
    {
        # NED-BMF.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NED-BMF.dat file
        "location": "NED",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "nedsms",  # NED-BMF.dat to be written to this directory
        "output": "NED-BMF",
    },
    {
        # NED-COM-CCTV.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NED-COM-CCTV.dat file
        "location": "NED",
        "system": "CCTS_0001",  # search for CCTS_0001 in the xml file
        "output_dir": "nedsms",  # NED-COM-CCTV.dat to be written to this directory
        "output": "NED-COM-CCTV",
    },
    {
        # NED-COM-PAS.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NED-COM-PAS.dat file
        "location": "NED",
        "system": "PASS_0001",  # search for PASS_0001 in the xml file
        "output_dir": "nedsms",  # NED-COM-PAS.dat to be written to this directory
        "output": "NED-COM-PAS",
    },
    {
        # NED-FPS.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NED-FPS.dat file
        "location": "NED",
        "system": "FPSD_0001",  # search for FPSD_0001 in the xml file
        "output_dir": "nedsms",  # NED-FPS.dat to be written to this directory
        "output": "NED-FPS",
    },
    {
        # NED-SIG.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NED-SIG.dat file
        "location": "NED",
        "system": "TRAD",  # search for TRAD in the xml file
        "output_dir": "nedsms",  # NED-SIG.dat to be written to this directory
        "output": "NED-SIG",
    },
    {
        # NED-AMS.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NED-AMS.dat file
        "location": "NED",
        "system": "AMS__0001",  # search for AMS__0001 in the xml file
        "output_dir": "nedsms",  # NED-AMS.dat to be written to this directory
        "output": "NED-AMS",
    },
    {
        # NDI-POW-DC.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NDI-POW-DC.dat file
        "location": "NDI",
        "system": "DC___0001",  # search for DC___0001 in the xml file
        "output_dir": "nedsms",  # NDI-POW-DC.dat to be written to this directory
        "output": "NDI-POW-DC",
    },
    {
        # NDI-POW-HV.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NDI-POW-HV.dat file
        "location": "NDI",
        "system": "HV___0001",  # search for HV___0001 in the xml file
        "output_dir": "nedsms",  # NDI-POW-HV.dat to be written to this directory
        "output": "NDI-POW-HV",
    },
    {
        # NPS-POW-HV.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NPS-POW-HV.dat file
        "location": "NPS",
        "system": "HV___0001",  # search for HV___0001 in the xml file
        "output_dir": "nedsms",  # NPS-POW-HV.dat to be written to this directory
        "output": "NPS-POW-HV",
    },
    {
        # NTS-POW-DC.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NPS-POW-DC.dat file
        "location": "NTS",
        "system": "DC___0001",  # search for DC___0001 in the xml file
        "output_dir": "nedsms",  # NTS-POW-DC.dat to be written to this directory
        "output": "NTS-POW-DC",
    },
    {
        # NTS-POW-HV.dat file from NEDSMS database
        "database": "NED",  # xml_DB_NED
        "environ": "NEDSMS",  # data written to NTS-POW-DC.dat file
        "location": "NTS",
        "system": "HV___0001",  # search for HV___0001 in the xml file
        "output_dir": "nedsms",  # NTS-POW-HV.dat to be written to this directory
        "output": "NTS-POW-HV",
    },
    #
    # ATS database
    #
    # BGK
    {
        # BGK-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to BGK-SIG.dat file
        "location": "BGK",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # BGK-SIG.dat to be written to this directory
        "output": "BGK-SIG",
    },
    # BNK
    {
        # BNK-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to BNK-SIG.dat file
        "location": "BNK",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # BNK-SIG.dat to be written to this directory
        "output": "BNK-SIG",
    },
    # CNT
    {
        # CNT-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to CNT-SIG.dat file
        "location": "CNT",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # CNT-SIG.dat to be written to this directory
        "output": "CNT-SIG",
    },
    # CQY
    {
        # CQY-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to CQY-SIG.dat file
        "location": "CQY",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # CQY-SIG.dat to be written to this directory
        "output": "CQY-SIG",
    },
    # DBG
    {
        # DBG-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to DBG-SIG.dat file
        "location": "DBG",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # DBG-SIG.dat to be written to this directory
        "output": "DBG-SIG",
    },
    # FRP
    {
        # FRP-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to FRP-SIG.dat file
        "location": "FRP",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # FRP-SIG.dat to be written to this directory
        "output": "FRP-SIG",
    },
    # HBF
    {
        # HBF-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to HBF-SIG.dat file
        "location": "HBF",
        "system": "TRAT",  # search for TRAT in the xml file
        "output_dir": "occats",  # HBF-SIG.dat to be written to this directory
        "output": "HBF-SIG",
    },
    # HGN
    {
        # HGN-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to HGN-SIG.dat file
        "location": "HGN",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # HGN-SIG.dat to be written to this directory
        "output": "HGN-SIG",
    },
    # KVN
    {
        # KVN-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to KVN-SIG.dat file
        "location": "KVN",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # KVN-SIG.dat to be written to this directory
        "output": "KVN-SIG",
    },
    # LTI
    {
        # LTI-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to LTI-SIG.dat file
        "location": "LTI",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # LTI-SIG.dat to be written to this directory
        "output": "LTI-SIG",
    },
    # OTP
    {
        # OTP-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to OTP-SIG.dat file
        "location": "OTP",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # OTP-SIG.dat to be written to this directory
        "output": "OTP-SIG",
    },
    # PGC
    {
        # PGC-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to PGC-SIG.dat file
        "location": "PGC",
        "system": "TRAT",  # search for TRAT in the xml file
        "output_dir": "occats",  # PGC-SIG.dat to be written to this directory
        "output": "PGC-SIG",
    },
    # PGL
    {
        # PGL-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to PGL-SIG.dat file
        "location": "PGL",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # PGL-SIG.dat to be written to this directory
        "output": "PGL-SIG",
    },
    # PTP
    {
        # PTP-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to PTP-SIG.dat file
        "location": "PTP",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # PTP-SIG.dat to be written to this directory
        "output": "PTP-SIG",
    },
    # SER
    {
        # SER-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to SER-SIG.dat file
        "location": "SER",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # SER-SIG.dat to be written to this directory
        "output": "SER-SIG",
    },
    # SKG
    {
        # SKG-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to SKG-SIG.dat file
        "location": "SKG",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # SKG-SIG.dat to be written to this directory
        "output": "SKG-SIG",
    },
    # WLH
    {
        # WLH-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to WLH-SIG.dat file
        "location": "WLH",
        "system": "TRAS",  # search for TRAS in the xml file
        "output_dir": "occats",  # WLH-SIG.dat to be written to this directory
        "output": "WLH-SIG",
    },
    # NED
    {
        # NED-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to WLH-SIG.dat file
        "location": "NED",
        "system": "TRAD",  # search for TRAS in the xml file
        "output_dir": "occats",  # WLH-SIG.dat to be written to this directory
        "output": "NED-SIG",
    },
    # OCC
    {
        # OCC-SIG.dat file from OCCATS database
        "database": "ATS",  # xml_DB_ATS
        "environ": "OCCATS",  # data written to WLH-SIG.dat file
        "location": "OCC",
        "system": "BMF",  # search for TRAS in the xml file
        "output_dir": "occats",  # WLH-SIG.dat to be written to this directory
        "output": "OCC-BMF",
    },
    #
    # CMS database
    #
    # BGK
    {
        # BGK-BMF.dat file from OCCCMS database
        "database": "CMS",  # xml_DB_CMS
        "environ": "OCCCMS",  # data written to BGK-BMF.dat file
        "location": "BGK",
        "system": "BMF",  # search for BMF in the xml file
        "output_dir": "occcms",  # BGK-BMF.dat to be written to this directory
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
    # BNK
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
    # CNT
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
    # CQY
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
    # DBG
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
    # FRP
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
    # HBF
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
    # HGN
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
    # KVN
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
    # LTI
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
    # OTP
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
    # PGC
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
    # PGL
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
    # PTP
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
    # SER
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
    # SKG
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
    # WLH
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
    # NEL Depot
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
    # CMS
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
    #
    # ECS database
    #
    # BGK
    {
        # BGK-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "BGKSMS",  # data written to BGK-ECS.dat file
        "location": "BGK",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # BGK-ECS.dat to be written to this directory
        "output": "BGK-ECS",
    },
    {
        # BGK-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "BGKSMS",  # data written to BGK-FPS.dat file
        "location": "BGK",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # BGK-FPS.dat to be written to this directory
        "output": "BGK-FPS",
    },
    {
        # BGK-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "BGKSMS",  # data written to BGK-ECS.dat file
        "location": "BGK",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # BGK-LNE.dat to be written to this directory
        "output": "BGK-LNE",
    },
    # BNK
    {
        # BNK-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "BNKSMS",  # data written to BNK-ECS.dat file
        "location": "BNK",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # BNK-ECS.dat to be written to this directory
        "output": "BNK-ECS",
    },
    {
        # BNK-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "BNKSMS",  # data written to BNK-FPS.dat file
        "location": "BNK",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # BNK-FPS.dat to be written to this directory
        "output": "BNK-FPS",
    },
    {
        # BNK-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "BNKSMS",  # data written to BNK-ECS.dat file
        "location": "BNK",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # BNK-LNE.dat to be written to this directory
        "output": "BNK-LNE",
    },
    # CNT
    {
        # CNT-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "CNTSMS",  # data written to CNT-ECS.dat file
        "location": "CNT",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # CNT-ECS.dat to be written to this directory
        "output": "CNT-ECS",
    },
    {
        # CNT-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "CNTSMS",  # data written to CNT-FPS.dat file
        "location": "CNT",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # CNT-FPS.dat to be written to this directory
        "output": "CNT-FPS",
    },
    {
        # CNT-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "CNTSMS",  # data written to CNT-ECS.dat file
        "location": "CNT",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # CNT-LNE.dat to be written to this directory
        "output": "CNT-LNE",
    },
    # CQY
    {
        # CQY-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "CQYSMS",  # data written to CQY-ECS.dat file
        "location": "CQY",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # CQY-ECS.dat to be written to this directory
        "output": "CQY-ECS",
    },
    {
        # CQY-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "CQYSMS",  # data written to CQY-FPS.dat file
        "location": "CQY",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # CQY-FPS.dat to be written to this directory
        "output": "CQY-FPS",
    },
    {
        # CQY-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "CQYSMS",  # data written to CQY-ECS.dat file
        "location": "CQY",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # CQY-LNE.dat to be written to this directory
        "output": "CQY-LNE",
    },
    # DBG
    {
        # DBG-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "DBGSMS",  # data written to DBG-ECS.dat file
        "location": "DBG",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # DBG-ECS.dat to be written to this directory
        "output": "DBG-ECS",
    },
    {
        # DBG-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "DBGSMS",  # data written to DBG-FPS.dat file
        "location": "DBG",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # DBG-FPS.dat to be written to this directory
        "output": "DBG-FPS",
    },
    {
        # DBG-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "DBGSMS",  # data written to DBG-ECS.dat file
        "location": "DBG",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # DBG-LNE.dat to be written to this directory
        "output": "DBG-LNE",
    },
    # FRP
    {
        # FRP-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "FRPSMS",  # data written to FRP-ECS.dat file
        "location": "FRP",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # FRP-ECS.dat to be written to this directory
        "output": "FRP-ECS",
    },
    {
        # FRP-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "FRPSMS",  # data written to FRP-FPS.dat file
        "location": "FRP",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # FRP-FPS.dat to be written to this directory
        "output": "FRP-FPS",
    },
    {
        # FRP-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "FRPSMS",  # data written to FRP-ECS.dat file
        "location": "FRP",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # FRP-LNE.dat to be written to this directory
        "output": "FRP-LNE",
    },
    # HBF
    {
        # HBF-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "HBFSMS",  # data written to HBF-ECS.dat file
        "location": "HBF",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # HBF-ECS.dat to be written to this directory
        "output": "HBF-ECS",
    },
    {
        # HBF-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "HBFSMS",  # data written to HBF-FPS.dat file
        "location": "HBF",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # HBF-FPS.dat to be written to this directory
        "output": "HBF-FPS",
    },
    {
        # HBF-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "HBFSMS",  # data written to HBF-ECS.dat file
        "location": "HBF",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # HBF-LNE.dat to be written to this directory
        "output": "HBF-LNE",
    },
    # HGN
    {
        # HGN-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "HGNSMS",  # data written to HGN-ECS.dat file
        "location": "HGN",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # HGN-ECS.dat to be written to this directory
        "output": "HGN-ECS",
    },
    {
        # HGN-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "HGNSMS",  # data written to HGN-FPS.dat file
        "location": "HGN",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # HGN-FPS.dat to be written to this directory
        "output": "HGN-FPS",
    },
    {
        # HGN-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "HGNSMS",  # data written to HGN-ECS.dat file
        "location": "HGN",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # HGN-LNE.dat to be written to this directory
        "output": "HGN-LNE",
    },
    # KVN
    {
        # KVN-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "KVNSMS",  # data written to KVN-ECS.dat file
        "location": "KVN",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # KVN-ECS.dat to be written to this directory
        "output": "KVN-ECS",
    },
    {
        # KVN-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "KVNSMS",  # data written to KVN-FPS.dat file
        "location": "KVN",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # KVN-FPS.dat to be written to this directory
        "output": "KVN-FPS",
    },
    {
        # KVN-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "KVNSMS",  # data written to KVN-ECS.dat file
        "location": "KVN",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # KVN-LNE.dat to be written to this directory
        "output": "KVN-LNE",
    },
    # LTI
    {
        # LTI-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "LTISMS",  # data written to LTI-ECS.dat file
        "location": "LTI",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # LTI-ECS.dat to be written to this directory
        "output": "LTI-ECS",
    },
    {
        # LTI-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "LTISMS",  # data written to LTI-FPS.dat file
        "location": "LTI",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # LTI-FPS.dat to be written to this directory
        "output": "LTI-FPS",
    },
    {
        # LTI-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "LTISMS",  # data written to LTI-ECS.dat file
        "location": "LTI",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # LTI-LNE.dat to be written to this directory
        "output": "LTI-LNE",
    },
    # OTP
    {
        # OTP-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "OTPSMS",  # data written to OTP-ECS.dat file
        "location": "OTP",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # OTP-ECS.dat to be written to this directory
        "output": "OTP-ECS",
    },
    {
        # OTP-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "OTPSMS",  # data written to OTP-FPS.dat file
        "location": "OTP",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # OTP-FPS.dat to be written to this directory
        "output": "OTP-FPS",
    },
    {
        # OTP-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "OTPSMS",  # data written to OTP-ECS.dat file
        "location": "OTP",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # OTP-LNE.dat to be written to this directory
        "output": "OTP-LNE",
    },
    # PGC
    {
        # PGC-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PGCSMS",  # data written to PGC-ECS.dat file
        "location": "PGC",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # PGC-ECS.dat to be written to this directory
        "output": "PGC-ECS",
    },
    {
        # PGC-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PGCSMS",  # data written to PGC-FPS.dat file
        "location": "PGC",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # PGC-FPS.dat to be written to this directory
        "output": "PGC-FPS",
    },
    {
        # PGC-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PGCSMS",  # data written to PGC-ECS.dat file
        "location": "PGC",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # PGC-LNE.dat to be written to this directory
        "output": "PGC-LNE",
    },
    # PGL
    {
        # PGL-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PGLSMS",  # data written to PGL-ECS.dat file
        "location": "PGL",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # PGL-ECS.dat to be written to this directory
        "output": "PGL-ECS",
    },
    {
        # PGL-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PGLSMS",  # data written to PGL-FPS.dat file
        "location": "PGL",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # PGL-FPS.dat to be written to this directory
        "output": "PGL-FPS",
    },
    {
        # PGL-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PGLSMS",  # data written to PGL-ECS.dat file
        "location": "PGL",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # PGL-LNE.dat to be written to this directory
        "output": "PGL-LNE",
    },
    # PTP
    {
        # PTP-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PTPSMS",  # data written to PTP-ECS.dat file
        "location": "PTP",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # PTP-ECS.dat to be written to this directory
        "output": "PTP-ECS",
    },
    {
        # PTP-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PTPSMS",  # data written to PTP-FPS.dat file
        "location": "PTP",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # PTP-FPS.dat to be written to this directory
        "output": "PTP-FPS",
    },
    {
        # PTP-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "PTPSMS",  # data written to PTP-ECS.dat file
        "location": "PTP",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # PTP-LNE.dat to be written to this directory
        "output": "PTP-LNE",
    },
    # SER
    {
        # SER-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "SERSMS",  # data written to SER-ECS.dat file
        "location": "SER",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # SER-ECS.dat to be written to this directory
        "output": "SER-ECS",
    },
    {
        # SER-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "SERSMS",  # data written to SER-FPS.dat file
        "location": "SER",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # SER-FPS.dat to be written to this directory
        "output": "SER-FPS",
    },
    {
        # SER-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "SERSMS",  # data written to SER-ECS.dat file
        "location": "SER",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # SER-LNE.dat to be written to this directory
        "output": "SER-LNE",
    },
    # SKG
    {
        # SKG-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "SKGSMS",  # data written to SKG-ECS.dat file
        "location": "SKG",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # SKG-ECS.dat to be written to this directory
        "output": "SKG-ECS",
    },
    {
        # SKG-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "SKGSMS",  # data written to SKG-FPS.dat file
        "location": "SKG",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # SKG-FPS.dat to be written to this directory
        "output": "SKG-FPS",
    },
    {
        # SKG-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "SKGSMS",  # data written to SKG-ECS.dat file
        "location": "SKG",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # SKG-LNE.dat to be written to this directory
        "output": "SKG-LNE",
    },
    # WLH
    {
        # WLH-ECS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "WLHSMS",  # data written to WLH-ECS.dat file
        "location": "WLH",
        "system": "ECS",  # search for ECS in the xml file
        "output_dir": "occecs",  # WLH-ECS.dat to be written to this directory
        "output": "WLH-ECS",
    },
    {
        # WLH-FPS.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "WLHSMS",  # data written to WLH-FPS.dat file
        "location": "WLH",
        "system": "FPS__0001",  # search for FPS__0001 in the xml file
        "output_dir": "occecs",  # WLH-FPS.dat to be written to this directory
        "output": "WLH-FPS",
    },
    {
        # WLH-LNE.dat file from OCCECS database
        "database": "ECS",  # xml_DB_ECS
        "environ": "WLHSMS",  # data written to WLH-ECS.dat file
        "location": "WLH",
        "system": "LNE__0001",  # search for LNE__0001 in the xml file
        "output_dir": "occecs",  # WLH-LNE.dat to be written to this directory
        "output": "WLH-LNE",
    },
]

_environments = [
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
    "OTP",
    "PGC",
    "PGL",
    "PTP",
    "SER",
    "SKG",
    "WLH",
    "NED",
    "ATS",
    "CMS",
    "ECS",
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


def is_valid_environ(environ):
    """
    Returns True when a given environment is a valid environment
    """
    return environ.upper() in _environments


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
    timestamp = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    header = f"""###########################################################
#  /home/dbs/SumReport/{environ}/{os.path.basename(ssr_dat)}                 #
#  Status Summary Report configuration file               #
#  generated automatically on {timestamp}        #
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
        "--pool",
        "-p",
        required=False,
        type=int,
        default=1,
        dest="pool",
        help="number of worker processes to be used (default=1)",
    )
    parser.add_argument(
        "--environment",
        "-e",
        required=False,
        default="",
        dest="environment",
        help="specific environment to be processed (e.g., CMS)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        dest="output_dir",
        help="path to output directory",
    )

    args = parser.parse_args()

    databases = _databases
    if args.environment != "":
        if not is_valid_environ(args.environment):
            logging.error(f"{args.environment} is not a valid environment")
            return
        databases = [db for db in _databases if db.get("database") == args.environment]

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

    # # FIXME Under macOS, for some reasons, logger does not output anything while performing the jobs via pool
    pool = multiprocessing.Pool(args.pool)
    [pool.apply_async(do_work, [args.xml_dir, args.output_dir, db]) for db in databases]
    pool.close()
    pool.join()

    end = time.perf_counter()
    logging.info(f"Total processing time: {end - start:0.4f} seconds")


if __name__ == "__main__":
    main()

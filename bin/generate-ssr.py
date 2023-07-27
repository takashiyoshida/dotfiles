#!/usr/bin/env python

import argparse
import locale
from functools import cmp_to_key
import logging
import logging.handlers
import os.path
import sys
import xml.etree.ElementTree as ET


sms_mapping = {
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

bgk_mapping = {
    "BGK": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

bnk_mapping = {
    "BNK": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

cnt_mapping = {
    "CNT": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

cqy_mapping = {
    "CQY": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

dbg_mapping = {
    "DBG": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

frp_mapping = {
    "FRP": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

hbf_mapping = {
    "HBF": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAT", "filename": "SIG"},
    ],
}

hgn_mapping = {
    "HGN": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

kvn_mapping = {
    "KVN": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

lti_mapping = {
    "LTI": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

otp_mapping = {
    "OTP": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

pgc_mapping = {
    "PGC": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAT", "filename": "SIG"},
    ],
}

pgl_mapping = {
    "PGL": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

ptp_mapping = {
    "PTP": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

ser_mapping = {
    "SER": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

skg_mapping = {
    "SKG": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

wlh_mapping = {
    "WLH": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
        {"node": "DNG__0001", "filename": "DNG"},
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "ETSB_0001", "filename": "POW-ETSB"},
        {"node": "HV___0001", "filename": "POW-HV"},
        {"node": "LIG__0001", "filename": "POW-LIG"},
        {"node": "LV___0001", "filename": "POW-LV"},
        {"node": "TRAS", "filename": "SIG"},
    ],
}

ned_mapping = {
    "NED": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "FPSD_0001", "filename": "FPS"},
        {"node": "TRAD", "filename": "SIG"},
        {"node": "AMS", "filename": "AMS"},
    ],
    # The following files do not require NED prefix in names
    "NDI": [
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "HV___0001", "filename": "POW-HV"},
    ],
    "NPS": [
        {"node": "HV___0001", "filename": "POW-HV"},
    ],
    "NTS": [
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "HV___0001", "filename": "POW-HV"},
    ],
}

ats_mapping = {
    "BGK": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "BNK": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "CNT": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "CQY": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "DBG": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "FRP": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "HBF": [
        {"node": "TRAT", "filename": "SIG"},
    ],
    "HGN": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "KVN": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "LTI": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "OTP": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "PGC": [
        {"node": "TRAT", "filename": "SIG"},
    ],
    "PGL": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "PTP": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "SER": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "SKG": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    "WLH": [
        {"node": "TRAS", "filename": "SIG"},
    ],
    # FIXME NED does not generate the _same_ set of data
    "NED": [
        {"node": "TRAD", "filename": "SIG"},
    ],
}

cms_mapping = {
    "BGK": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "BNK": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "CNT": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "CQY": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "DBG": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "FRP": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "HBF": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "HGN": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "KVN": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "LTI": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "NED": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
    ],
    "OTP": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "PGC": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "PGL": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "PTP": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "SER": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "SKG": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "WLH": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "OCC": [
        {"node": "BMF", "filename": "BMF"},
        {"node": "CCTS_0001", "filename": "COM-CCTV"},
        {"node": "PASS_0001", "filename": "COM-PAS"},
        {"node": "PISS_0001", "filename": "COM-PIS"},
    ],
    "NDI": [
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "HV___0001", "filename": "POW-HV"},
    ],
    "NPS": [
        {"node": "HV___0001", "filename": "POW-HV"},
    ],
    "NTS": [
        {"node": "DC___0001", "filename": "POW-DC"},
        {"node": "HV___0001", "filename": "POW-HV"},
    ],
}

ecs_mapping = {
    "BGK": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "BNK": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "CNT": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "CQY": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "DBG": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "FRP": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "HBF": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "HGN": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "KVN": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "LTI": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "OTP": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "PGC": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "PGL": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "PTP": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "SER": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "SKG": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
    "WLH": [
        {"node": "ECS", "filename": "ECS"},
        {"node": "FPS__0001", "filename": "FPS"},
        {"node": "LNE__0001", "filename": "LNE"},
    ],
}

database_list = {
    "BGK": bgk_mapping,
    "BNK": bnk_mapping,
    "CNT": cnt_mapping,
    "CQY": cqy_mapping,
    "DBG": dbg_mapping,
    "FRP": frp_mapping,
    # HBF station is a terminus station and requires different SIG data
    "HBF": hbf_mapping,
    "HGN": hgn_mapping,
    "KVN": kvn_mapping,
    "LTI": lti_mapping,
    "NED": ned_mapping,
    "OTP": otp_mapping,
    # PGC station is a terminus station and requires different SIG data
    "PGC": pgc_mapping,
    "PGL": pgl_mapping,
    "PTP": ptp_mapping,
    "SER": ser_mapping,
    "SKG": skg_mapping,
    "WLH": wlh_mapping,
    "ATS": ats_mapping,
    "CMS": cms_mapping,
    "ECS": ecs_mapping,
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
    "trp",
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


def validate_database(database):
    """
    Returns True if a given database is a member of database list
    """
    return database in database_list


def validate_swc(swc):
    """
    Returns True if a given environment is a member of SWC mapping list
    """
    return swc in sms_mapping


def get_swc_node(swc):
    """
    Returns a node text to search for
    """
    data = hbf_mapping.get(swc)
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


def get_swc_outfile(environ, filename, output_dir):
    """
    Returns an output filename, given an environment and a SWC (e.g., BNK-BMF.dat)
    """
    return f"{output_dir}/{environ}-{filename}.dat"


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


def write_ssr(database, points, filename):
    """
    Writes SSR for GWS
    """
    logging.info(f"  >> Writing database points to {os.path.basename(filename)} ...")
    with open(filename, "w") as outfile:
        # SSR file still needs comments at the top of the file
        # ENVIRONEMENT needs six-letter environment name (e.g., BNKSMS)
        database = set_environment_name(database)
        outfile.write(f"ENVIRONEMENT={database}\n")
        outfile.write("CONFIGURATION=\n")

        for p in points:
            logging.debug(f"POINT=<alias>{p}")
            outfile.write(f"POINT=<alias>{p}\n")
        logging.info(
            f"  >> No. of database points written to {os.path.basename(filename)}: {len(points)}"
        )


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
        "--database",
        "-d",
        required=True,
        dest="database",
        help=f"valid database is one of {sorted(database_list)}",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        dest="output_dir",
        help="path to output directory of SSR file",
    )

    locale.setlocale(locale.LC_ALL, ("en_US", "UTF-8"))

    args = parser.parse_args()
    logging.debug(f"Given arguments: {args}")

    # args.database = args.database.upper()

    if not validate_database(args.database):
        logging.error(f"Invalid environment, {args.database}.")
        logging.error(f"Valid environment is one of {sorted(database_list)}.")
        sys.exit(1)

    if not validate_output_dir(args.output_dir):
        logging.error(f"{args.output_dir} does not exist.")
        sys.exit(1)

    root = ET.parse(args.xmlFile)
    dataset = database_list.get(f"{args.database}")

    for environ in dataset.keys():
        logging.info(f"Extracting database points for {environ} ...")
        for item in dataset.get(environ):
            node = item.get("node")
            filename = item.get("filename")
            outfile = get_swc_outfile(environ, filename, args.output_dir)
            logging.info(f"Searching for database points under {node} ...")

            prefix = ""
            points = []

            result = root.findall(
                f".//HierarchyItem[@name='{environ}']//HierarchyItem[@name='{node}']//HierarchyItem"
            )
            for foo in result:
                alias = foo.get("alias")
                name = foo.get("name")

                if alias == f"{environ}_{name}":
                    continue

                if not ignore_name(name):
                    parent = root.findall(f".//HierarchyItem[@alias='{alias}']/..")
                    if len(parent) == 1:
                        prefix = parent[0].get("alias")
                        points.append(f"{prefix}:{name}")
                    else:
                        logging.warn(f"Unexpected number of parents for alias {alias}")

            if len(points) > 0:
                points.sort(key=cmp_to_key(locale.strcoll))
                write_ssr(environ, points, outfile)
            else:
                logging.error(
                    f"No database points were discovered for {environ} {node}"
                )
            logging.info("")


if __name__ == "__main__":
    main()

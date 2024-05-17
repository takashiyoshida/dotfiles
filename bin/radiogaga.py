#!/usr/bin/env python

import argparse
import csv
import logging
import logging.handlers
import re
import struct

# DD/MM HH:mm:ss
TIMESTAMP = r'[0-3][0-9]\/[01][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
METHOD_EVENT = r'Method = [\da-f]+|Event = [\da-f]+'

# Ignore the second timestamp
HEADER = r'^(?P<timestamp>{}) \(.+\) \[.+\] Length = (?P<length>\d+); SessRef = (?P<session>\-?\d+); TransId = (?P<trans_id>\d+); Status = (?P<status>\-?\d+); (?P<method>{}); Param ='.format(
    TIMESTAMP, METHOD_EVENT)

# Hexadecimal data, separated from ASCII representation by at least three spaces
DATA = r'\s{3,}'

# API Identifiers defined in Appendix C.10 of RCS IDD
# However, unlike the IDD, I separate the API identifiers with underscores
# to improve readability.
METHODS_EVENTS = {
    0x2: 'ATTACH_SESSION',  # 2
    0x3: 'DETACH_SESSION',  # 3
    0x4: 'REQUEST_VERSION',  # 4
    0x5: 'INITIALISE',  # 5
    0x6: 'SET_SYSTEM_ERROR_THRESHOLD',  # 6
    0x7: 'LOGIN',  # 7
    0x8: 'LOGOUT',  # 8
    0x9: 'CHANGE_PASSWORD',  # 9
    0xa: 'QUERY_REFERENCE',  # 10
    0xb: 'CHANGE_REFERENCE',  # 11
    0xc: 'SEARCH_SUBSCRIBER',  # 12
    0xd: 'NEW_REFERENCE',  # 13
    0xe: 'TEXT2SR',  # 14
    0xf: 'DELETE_REFERENCE',  # 15
    0x10: 'DELETE_SUBSCRIBER',  # 16
    0x11: 'SELECT',  # 17
    0x12: 'DESELECT',  # 18
    0x13: 'DEMAND_TX',  # 19
    0x14: 'CEASE_TX',  # 20
    0x15: 'SETUP_CALL',  # 21
    0x16: 'ANSWER_CALL',  # 22
    0x17: 'DISCONNECT',  # 23
    0x18: 'SEND_SDS',  # 24
    0x19: 'ATTACH_AUDIO',  # 25
    0x1a: 'DETACH_AUDIO',  # 26
    0x1b: 'MONITOR_SUBSCRIBER',  # 27
    0x1c: 'FORCE_CALL_TERMINATION',  # 28
    0x1d: 'MONITOR_CALL',  # 29
    0x20: 'INCLUDE',  # 32
    0x21: 'AUTHORISE_CALL',  # 33
    0x23: 'GET_GROUP_DETAILS',  # 35
    0x26: 'CONVERT_TO_DBTIME',  # 38
    0x27: 'ATTACH_TO_GROUP',  # 39
    0x28: 'DETATCH_FROM_GROUP',  # 40
    0x29: 'SEND_CIRCUIT_DATA',  # 41
    0x30: 'TEXT_TO_REFERENCE',  # 48
    0x32: 'ATTACH_MONITOR_AUDIO',  # 50
    0x33: 'JOIN',  # 51
    0x34: 'DETACH_MONITOR_AUDIO',  # 52
    0x65: 'GET_ACTIVE_ALARM_LIST',  # 101
    0x8343: 'EVENT_SC_ACTIVE_ALARM',  # 33603
    0xa000: 'EVENT_SYSTEM_ERROR',  # 40960
    0xa001: 'EVENT_INCOMING_CALL',  # 40961
    0xa002: 'EVENT_INCOMING_SDS',  # 40962
    0xa003: 'EVENT_CALL_STATUS',  # 40963
    0xa004: 'EVENT_SUBSCRIBER_ACTIVITY',  # 40964
    0xa005: 'EVENT_INCOMING_CIRCUIT_DATA',  # 40965
    0xa006: 'EVENT_CIRCUIT_DATA_CAPACITY',  # 40966
    0xa009: 'EVENT_REQUEST_AUTHORISE_CALL',  # 40969
    0xa00a: 'EVENT_GROUP_CALL_ACK',  # 40970
    0xa00e: 'EVENT_DGNA_CREATED',  # 40974
    0xa00f: 'EVENT_DGNA_DELETED',  # 40975
}

COMMANDS = {
    0x1: 'Carrier On',  # 1
    0x2: 'Carrier Off',  # 2
    0x3: 'Quad Screen',  # 3
    0x4: 'Single Screen',  # 4
    0x5: 'Sequence',  # 5
    0x6: 'Return to Default',  # 6
    0x7: 'command',  # 7
    0x8: 'command',  # 8
    0x9: 'Command Received',  # 9
    0xa: 'Frequency Change',  # 10
    0xb: 'PA Live Announcement',  # 11
    0xc: 'Pre-Recorded Announcement',  # 12
    0xd: 'DVA Announcement',  # 13
    0xe: 'PA Reset',  # 14
    0xf: 'Request for ATAS Version (1)',  # 15
    0x10: 'ATAS Library Enable (1)',  # 16
    0x11: 'ATAS Library Disable (1)',  # 17
    0x12: 'PA Continue',  # 18
    0x13: 'PA Command Received',  # 19
    0x14: 'Ready for Live/DVA Announcement',  # 20
    0x15: 'ATAS Version Number',  # 21
    0x16: 'Request for PA Reset',  # 22
    0x17: 'Audio SW on PA',  # 23
    0x18: 'Train PA Message Completed',  # 24
    0x19: 'ATAS Cyclic Announcement',  # 25
    0x1a: 'Audio SW on Cab to Cab',  # 26
    0x1b: 'command',  # 27
    0x1c: 'command',  # 28
    0x1d: 'command',  # 29
    0x1e: 'command',  # 30
    0x1f: 'PIS Free-Text Message',  # 31
    0x20: 'PIS Pre-Stored Message',  # 32
    0x21: 'PIS Library Download',  # 33
    0x22: 'PIS Library Upload (1)',  # 34
    0x23: 'Reset Emergency Message',  # 35
    0x24: 'Request for PIS Version (1)',  # 36
    0x25: 'PIS Library Enable (1)',  # 37
    0x26: 'PIS Library Disable (1)',  # 38
    0x27: 'End of PIS Download',  # 39
    0x28: 'command',  # 40
    0x29: 'PIS Version Number',  # 41
    0x2a: 'PIS Command Received',  # 42
    0x2b: 'PIS Library Upgrade',  # 43
    0x2c: 'PIS Schedule Download',  # 44
    0x2d: 'PIS Schedule Upgrade',  # 45
    0x2e: 'command',  # 46
    0x2f: 'command',  # 47
    0x30: 'command',  # 48
    0x31: 'command',  # 49
    0x32: 'command',  # 50
    0x33: 'PEC Answer',  # 51
    0x34: 'PEC Reset',  # 52
    0x35: 'PEC Activated',  # 53
    0x36: 'PEC Selected By Driver',  # 54
    0x37: 'PEC Command Received',  # 55
    0x38: 'Ready for PEC Conversation',  # 56
    0x39: 'Request for PEC Reset',  # 57
    0x3a: 'PEC Continue',  # 58
    0x3b: 'command',  # 59
    0x3c: 'command',  # 60
    0x3d: 'Critical Alarm',  # 61
    0x3e: 'command',  # 62
    0x3f: 'Request for OCC Call',  # 63
    0x40: 'Request for COMMS Change Over',  # 64
    0x41: 'Change Over Status',  # 65
    0x42: 'Bad Command',  # 66
    0x43: 'Change Over Status',  # 67
    0x44: 'OCC Call Command Received',  # 68
    0x45: 'OCC Call Reset',  # 69
    0x46: 'End of OCC Call',  # 70
    0x47: 'Test Call',  # 71
    0x48: 'Test Call Result',  # 72
    0x49: 'TETRA/ISCS Mode',  # 73
    0x4a: 'Request for Voice Call',  # 74
    0x4b: 'Change Area',  # 75
    0x4c: 'TETRA/ISCS Mode Received',  # 76
    0x4d: 'Change Area Received',  # 77
    0x4e: 'Voice Call Command Received',  # 78
    0x4f: 'End of Voice Call',  # 79
    0x50: 'command',  # 80
    0x51: 'command',  # 81
    0x52: 'command',  # 82
    0x53: 'command',  # 83
    0x54: 'command',  # 84
    0x55: 'command',  # 85
    0x56: 'command',  # 86
    0x57: 'command',  # 87
    0x58: 'command',  # 88
    0x59: 'command',  # 89
    0x5a: 'Test Alarm (2)',  # 90
    0x5b: 'TCI Alarms (2)',  # 91
}

ORIGINS = {
    0: 'TCI',
    1: 'TCI',
    10: 'OCC',
    11: 'OCCGWS1A',
    12: 'OCCGWS2A',
    13: 'OCCGWS3A',
    14: 'OCCGWS4A',
    15: 'OCCGWS5A',
    # The IDD does not specifically say this, but I suspect this is
    # the actual definition
    21: 'HBF Server',
    22: 'OTP Server',
    23: 'CNT Server',
    24: 'CQY Server',
    25: 'DBG Server',
    26: 'LTI Server',
    27: 'FRP Server',
    28: 'BNK Server',
    29: 'PTP Server',
    30: 'WLH Server',
    31: 'SER Server',
    32: 'KVN Server',
    33: 'HGN Server',
    34: 'BGK Server',
    35: 'SKG Server',
    36: 'PGL Server',
    37: 'PGC Server',
    51: 'HBF GWS',
    52: 'OTP GWS',
    53: 'CNT GWS',
    54: 'CQY GWS',
    55: 'DBG GWS',
    56: 'LTI GWS',
    57: 'FRP GWS',
    58: 'BNK GWS',
    59: 'PTP GWS',
    60: 'WLH GWS',
    61: 'SER GWS',
    62: 'KVN GWS',
    63: 'HGN GWS',
    64: 'BGK GWS',
    65: 'SKG GWS',
    66: 'PGL GWS',
    67: 'PGC GWS',
    80: 'DCC Server',
    81: 'NEDGWS1A',
    82: 'NEDGWS2A',
    83: 'NEDGWS3A DSM',
    90: 'TTCR Server',
    91: 'TTCR GWS',
}

PIS_STATUS_5 = {
    1: 'PIS Proceeding',
    2: 'PIS in Use',
    3: 'PIS Library Upgraded',
    4: 'PIS Reset',
    5: 'PIS Failed',
    10: 'Different Version No.'
}

PIS_STATUS_9 = {1: 'Request', 2: 'Ready for Upload'}

PIS_STATUS_10 = {0: 'Successful', 1: 'Failed'}


def init_logging():
    '''
    Initializes logger
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console_formatter = logging.Formatter(fmt='%(levelname)s %(message)s')
    console.setFormatter(console_formatter)
    console.setLevel(logging.INFO)
    logger.addHandler(console)

    logfile = logging.FileHandler('radiogaga.log')
    logfile_formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(message)s')
    logfile.setFormatter(logfile_formatter)
    logfile.setLevel(logging.DEBUG)
    logger.addHandler(logfile)


def parse_logfile(infile):
    '''
    Parses given rad_log file
    '''
    with open(infile, 'rb') as logfile:
        line_num = 0
        has_header = False

        rad_events = []

        event = None
        rad_data = ''  # temporarily holds binary data for radio event
        rad_text = ''  # temporarily holds text representation of the binary data

        for line in logfile:
            #line = line.strip()
            line_num += 1

            if len(line) == 0:
                logging.info('Ignoring blank line at {} of {}'.format(
                    line_num, infile))
                continue

            match = re.match(HEADER, line)
            if match:
                logging.debug('Line {} looks like a header'.format(line_num))
                has_header = True

                logging.debug('timestamp  : {}'.format(
                    match.group('timestamp')))
                logging.debug('length     : {}'.format(match.group('length')))
                logging.debug('session    : {}'.format(match.group('session')))
                logging.debug('trans_id   : {}'.format(
                    match.group('trans_id')))
                logging.debug('status     : {}'.format(match.group('status')))
                # Method = XXXX or Event = XXXX
                index = match.group('method').index('=')
                met_event = match.group('method')[index + 1:].strip()
                logging.debug('method/event: {}'.format(met_event))

                if event != None:
                    event['data'] = rad_data.strip()
                    event['text'] = rad_text.strip()
                    rad_events.append(event)

                    rad_data = ''
                    rad_text = ''

                event = {
                    'timestamp': match.group('timestamp'),  # time of the event
                    # length of the message
                    'length': int(match.group('length')),
                    'session': int(match.group('session')),  # session ID
                    # transmission ID
                    'trans_id': int(match.group('trans_id')),
                    'status': int(match.group('status')),  # status
                    # method/event (in hexadecimal)
                    'met_event': '0x{}'.format(met_event),
                    'i_met_event': int(met_event, 16),  # internal data
                    'description': '',  # description of the method/event
                    'command': '',  # command in SDS message
                    'atc_car': '',  # ATC car number in SDS message
                    'origin': '',  # Origin in SDS message
                    'sds_status': '',  # status returned in some SDS message
                    'data': '',  # binary data
                    'text': ''
                }  # ASCII representation of the binary data

                continue

            match = re.search(DATA, line)
            if match:
                logging.debug('Line {} looks like data'.format(line_num))
                if not has_header:
                    logging.warning(
                        'Encountered radio data without a header at line {} of {}; Skipping...'
                        .format(line_num, infile))
                    continue

                # Split the hexadecimal data and ASCII representation
                index = line.index('   ')

                hexdump = line[0:index].strip()
                text = line[index:].strip()

                logging.debug('hexdump: {}'.format(hexdump))
                logging.debug('text   : {}'.format(text))

                rad_data += ' ' + hexdump
                rad_text += '' + text

                logging.debug('rad_data: {}'.format(rad_data))
                logging.debug('rad_text: {}'.format(rad_text))
            else:
                logging.warning(
                    'Ignoring unexpected data at line {} of {}'.format(
                        line_num, infile))
                has_header = False
                rad_data = ''
                rad_text = ''
                logging.debug('{}'.format(line))

    if event != None:
        event['data'] = rad_data.strip()
        event['text'] = rad_text.strip()
        rad_events.append(event)

    logging.info('Extracted {} data from {}'.format(len(rad_events), infile))

    return rad_events


def describe_method_event(met_event):
    '''
    Describe the given method/event into descriptive text
    '''
    if met_event <= 0x65:  # Append METHOD_ to the description
        desc = 'METHOD_' + METHODS_EVENTS.get(met_event)
    elif met_event > 0x65 and met_event <= 0x8065:  # Append EVENTS_ to the description
        if (met_event % 0x8000) in METHODS_EVENTS:
            desc = 'EVENT_' + METHODS_EVENTS.get(met_event % 0x8000)
        else:
            desc = 'ERROR: Unknown event'
    else:
        desc = METHODS_EVENTS.get(met_event)
    logging.debug('{}: {}'.format(hex(met_event), desc))
    return desc


def convert_hex_to_dec(data):
    '''
    Convert a given hexadecimal string into a list of integers
    '''
    try:
        # Append a blank space at the beginning
        data = ' ' + data
        temp = data.replace(' ', '\\x')
        format = "%dB" % (len(temp.decode('string_escape')))
        raw_data = struct.unpack(format, temp.decode('string_escape'))
        logging.debug('raw_data: {}'.format(raw_data))
    except ValueError as e:
        logging.exception(e)
        logging.error('{}'.format(data))
        raw_data = []
    return raw_data


def decode_command(raw_data, offset):
    '''
    Returns command name from command ID
    '''
    cmd_code = raw_data[offset]
    cmd_name = COMMANDS.get(cmd_code)
    logging.debug('code: {} {}'.format(cmd_code, cmd_name))
    return [cmd_code, cmd_name]


def decode_atc_car_num(raw_data, offset):
    '''
    Returns ATC car number from SDS message
    '''
    return raw_data[offset] << 8 | raw_data[offset + 1]


def decode_origin(raw_data, offset):
    '''
    Decode the origin field of the SDS message
    '''
    return ORIGINS.get(raw_data[offset])


def decode_sds_message(event, raw_data):
    '''
    '''
    if event['i_met_event'] == 0x18:  # METHOD_SENDSDS
        offset = 44
    elif event['i_met_event'] == 0xa002:  # EVENT_INCOMINGSDS
        offset = 76
    else:
        return

    logging.debug('offset: {}, value: {}'.format(offset, raw_data[offset]))
    if raw_data[offset] != 0x07:
        logging.error('Unexpected flag value {} at {}'.format(
            raw_data[offset], offset))
        return

    [cmd_code, cmd_name] = decode_command(raw_data, offset + 1)
    logging.debug('command: {}, {}'.format(cmd_code, cmd_name))
    event['command'] = '{} ({})'.format(cmd_name, hex(cmd_code))

    atc_car = decode_atc_car_num(raw_data, offset + 2)
    logging.debug('ATC car number: {}'.format(atc_car))
    event['atc_car'] = '{} ({})'.format(atc_car, hex(atc_car))

    origin = decode_origin(raw_data, offset + 5)
    logging.debug('origin: {}'.format(origin))
    event['origin'] = origin

    if cmd_code >= 0x1f and cmd_code <= 0x2d:
        [status_code,
         status_name] = decode_pis_command_status(cmd_code, offset, raw_data)
        if status_name == None:
            event['sds_status'] = 'Undefined ({})'.format(status_code)
        elif len(status_name) > 0:
            event['sds_status'] = '{} ({})'.format(status_name,
                                                   hex(status_code))


def decode_pis_command_status(command, offset, raw_data):
    '''
    '''
    index = raw_data[offset + 6]

    if command == 0x22:  # PIS Library Upload (1)
        logging.debug('0x22: {}, {}'.format(index, raw_data))
        return [index, PIS_STATUS_9.get(index)]
    elif command == 0x27:  # End of PIS Download
        # status 10
        logging.debug('0x27: {}, {}'.format(index, raw_data))
        return [index, PIS_STATUS_10.get(index)]
    elif command == 0x2a:  # PIS Command Received
        # status 5
        logging.debug('0x2a: {}, {}'.format(index, raw_data))
        return [index, PIS_STATUS_5.get(index)]
    else:
        # there are no status value
        return ['', '']


def write_events(events, outfile):
    '''
    Writes events to a file
    '''
    with open(outfile, 'wb') as csvfile:
        fieldnames = [
            'timestamp', 'length', 'session', 'trans_id', 'status',
            'met_event', 'i_met_event', 'description', 'command', 'atc_car',
            'origin', 'sds_status', 'data', 'text'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in events:
            writer.writerow(row)


def main():
    '''
    main function
    '''
    init_logging()

    parser = argparse.ArgumentParser(prog='radiogaga')
    parser.add_argument('--log',
                        '-l',
                        required=True,
                        dest='logs',
                        help='path to rad_log files')
    parser.add_argument('--output',
                        '-o',
                        required=True,
                        dest='outfile',
                        help='writes events from rad_log to a CSV file')
    args = parser.parse_args()
    print(args)

    # Parse the given log file into a series of events
    rad_events = parse_logfile(args.logs)

    # Decode parts of radio events
    for row in rad_events:
        description = describe_method_event(row['i_met_event'])
        row['description'] = description

        if len(row['data']) > 0:
            raw_data = convert_hex_to_dec(row['data'])
            decode_sds_message(row, raw_data)

    write_events(rad_events, args.outfile)


if __name__ == '__main__':
    main()

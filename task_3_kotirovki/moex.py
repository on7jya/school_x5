import argparse
import csv
import datetime
import json
import logging
import xml.etree.ElementTree as ElementTree

import requests as req

URI = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities/five.xml'
TIMEOUT = 30


def log_to_file(namelogger):
    """Logging to file"""
    global logger
    logger = logging.getLogger(namelogger)  # create logger
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("kotirovki.log")  # create console handler and set level to debug
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)  # add formatter to fh
    logger.addHandler(fh)  # add fh to logger
    return logger


def log_to_console(message):
    """Print to console"""
    print(f'{datetime.datetime.now().strftime("%Y-%m-%d %T")} - {message}')


def create_parser():
    """Parse arguments from command line"""
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-format', type=str, required=True, help="format file")
        parser.add_argument('-out', type=str, required=True, help="path to output file")
        parser.add_argument('-watch', required=False, action='store_const', const=True,
                            default=False, help="tracking mode")
        parser.add_argument('-refresh', type=int, required=False, default='60', help="seconds refresh information")
        return parser
    except TypeError as e:
        logger.error("error parsing arguments from the command line: " + str(e))
    except KeyboardInterrupt as e:
        logger.error(str(e))


def get_request_moex():
    """GET request to MOEX API"""
    try:
        response = req.get(url=URI, timeout=TIMEOUT)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        return response.content
    except req.Timeout:
        logger.error(f'error timeout, url: {URI}')
    except req.HTTPError as err:
        code = err.response.status_code
        logger.error(f'error url: {URI}, code: {code}')
    except req.RequestException:
        logger.error(f'download error url: {URI}')


def parse_xml(xml_tmp, format_out, path):
    """Parse the XML file from API"""
    tree = ElementTree.XML(xml_tmp)
    row_to_file = []
    try:
        row = tree.find("data[@id='marketdata']/rows/row")
        value_updatetime = row.get('UPDATETIME')
        value_open = row.get('OPEN')
        value_low = row.get('LOW')
        value_high = row.get('HIGH')
        value_last = row.get('LAST')

        prev_updatetime = last_time_from_file(path)
        logger.info('prev_updatetime ' + prev_updatetime + ' updatetime ' + value_updatetime)

        if prev_updatetime != value_updatetime:
            row_to_file.append(datetime.datetime.now().strftime("%Y-%m-%d %T"))
            row_to_file.append(value_updatetime)
            row_to_file.append(value_open)
            row_to_file.append(value_low)
            row_to_file.append(value_high)
            row_to_file.append(value_last)
            save_to_file(row_to_file, path, format_out)
            return True
        else:
            logger.warning(f'UPDATETIME matches the last available value, the file will not be written!')
            return False
    except ElementTree.ParseError as e:
        logger.error(f'parsing error: {str(e)}')


def save_to_file(lst, path, format_file):
    """Write information to output file"""
    try:
        if format_file.upper() == 'CSV':
            with open(path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(lst)
        elif format_file.upper() == 'JSON':
            with open(path, 'w') as f:
                json.dump(lst, f)
        else:
            logger.error(f'unknown format specified: {format_file.upper()}')
    except IOError as e:
        logger.error(f'error writing to file {str(e)}')


def last_time_from_file(path):
    """Parsing a value last updatetime from output file"""
    prev_updatetime = 'no_time'
    try:
        with open(path, "r") as file:
            last_line = file.readlines()[-1]
        last_line = last_line.split(',')
        prev_updatetime = last_line[1].strip(' ').strip('"')
    except IndexError as e:
        logger.error(f'Empty file, checking for the last value from the file will not work: {str(e)}')
    return prev_updatetime

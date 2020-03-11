import argparse
import csv
import json
import requests as req
import xml.etree.ElementTree as ET
import datetime
import sys


def create_parser():
    """Parse arguments from command line"""
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-format', nargs='?')
        parser.add_argument('-out', nargs='?')
        return parser
    except Exception as e:
        print("ошибка разбора аргументов из командной строки: " + str(e))


def get_request_moex():
    """GET request to MOEX API"""
    try:
        url = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities/five.xml'
        response = req.get(url, timeout=30)
        response.raise_for_status()
    except req.Timeout:
        print(f'ошибка timeout, url: {url}')
    except req.HTTPError as err:
        code = err.response.status_code
        print(f'ошибка url: {url}, code: {code}')
    except req.RequestException as e:
        print(f'ошибка скачивания url: {url}')
    except Exception as e:
        print(f'ошибка: {str(e)}')
    else:
        # print(response.content)
        pass
    return response.content


def parse_XML(format_out, path):
    """Parse the XML file from API"""
    xml_tmp = get_request_moex()
    tree = ET.XML(xml_tmp)
    try:
        row = tree.find("data[@id='marketdata']/rows/row")

        row_to_file = []

        value_updatetime = row.get('UPDATETIME')
        value_open = row.get('OPEN')
        value_low = row.get('LOW')
        value_high = row.get('HIGH')
        value_last = row.get('LAST')

        prev_updatetime = last_time_from_file(path)
        print('prev_updatetime ' + prev_updatetime)
        print('UPDATETIME ' + value_updatetime)

        if prev_updatetime != value_updatetime:
            row_to_file.append(datetime.datetime.now().strftime("%Y-%m-%d %T"))
            row_to_file.append(value_updatetime)
            row_to_file.append(value_open)
            row_to_file.append(value_low)
            row_to_file.append(value_high)
            row_to_file.append(value_last)

            save_to_file(row_to_file, path, format_out)
        else:
            print(f'UPDATETIME совпадает с последним имеющимся значением, запись в файл не будет осуществлена!')
    except ET.ParseError as e:
        print(f'ошибка парсинга: {str(e)}')
    except Exception as e:
        print(f'ошибка: {str(e)}')


def save_to_file(lst, path, format):
    """Write information to output file"""
    try:
        if format.upper() == 'CSV':
            with open(path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(lst)
        elif format.upper() == 'JSON':
            with open(path, 'w') as f:
                json.dump(lst, f)
        else:
            print(f'задан неизвестный формат: {format.upper()}')
    except Exception as e:
        print(f'ошибка записи в файл {str(e)}')


def last_time_from_file(path):
    """Parsing a value last updatetime from output file"""
    try:
        with open(path, "r") as file:
            last_line = file.readlines()[-1]
            print(last_line)
        last_line = last_line.split(',')
        prev_updatetime = last_line[1].strip(' ').strip('"')
        return prev_updatetime
    except Exception as e:
        print(f'в файле нет строк, проверка на последнее значение из файла не сработает: {str(e)}')
        return 'no_time'


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    # print(args.format)
    # print(args.out)
    parse_XML(args.format, args.out)


if __name__ == "__main__":
    main()

# python kotirovki.py -format csv -out ./output_task_3.csv
# python kotirovki.py -format json -out ./output_task_3.json
# python kotirovki.py -format xml -out ./output_task_3.xml

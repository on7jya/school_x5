import argparse
import sys

file_path = str(sys.argv[1])

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', nargs='?')
    return parser


def find_and_print_result(list):
    most_common = None
    qty_most_common = 0
    dict_common = dict()  # most_common, qty_most_common

    for item in list:
        qty = list.count(item)
        dict_common.update({int(item): qty})
        if qty > qty_most_common:
            qty_most_common = qty
            most_common = int(item)

    # Если несколько значений встретились одинаковое количество раз, то вывести наименьшее из них.
    max_value = max(dict_common.values())
    min_key = most_common
    for key, value in dict_common.items():
        if value == max_value:
            if min_key >= key:
                min_key = key
                most_common = key
                qty_most_common = value

    print(str(most_common) + ' - ' + str(qty_most_common))


def string_append_to_list(string, list):
    num = string.replace('\n', '')
    list.append(num)

def read_from_file(file_path, size_pack):
    try:
        f = open(file_path)
        count = 0
        nums_aggr = []
        for line in f:
            if count % (size_pack) == 0 and count != 0:
                find_and_print_result(nums_aggr)
                nums_aggr = []

            count += 1
            string_append_to_list(line, nums_aggr)

        find_and_print_result(nums_aggr)
    except IOError:
        return ""


def main():

    parser = create_parser()
    args = parser.parse_args(sys.argv[2:])
    if args.size is None:
        args.size = 10
        print('Pack size set to 10')

    path = file_path
    read_from_file(path, int(args.size))


if __name__ == "__main__":
    main()


# в среду доработать отлов ошибок и тесты
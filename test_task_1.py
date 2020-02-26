import task_1
import pytest


# тестирование функции поиска конечного результата
def test_find_and_print_result_1():
    list_from_file = ['1', '1', '3', '3', '3']
    most_common, qty = task_1.find_and_print_result(list_from_file)
    assert (most_common == '3') & (qty == '3')


def test_find_and_print_result_2():
    list_from_file = ['5', '4', '1', '3', '2']
    most_common, qty = task_1.find_and_print_result(list_from_file)
    assert (most_common == '1') & (qty == '1')


def test_find_and_print_result_3():
    list_from_file = ['9', '10', '22', '10', '22']
    most_common, qty = task_1.find_and_print_result(list_from_file)
    assert (most_common == '10') & (qty == '2')


# тестирование функции чтения из файла
def test_read_from_file():
    fname = 'tests/test_input_task_1.txt'
    with open(fname, 'w') as fp:
        fp.write('1\n1\n3\n3\n3\n9\n5\n1\n7\n8\n10\n22\n10\n22\n9\n1\n1\n1\n22\n22\n')
    task_1.read_from_file(fname, 5)
    assert 1

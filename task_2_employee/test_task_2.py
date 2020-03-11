import pytest
import task_2
import os
from dicttoxml import dicttoxml  # библиотека для сериализации объекта типа данных Dictionary  в XML
import json


# тестирование функции сортировки
def test_sort():
    emp1 = task_2.Employee('Piotr', 'Ivanov', 'pp@ya.ru')
    emp2 = task_2.Employee('Irina', 'Petrova', 'ir@ya.ru')
    emp3 = task_2.Administrator('Irina', 'Nikolaeva', 'ir@ya.ru', ["127.0.0.1", "192.168.1.2", "133.134.122.111"])
    emps = [emp1, emp2, emp3]
    task_2.EmpList.sort_empl(emps)
    assert (emps[2].last_name == 'Petrova') & (emps[0].last_name == 'Ivanov')


# тестирование функции сериализации в JSON
def test_save_list_json():
    emp1 = task_2.Employee('Piotr', 'Ivanov', 'pp@ya.ru')
    emp2 = task_2.Employee('Irina', 'Petrova', 'ir@ya.ru')
    emp3 = task_2.Administrator('Irina', 'Nikolaeva', 'ir@ya.ru', ["127.0.0.1", "192.168.1.2", "133.134.122.111"])
    emps = [emp1, emp2, emp3]
    path = "tests/test_save_list_json.json"
    task_2.EmpList.save_list(emps, path, "JSON")
    assert os.path.isfile(path)


# тестирование функции сериализации в XML
def test_save_list_xml():
    emp1 = task_2.Employee('Piotr', 'Ivanov', 'pp@ya.ru')
    emp2 = task_2.Employee('Irina', 'Petrova', 'ir@ya.ru')
    emp3 = task_2.Administrator('Irina', 'Nikolaeva', 'ir@ya.ru', ["127.0.0.1", "192.168.1.2", "133.134.122.111"])
    emps = [emp1, emp2, emp3]
    path = "tests/test_save_list_xml.xml"
    task_2.EmpList.save_list(emps, path, "XML")
    assert os.path.isfile(path)


# тестирование функции десериализации XML
def test_load_list_xml():
    path = "tests/test_load_list_xml.xml"
    emp4 = task_2.Director('Svetlana', 'Sergeeva', 's_sergeeva@ya.ru', 'ERP')
    emp1 = task_2.Employee('Piotr', 'Ivanov', 'pp@ya.ru')
    emp2 = task_2.Developer('Irina', 'Petrova', 'ir@ya.ru', ["1C", "Excel", "Word"])
    emp3 = task_2.Administrator('Irina', 'Nikolaeva', 'ir@ya.ru', ["127.0.0.1", "192.168.1.2", "133.134.122.111"])
    emps = [emp1, emp2, emp3]
    out_list = []
    for el in emps:
        out_list.append(el.__dict__)
    item_f = lambda x: 'employee' if x == 'employees' else (
        'ip' if x == 'vms' else ('name' if x == 'systems' else 'item'))
    xml = dicttoxml(out_list, item_func=item_f, custom_root='employees', attr_type=False)
    from xml.dom.minidom import parseString
    with open(path, 'w') as f:
        dom = parseString(xml)
        f.write(dom.toprettyxml())
    ll = task_2.EmpList.load_list(path, "XML")
    assert len(ll) == len(out_list)


# тестирование функции десериализации JSON
def test_load_list_json():
    path = "tests/test_load_list_json.json"
    emp4 = task_2.Director('Svetlana', 'Sergeeva', 's_sergeeva@ya.ru', 'ERP')
    emp1 = task_2.Employee('Piotr', 'Ivanov', 'pp@ya.ru')
    emp2 = task_2.Developer('Irina', 'Petrova', 'ir@ya.ru', ["1C", "Excel", "Word"])
    emp3 = task_2.Administrator('Irina', 'Nikolaeva', 'ir@ya.ru', ["127.0.0.1", "192.168.1.2", "133.134.122.111"])
    emps = [emp1, emp2, emp3]
    out_list = []
    for el in emps:
        out_list.append(el.__dict__)
    dc = {}
    dc['employees'] = out_list
    with open(path, 'w') as f:
        json.dump(dc, f)
    ll = task_2.EmpList.load_list(path, "JSON")
    assert len(ll) == len(out_list)

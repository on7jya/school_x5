import json
from dicttoxml import dicttoxml
import os

# переменные окружения
# EMPLOYEES_FILE = "input_task_2.xml"
# OUTPUT_FILE = "output_task_2.xml"
# OUTPUT_FORMAT = "XML"

EMPLOYEES_FILE = os.getenv('EMPLOYEES_FILE')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT')


class Employee:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.title = ''

    def __repr__(self):
        return self.last_name + ' ' + self.first_name

    def Compare(emp1, emp2):
        if emp1.last_name != emp2.last_name:
            return 0 if emp1.last_name < emp2.last_name else 1
        else:
            return 0 if emp1.first_name < emp2.first_name else 1


class Director(Employee):
    def __init__(self, first_name, last_name, email, department):
        super(Director, self).__init__(first_name, last_name, email)
        self.department = department
        self.title = 'Директор'


class Developer(Employee):
    def __init__(self, first_name, last_name, email, systems):
        super(Developer, self).__init__(first_name, last_name, email)
        self.systems = systems
        self.title = 'Разработчик'


class Administrator(Employee):
    def __init__(self, first_name, last_name, email, vms):
        super(Administrator, self).__init__(first_name, last_name, email)
        self.vms = vms
        self.title = 'Администратор'


class EmpList:
    # метод для десериализации
    def LoadList(path, format):
        dc = {}
        dcl = []  # список для хранения  объектов Dictionary
        if format == 'JSON':
            try:
                with open(path, 'r') as f:
                    dc = json.load(f)
                    dcl = dc['employees']
                    # print(dc)
            except IOError as ioerr:
                print("Ошибка доступа к файлу " + str(ioerr))
            except Exception as e:  # исходный файл должен быть в ANSI
                print("Неизвестная ошибка при преобразовании данных JSON: " + str(e))
        if format == 'XML':
            try:
                from xml.etree import cElementTree as ElementTree
                with open(path, 'r') as f:
                    str_tmp = f.read()
                    root = ElementTree.XML(str_tmp)
                    for item in root:
                        dict_emp = {}
                        for sub_item in item:
                            tag = sub_item.tag
                            if tag in ['vms', 'systems']:
                                ar = []
                                for ar_item in sub_item:
                                    ar.append(ar_item.text)
                                dict_emp[sub_item.tag] = ar
                            else:
                                dict_emp[sub_item.tag] = sub_item.text
                        dcl.append(dict_emp)
            except IOError as ioerr:
                print("Ошибка доступа к файлу " + str(ioerr))
            except Exception as e:
                print("Неизвестная ошибка при преобразовании данных XML: " + str(e))
        # print(dcl)

        # преобразование списка объектов Dictionary в список объектов классов Administator, Director, Developer
        emps = []
        for item in dcl:
            try:
                if item['title'] == 'Директор':
                    emp = Director(item['first_name'], item['last_name'], item['email'], item['department'])
                    emps.append(emp)
                elif item['title'] == 'Администратор':
                    emp = Administrator(item['first_name'], item['last_name'], item['email'], item['vms'])
                    emps.append(emp)
                elif item['title'] == 'Разработчик':
                    emp = Developer(item['first_name'], item['last_name'], item['email'], item['systems'])
                    emps.append(emp)
                else:
                    emp = Employee(item['first_name'], item['last_name'], item['email'])
                    emps.append(emp)

            except Exception as e:
                print("Ошибка при создании экзамепляра класса работника: " + str(e))

        return emps

    def SaveList(lst, path, format):
        out_list = []
        for el in lst:
            out_list.append(el.__dict__)
        if format == 'JSON':
            dc = {}
            dc['employees'] = out_list

            with open(path, 'w') as f:
                json.dump(dc, f)
        if format == 'XML':
            item_f = lambda x: 'employee' if x == 'employees' else (
                'ip' if x == 'vms' else ('name' if x == 'systems' else 'item'))
            xml = dicttoxml(out_list, item_func=item_f, custom_root='employees', attr_type=False)
            from xml.dom.minidom import parseString
            with open(path, 'w') as f:
                dom = parseString(xml)
                f.write(dom.toprettyxml())

    def Sort(lst):
        try:
            for i in range(0, len(lst) - 1):
                for j in range(i + 1, len(lst)):
                    if Employee.Compare(lst[i], lst[j]) == 1:
                        tmp = lst[j]
                        lst[j] = lst[i]
                        lst[i] = tmp
        except Exception as e:
            print("Ошибка в функции сортировки: " + str(e))


if __name__ == '__main__':
    emps = EmpList.LoadList(EMPLOYEES_FILE, OUTPUT_FORMAT)
    EmpList.Sort(emps)
    EmpList.SaveList(emps, OUTPUT_FILE, OUTPUT_FORMAT)

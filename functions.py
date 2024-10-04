import json
import xml.etree.ElementTree as ET
import os
from classes import *

# Функция для красивых отступов в XML
def indent_xml(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent_xml(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# функция для проверки расширения файла
def chek_file_extencion(filename, extension):
    file_extencion = os.path.splitext(filename)[1][1:]
    return file_extencion.lower() == extension.lower()


# Вспомогательная функция для ввода положительного целого числа
def input_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise Exception_capacity(value)
            return value
        except ValueError:
            print("Ошибка: введите целое число.")
        except Exception_capacity as e:
            print(e.message)

# Вспомогательная функция для ввода непустой строки
def input_non_empty_str(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        print("Ошибка: строка не должна быть пустой.")

# Функция выбора типа транспорта
def choose_transport():
    print("Выберите тип транспорта:")
    print("1. Автобус (Bus)")
    print("2. Самолёт (Plane)")
    print("3. Поезд метро (Subway_train)")
    print("4. Трамвай (Tram)")
    choice = input("Введите номер: ")

    if choice == "1":
        return Bus(
            capacity=input_positive_int("Введите вместимость автобуса: "),
            route_number=input_positive_int("Введите номер маршрута: "),
            color=input_non_empty_str("Введите цвет автобуса: ")
        )
    elif choice == "2":
        return Plane(
            capacity=input_positive_int("Введите вместимость самолёта: "),
            flight_name=input_non_empty_str("Введите название рейса: "),
            route_number=input_positive_int("Введите номер маршрута: ")
        )
    elif choice == "3":
        return Subway_train(
            capacity=input_positive_int("Введите вместимость поезда метро: "),
            subway_train_name=input_non_empty_str("Введите название поезда: "),
            route_number=input_positive_int("Введите номер маршрута: ")
        )
    elif choice == "4":
        return Tram(
            capacity=input_positive_int("Введите вместимость трамвая: "),
            tram_name=input_non_empty_str("Введите название трамвая: "),
            route_number=input_positive_int("Введите номер маршрута: ")
        )
    else:
        print("Неверный выбор. Попробуйте снова.")
        return choose_transport()

# Функция сохранения данных в JSON файл
def save_to_json(filename, objects):
    with open(filename, 'w') as file:
        json.dump([obj.to_dict() for obj in objects], file, indent=4)
    print(f"Данные сохранены в файл {filename}")

# Функция загрузки данных из JSON файла
def load_from_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return [Transport.from_dict(item) for item in data]
    except FileNotFoundError:
        print("Файл не найден")
        return []

# Сохранение данных в XML файл
def save_to_xml(filename, objects):
    root = ET.Element("Transports")

    for obj in objects:
        obj_element = ET.SubElement(root, obj.__class__.__name__)
        for key, value in obj.to_dict().items():
            ET.SubElement(obj_element, key).text = str(value)

    indent_xml(root)
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Данные сохранены в XML файл {filename}")

# Загрузка данных из XML файла
def load_from_xml(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()

        objects = []
        for obj_element in root:
            obj_data = {}
            for data in obj_element:
                obj_data[data.tag] = data.text

            # Преобразуем строки в соответствующие типы данных
            if 'capacity' in obj_data:
                obj_data['capacity'] = int(obj_data['capacity'])
            if 'route_number' in obj_data:
                obj_data['route_number'] = int(obj_data['route_number'])

            # Восстановление объекта на основе типа
            obj = Transport.from_dict(obj_data)
            objects.append(obj)

        return objects
    except FileNotFoundError:
        print("Файл не найден")
        return []
    except ET.ParseError:
        print("Ошибка разбора XML")
        return []

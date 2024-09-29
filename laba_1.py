import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

# Исключение для проверки вместимости
class Exception_capacity(Exception):
    def __init__(self, value):
        self.value = value
        self.message = f"Значение {value} является недопустимым. Должно быть > 0"
        super().__init__(self.message)

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

# Основное меню
def main():
    objects = []

    while True:
        print("\nМеню:")
        print("1. Добавить новый транспорт")
        print("2. Сохранить данные в файл Json")
        print("3. Загрузить данные из файла Json")
        print("4. Показать все данные")
        print("5. Сохранить данные в XML файл")
        print("6. Загрузить данные из XML файла")
        print("7. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            transport = choose_transport()
            objects.append(transport)
            print(f"Добавлен {transport.__class__.__name__}: {transport.to_dict()}")
        elif choice == "2":
            filename = input("Введите имя файла для сохранения: ")
            save_to_json(filename, objects)
        elif choice == "3":
            filename = input("Введите имя файла для загрузки: ")
            objects = load_from_json(filename)
        elif choice == "4":
            if objects:
                for obj in objects:
                    print(f"Тип: {obj.__class__.__name__}, Данные: {obj.to_dict()}")
            else:
                print("Нет данных для отображения.")
        elif choice == "5":
            filename = input("Введите имя XML файла для сохранения: ")
            save_to_xml(filename, objects)
        elif choice == "6":
            filename = input("Введите имя XML файла для загрузки: ")
            objects = load_from_xml(filename)
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

# Базовый класс Transport
class Transport:
    def __init__(self, capacity=0, route_number=0):
        self.capacity = capacity
        self.route_number = route_number

    def get_route_number(self) -> int:
        return self.route_number

    def get_capacity(self) -> int:
        return self.capacity

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "capacity": self.capacity,
            "route_number": self.route_number
        }

    @staticmethod
    def from_dict(data: dict) -> 'Transport':
        if data["type"] == "Bus":
            return Bus.from_dict(data)
        elif data["type"] == "Plane":
            return Plane.from_dict(data)
        elif data["type"] == "Subway_train":
            return Subway_train.from_dict(data)
        elif data["type"] == "Tram":
            return Tram.from_dict(data)
        else:
            return Transport(data["capacity"], data["route_number"])

# Класс Bus
class Bus(Transport):
    def __init__(self, capacity: int, route_number: int, color: str = "white"):
        super().__init__(capacity, route_number)
        self.color = color

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "capacity": self.capacity,
            "route_number": self.route_number,
            "color": self.color
        }

    @staticmethod
    def from_dict(data: dict) -> 'Bus':
        return Bus(data["capacity"], data["route_number"], data["color"])

# Класс Plane
class Plane(Transport):
    def __init__(self, capacity: int, flight_name: str, route_number: int):
        super().__init__(capacity, route_number)
        self.flight_name = flight_name

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "capacity": self.capacity,
            "flight_name": self.flight_name,
            "route_number": self.route_number
        }

    @staticmethod
    def from_dict(data: dict) -> 'Plane':
        return Plane(data["capacity"], data["flight_name"], data["route_number"])

# Класс Subway_train
class Subway_train(Transport):
    def __init__(self, capacity: int, subway_train_name: str, route_number: int):
        super().__init__(capacity, route_number)
        self.subway_train_name = subway_train_name

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "capacity": self.capacity,
            "subway_train_name": self.subway_train_name,
            "route_number": self.route_number
        }

    @staticmethod
    def from_dict(data: dict) -> 'Subway_train':
        return Subway_train(data["capacity"], data["subway_train_name"], data["route_number"])

# Класс Tram
class Tram(Transport):
    def __init__(self, capacity: int, tram_name: str, route_number: int):
        super().__init__(capacity, route_number)
        self.tram_name = tram_name

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "capacity": self.capacity,
            "tram_name": self.tram_name,
            "route_number": self.route_number
        }

    @staticmethod
    def from_dict(data: dict) -> 'Tram':
        return Tram(data["capacity"], data["tram_name"], data["route_number"])

if __name__ == "__main__":
    main()

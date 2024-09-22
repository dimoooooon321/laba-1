import json


class Transport:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Вместимость должна быть положительным числом")
        self.capacity = capacity

    def get_capacity(self):
        return self.capacity

    def set_capacity(self, capacity):
        self.capacity = capacity
        if capacity <= 0:
            raise ValueError("Вместимость должна быть положительным числом")

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "capacity": self.capacity
        }

    @staticmethod
    def from_dict(data: dict) -> 'Transport':
        if data["type"] == "Bus":
            return Bus.from_dict(data)
        elif data["type"] == "Plane":
            return Plane.from_dict(data)
        else:
            return Transport(data["capacity"])


class Bus(Transport):

    def __init__(self, capacity: int, route_number: int, color: str = "white") -> None:
        super().__init__(capacity)
        self.capacity = capacity
        self.color = color
        self.route_number = route_number
        if route_number <= 0:
            raise ValueError("номер маршрута должен быть положительным числом")

    def get_color(self) -> str:
        return self.color

    def get_route_number(self) -> int:
        return self.route_number

    def set_color(self, color) -> None:
        self.color = color

    def set_route_number(self, route_number) -> None:
        self.route_number = route_number

    # метод словаря
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


class Plane(Transport):

    def __init__(self, capacity: int, flight_name: str, flight_number: int) -> None:
        super().__init__(capacity)
        self.flight_number = flight_number
        self.flight_name = flight_name
        if flight_number <= 0:
            raise ValueError("номер рейса должен быть положительным числом")

    pass

    def get_flight_number(self) -> int:
        return self.flight_number

    def get_flihght_name(self) -> str:
        return self.flight_name

    def set_flight_number(self, flight_number):
        self.flight_number = flight_number

    def set_flight_name(self, flight_name):
        self.flight_name = flight_name

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "capacity": self.capacity,
            "flight_name": self.flight_name,
            "flight_number": self.flight_number
        }

    @staticmethod
    def from_dict(data: dict) -> 'Plane':
        return Plane(data["capacity"], data["flight_name"], data["flight_number"])

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            print("Файл успешно открыт\n")
            print(data)
    except IOError as e:
        print("Не удалось прочитать файл")
        data = []

# Функция для записи списка объектов в JSON-файл
def save_to_file(filename, objects):
    with open(filename, 'w') as file:
        json.dump([obj.to_dict() for obj in objects], file, indent=4)

# Функция для чтения объектов из JSON-файла
def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return [Transport.from_dict(item) for item in data]
    except FileNotFoundError:
        print("Файл не найден")
        return []

# Пример использования
bus = Bus(40, 120, "blue")
plane = Plane(180, "Flight-777", 777)

# Запись объектов в файл
objects_to_save = [bus, plane]
save_to_file('data.json', objects_to_save)

# Чтение объектов из файла
loaded_objects = load_from_file('data.json')

for obj in loaded_objects:
    print(f"Тип: {obj.__class__.__name__}, Данные: {obj.to_dict()}")

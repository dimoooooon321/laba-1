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
            "capcity": self.capacity
        }



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
            "capcity": self.capacity,
            "color": self.color,
            "route_number": self.route_number
        }

class Plane(Transport):

    def __init__(self, capacity: int, flight_name: str, flight_number: int) -> None:
        super().__init__(capacity)
        self.capacity = capacity
        self.flight_number = flight_number
        if flight_number <= 0:
            raise ValueError("номер рейса должен быть положительным числом")
        self.flight_name = flight_name

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
            "capcity": self.capacity,
            "flight_name": self.flight_name,
            "flight_number": self.flight_number
        }



    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            print("Файл успешно открыт\n")
            print(data)
    except IOError as e:
        print("Не удалось прочитать файл")
        data = []

    bus1 = (17, 228, "white")

    js1 = json.dumps(bus1)
    print('\n')
    print(js1)

    js2 = json.dumps(bus1, indent=4) # indent - отступ в формате json (т.е. 4 пробела)
    print(js2)


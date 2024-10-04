

# Исключение для проверки вместимости
class Exception_capacity(Exception):
    def __init__(self, value):
        self.value = value
        self.message = f"Значение {value} является недопустимым. Должно быть > 0"
        super().__init__(self.message)

# Базовый класс Transport
class Transport:
    def __init__(self, capacity = 0, route_number = 0):
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
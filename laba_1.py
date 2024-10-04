from classes import *
from functions import *

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
            while True:
                filename = input("Введите имя файла для сохранения: ")
                if(chek_file_extencion(filename, "json")):
                    save_to_json(filename, objects)
                    break
                else: print("неверный формат файла")
        elif choice == "3":
            filename = input("Введите имя файла для загрузки: ")
            while True:
                if(chek_file_extencion(filename,"json")):
                    objects = load_from_json(filename)
                    break
                else: print("неверный формат файла")
        elif choice == "4":
            if objects:
                for obj in objects:
                    print(f"Тип: {obj.__class__.__name__}, Данные: {obj.to_dict()}")
            else:
                print("Нет данных для отображения.")
        elif choice == "5":
            while True:
                filename = input("Введите имя файла в формате 'example.xml' для сохранения: ")
                if (chek_file_extencion(filename,"xml")) == True:
                    save_to_xml(filename, objects)
                    break
                else:print("неверный формат файла")
        elif choice == "6":
            while True:
                filename = input("Введите имя файла в формате 'example.xml' для загрузки: ")
                if (chek_file_extencion(filename, "xml")) == True:
                    objects = load_from_xml(filename)
                    break
                else:
                    print("неверный формат файла")
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")



if __name__ == "__main__":
    main()

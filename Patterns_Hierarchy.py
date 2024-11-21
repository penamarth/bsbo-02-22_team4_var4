from abc import ABC, abstractmethod


# Интерфейс обработчика
class ОбработчикЗапроса(ABC):
    def __init__(self, имя):
        self._следующий_обработчик = None
        self.имя = имя

    def установить_следующий(self, обработчик):
        self._следующий_обработчик = обработчик
        return обработчик

    @abstractmethod
    def обработать_запрос(self, запрос):
        if self._следующий_обработчик:
            print(
                f"{self.имя} не может обработать запрос '{запрос['тип']}' и передает его дальше."
            )
            return self._следующий_обработчик.обработать_запрос(запрос)
        print(f"Запрос '{запрос['тип']}' не может быть обработан.")
        return False


# Конкретные обработчики
class Аспирант(ОбработчикЗапроса):
    def обработать_запрос(self, запрос):
        if запрос["тип"] == "помощь_с_курсом":
            print(f"{self.имя} обработал запрос: {запрос['описание']}.")
            return True
        return super().обработать_запрос(запрос)


class Преподаватель(ОбработчикЗапроса):
    def обработать_запрос(self, запрос):
        if запрос["тип"] == "внесение_успеваемости":
            print(f"{self.имя} обработал запрос: {запрос['описание']}.")
            return True
        return super().обработать_запрос(запрос)


class ЗаведующийКафедрой(ОбработчикЗапроса):
    def обработать_запрос(self, запрос):
        if запрос["тип"] == "утверждение_учебной_программы":
            print(f"{self.имя} обработал запрос: {запрос['описание']}.")
            return True
        return super().обработать_запрос(запрос)


class Декан(ОбработчикЗапроса):
    def обработать_запрос(self, запрос):
        if запрос["тип"] in ["перевод_группы", "генерация_отчета"]:
            print(f"{self.имя} обработал запрос: {запрос['описание']}.")
            return True
        return super().обработать_запрос(запрос)


# Основной класс системы деканата
class СистемаДеканата:
    def __init__(self):
        # Создаем обработчиков
        self.асп = Аспирант("Аспирант")
        self.преп = Преподаватель("Преподаватель")
        self.зав_каф = ЗаведующийКафедрой("Заведующий кафедрой")
        self.декан = Декан("Декан")

        # Строим цепочку обязанностей
        self.асп.установить_следующий(self.преп).установить_следующий(
            self.зав_каф
        ).установить_следующий(self.декан)

    def обработать_запрос(self, тип, описание):
        запрос = {"тип": тип, "описание": описание}
        print(f"Создан запрос: '{запрос['тип']}' - {запрос['описание']}")
        результат = self.асп.обработать_запрос(запрос)
        if результат:
            print(f"Запрос '{тип}' успешно обработан.\n")
        else:
            print(f"Запрос '{тип}' не был обработан.\n")

    def показать_меню(self):
        print("Выберите запрос:")
        print("1. Помощь с курсом")
        print("2. Внесение успеваемости")
        print("3. Утверждение учебной программы")
        print("4. Перевод студента в другую группу")
        print("5. Генерация отчета")
        print("0. Выход")


# Клиентский код
if __name__ == "__main__":
    система = СистемаДеканата()

    while True:
        система.показать_меню()
        выбор = input("Введите номер запроса: ").strip()

        if выбор == "1":
            система.обработать_запрос(
                "помощь_с_курсом", "Нужна помощь с материалом курса."
            )
        elif выбор == "2":
            система.обработать_запрос(
                "внесение_успеваемости", "Добавить оценки для группы."
            )
        elif выбор == "3":
            система.обработать_запрос(
                "утверждение_учебной_программы", "Программа для кафедры."
            )
        elif выбор == "4":
            система.обработать_запрос(
                "перевод_группы", "Перевести студента в другую группу."
            )
        elif выбор == "5":
            система.обработать_запрос(
                "генерация_отчета", "Создать отчет по успеваемости."
            )
        elif выбор == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.\n")

"""ИГРА МОРСКОЙ БОЙ (С КОМПЬЮТЕРОМ)"""

from random import randint


# 1. Класс точки.
class Dot:
    def __init__(self, x, y):  # Метод для обозначения точки по координатам "x" и "y".
        self.x = x
        self.y = y

    def __eq__(self, other):  # Метод сравнения точек между не только между собой, но и по кораблям.
        return self.x == other.x and self.y == other.y  # Сравнение точек между собой.


# 2. Класс исключений.
class FieldException(Exception):  # Общий класс исключений.
    pass


class FieldOutException(FieldException):  # Исключение если игрок стреляет за пределы поля.
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы поля!"


class FieldRepeatException(FieldException):  # Исключение если игрок уже стрелял по клетке.
    def __str__(self):
        return "Вы уже стреляли по этой клетке!"


class FieldWrongShipException(FieldException):  # Исключение если корабль не разместился в пределах поля.
    pass


# 3. Класс корабля.
class Ship:
    def __init__(self, bow, length, direction):  # Определяем параметры корабля.
        self.bow = bow  # Нос (начало) корабля.
        self.length = length  # Длина корабля.
        self.direction = direction  # Направление (горизонталь или вертикаль) корабля.
        self.health = length  # Здоровье корабля == его длине.

    @property  # Используется для определения свойств в классе.
    def dots(self):  # Метод точек.
        ship_dots = []  # Создаем пустой список для сбора точек при попадании по кораблям.
        for i in range(self.length):  # Проходим циклом по каждому элементу в длине корабля.
            current_x = self.bow.x  # Обозначение носа корабля по "x".
            current_y = self.bow.y  # Обозначение носа корабля по "y".

            if self.direction == 0:  # Если вертикальное расположение корабля.
                current_x += i  # Увеличивает каждый проход точки на i.

            elif self.direction == 1:  # Если горизонтальное расположение корабля.
                current_y += i  # Увеличивает каждый проход точки на i.

            ship_dots.append(Dot(current_x, current_y))  # В случае удачи, добавляем точки в список ship_dots.

        return ship_dots  # Если не удалось, то запускаем цикл снова.

    def shooted(self, shot):  # Метод стрелявшего.
        return shot in self.dots  # Возвращает выстрелы в метод точек dots.


# 4. Класс цветов. Добавил цветов, можно менять цвета любых элементов: корабли, точки, "X", текст и т.д.
class Color:
    green = '\033[92m'  # Зеленый яркий.
    greenB = '\033[1;92m'  # Зеленый яркий жирный.
    green2 = '\033[32m'  # Зеленый темный.
    green2B = '\033[1;32m'  # Зеленый темный жирный.

    yellow = '\033[93m'  # Желтый яркий.
    yellowB = '\033[1;93m'  # Желтый яркий жирный.
    yellow2 = '\033[33m'  # Желтый темный.
    yellow2B = '\033[1;33m'  # Желтый темный жирный.

    red = '\033[91m'  # Красный.
    redB = '\033[1;91m'  # Красный жирный.

    purple = '\033[95m'  # Фиолетовый яркий.
    purpleB = '\033[1;95m'  # Фиолетовый яркий жирный.
    purple2 = '\033[35m'  # Фиолетовый темный.
    purple2B = '\033[1;35m'  # Фиолетовый темный жирный.

    turquoise = '\033[96m'  # Бирюзовый яркий.
    turquoiseB = '\033[1;96m'  # Бирюзовый яркий жирный.
    turquoise2 = '\033[36m'  # Бирюзовый темный.
    turquoise2B = '\033[1;36m'  # Бирюзовый темный жирный.

    blue = '\033[94m'  # Голубой яркий.
    blueB = '\033[1;94m'  # Голубой яркий жирный.
    blue2 = '\033[34m'  # Голубой темный.
    blue2B = '\033[1;34m'  # Голубой темный жирный.

    gray = '\033[37m'  # Серый.
    reset = '\033[0m'  # Стандартный, сброс.


def set_color(letter, color):  # Метод применения цветов к элементам.
    return color + letter + Color.reset  # Цвет + символ или текст + сброс к заводским цветам.


# 5. Класс доски.
class Field:
    def __init__(self, hide=False, size=10):  # Передаем параметры, показывать свою доску, размер доски.
        self.hide = hide  # Отображение доски игрока.
        self.size = size  # Размер доски.

        self.count = 0  # Счетчик.

        self.field = [["_"] * size for _ in range(self.size)]  # С помощью генератора списка создаем поле равное size.
        self.busy = []  # Новый список с занятыми точками, от попаданий и промахов.
        self.ships = []  # Новый список с подбитыми кораблями.

    def add_ships(self, ship):  # Добавление корабля.
        for dot in ship.dots:  # Для каждой точки в ship.
            if self.out(dot) or dot in self.busy:  # Если точка попадает под условия в out или находится в списке busy.
                raise FieldWrongShipException()  # Исключение неверного расположения корабля на поле.
        for dot in ship.dots:  # Для каждой точки в ship.
            self.field[dot.x][dot.y] = set_color("■", Color.blue2)  # Ставим "■" по координатам "x" и "y"
            # (корабли окрашены через set_color).
            self.busy.append(dot)

        self.ships.append(ship)  # Добавляем в список собственных кораблей.
        self.contours(ship)  # Обходим контуры корабля точками.

    def contours(self, ship, choice=False):  # choice - отвечает за расстановку точек вокруг корабля.
        near = [  # Объявляем все точки в списке кортежей near, вокруг той в которой мы находимся.
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:  # Проходим по каждой точке циклом в ship.
            for dx, dy in near:  # Для каждой координаты в списке кортежей near.
                current = Dot(dot.x + dx, dot.y + dy)  # Сдвигаем координаты на 1 по "x" и "y".
                if not (self.out(current)) and current not in self.busy:  # Если точка не выходит за out (границы поля)
                    # и не занята то.
                    if choice:  # choice - отвечает за расстановку точек вокруг корабля.
                        self.field[current.x][current.y] = set_color("•", Color.yellow)  # Ставим точку на месте
                        # координат ниже ("•" окрашена через set_color).
                    self.busy.append(current)  # Добавляем текущие координаты точки в список busy.

    def __str__(self):  # Добавил немного красок для лучшей визуализации.
        result = set_color("•", Color.green2)
        result += " | \033[32m0\033[0m | \033[32m1\033[0m | \033[32m2\033[0m | \033[32m3\033[0m | \033[32m4\033[0m |" \
                  " \033[32m5\033[0m | \033[32m6\033[0m | \033[32m7\033[0m | \033[32m8\033[0m | \033[32m9\033[0m |"
        for i, row in enumerate(self.field):
            result += f"\033[32m\n{i}\033[0m | " + " | ".join(row) + " |"

        if self.hide:
            result = result.replace("■", "\033[0m_")  # Заменяем символы корабля "■" на пустые символы "_" (reset цвет).
        return result

    def out(self, dot):  # Метод out, для определения точек, не находятся ли за пределами поля.
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))  # Ничего не возвращаем если условие верно.

    def shot(self, dot):  # Метод shot.
        if self.out(dot):  # Проверяем если попал за пределы поля.
            raise FieldOutException()  # Исключение, что попал за пределы поля.

        if dot in self.busy:  # Если точка уже в списке busy, то.
            raise FieldRepeatException()  # Исключение, что уже стрелял по этой клетке.

        self.busy.append(dot)  # Далее добавляем точку в busy, если она не была занята ранее.

        for ship in self.ships:  # Проходим в цикле по списку с подбитыми кораблями.
            if dot in ship.dots:  # Если точка находится в ship.dots.
                ship.health -= 1  # Здоровье корабля = - 1.
                self.field[dot.x][dot.y] = set_color("X", Color.redB)  # На место точки ставится "X" ("X" окрашен через
                # set_color).
                if ship.health == 0:  # Если здоровье корабля == 0.
                    self.count += 1  # Прибавляем к счетчику уничтоженных кораблей 1.
                    self.contours(ship, choice=True)  # Обводим контур корабля точками.
                    print("Корабль уничтожен!")  # Выводим сообщение.
                    return False
                else:
                    print("Корабль ранен!")  # Выводим сообщение.
                    return True  # Повторяем ход.

        self.field[dot.x][dot.y] = set_color("•", Color.yellow)  # Если ни один корабль не был поражен, ставим точку по
        # координатам ("•" окрашена через set_color).
        print("Мимо!")  # Выводим сообщение.
        return False

    def begin(self):  # Функция начала игры.
        self.busy = []  # Обнуляем список busy, для хранения точек игрока.


# 6. Класс игрока.
class Player:
    def __init__(self, field, enemy):  # Параметры: доска игрока, доска компьютера.
        self.field = field  # Доска игрока.
        self.enemy = enemy  # Доска компьютера.

    def ask(self):
        raise NotImplementedError()  # Исключение, возникающее в случаях, когда наследник класса не переопределил
        # метод, который должен был.

    def move(self):
        while True:  # Запускаем вечный цикл для постоянных выстрелов.
            try:  # Проверка исключением.
                target = self.ask()  # Просим компьютер или игрока дать координаты.
                repeat = self.enemy.shot(target)  # Выполняем выстрел.
                return repeat  # Если выстрел прошёл удачно, повторяем выстрел.
            except FieldException as e:  # Если нет то.
                print(e)  # Исключение и цикл продолжается.


# 7. Класс компьютера.
class AI(Player):  # Компьютерный игрок.
    def ask(self):  # Спрашиваем координаты точек.
        d = Dot(randint(0, 8), randint(0, 8))  # random, случайно генерит точки в диапазоне от 0 до 8 по "x" и "y".
        print(f"Ход компьютера: {d.x} {d.y}")  # Выводим сообщение с координатами.
        return d  # Возвращаем точки.


# 8. Класс пользователя.
class User(Player):  # Пользователь.
    def ask(self):  # Спрашиваем координаты точек.
        while True:  # Запускаем вечный цикл.
            cords = input("Ваш ход: ").split()  # Вводим координаты, через сплит разделяем 2 цифры.

            if len(cords) != 2:  # Если кол-во координат не равно 2, то.
                print(" Введите 2 координаты! ")  # Пишем сообщение.
                continue

            x, y = cords  # Присваиваем координаты "x" и "y".

            if not (x.isdigit()) or not (y.isdigit()):  # Проверка, если координаты "x" или "y" не цифры.
                print(" Введите числа! ")  # Пишем сообщение.
                continue

            x, y = int(x), int(y)  # Переводим "x" и "y" в целочисленный формат.

            return Dot(x, y)  # Возвращаем точки по индексам.


# 9. Класс игры.
class Game:
    def __init__(self, size=10):
        self.size = size
        pl = self.random_field()
        co = self.random_field()
        co.hide = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_field(self):
        field = None
        while field is None:
            field = self.random_place()
        return field

    def random_place(self):  # Расстановка кораблей.
        lens = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Длина кораблей, точнее кол-во и их разновидность.
        field = Field(size=self.size)  # Длина доски == длине.
        attempts = 0  # Попытки.
        for length in lens:  # Для каждой точки в списке lens.
            while True:  # Запускаем вечный цикл.
                attempts += 1  # С каждым проходом увеличиваем попытку на + 1.
                if attempts > 2000:  # Если попыток больше 2000.
                    return None  # Ничего не возвращаем.
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))  # Расстановка
                # кораблей с помощью random.
                try:  # Проверка исключением.
                    field.add_ships(ship)  # Если все хорошо, корабль поставился то.
                    break  # Останавливаем цикл.
                except FieldWrongShipException:  # Если нет, то исключение.
                    pass
        field.begin()  # Вызываем доску с началом игры.
        return field  # Запускаем цикл заново.

    def greetings(self):
        print("-" * 43)
        print("|", set_color("           ИГРА МОРСКОЙ БОЙ            ".center(6), Color.yellowB), "|")
        print("-" * 43)
        print("|            \033[1;93mФормат ввода:\033[0m \033[1;34mx\033[0m \033[1;36my\033[0m"
              "            |".center(6))
        print("|", set_color("          'x' - номер строки           ".center(6), Color.blue2B), "|")
        print("|", set_color("          'y' - номер столбца          ".center(6), Color.turquoise2B), "|")

    def loop(self):
        num = 0
        while True:
            print("-" * 43)
            print("|", set_color("                 ИГРОК                 ".center(6), Color.blue2B), "|")
            print("-" * 43)
            print(self.us.field)
            print("-" * 43)
            print("|", set_color("               КОМПЬЮТЕР               ".center(6), Color.redB), "|")
            print("-" * 43)
            print(self.ai.field)
            if num % 2 == 0:
                print("-" * 43)
                print("              ( Ход игрока )                ".center(6))
                print("-" * 43)
                repeat = self.us.move()
            else:
                print("-" * 43)
                print("            ( Ход компьютера )             ".center(6))
                print("-" * 43)
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.field.count == 7:
                print("-" * 43)
                print("Игрок выиграл!")
                break

            if self.us.field.count == 7:
                print("-" * 43)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greetings()
        self.loop()


g = Game()
g.start()

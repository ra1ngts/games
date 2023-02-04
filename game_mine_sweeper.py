"""ИГРА САПЕР"""
from random import randint


class BoardException(Exception):
    """Общий класс исключений."""
    pass


class BoardOutException(BoardException):
    """Исключение если игрок стреляет за пределы поля."""

    def __str__(self):
        """
        Метод строки.
        :return: Возврат координат.
        """
        return "Вы называете координаты за пределами доски!"


class BoardUsedException(BoardException):
    """Исключение если повторно стрелял по клетке."""

    def __str__(self):
        """
        Метод строки.
        :return: Возврат координат.
        """
        return "Вы уже называли эти координаты!"


class BoardWrongMineException(BoardException):
    """Исключение если мина не разместилась в пределах доски."""
    pass


class Color:
    """Класс выбора цвета для элементов."""
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


class Dot:
    """Класс определения точки."""

    def __init__(self, x, y):
        """
        Устанавливает параметры для класса Dot.
        :param x: Координата по оси "x".
        :param y: Координата по оси "y".
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Сравнение точек между собой.
        :param other: Сравнение точек "x" и "y" с "other".
        :return: Возврат сравнения.
        """
        return self.x == other.x and self.y == other.y  # Сравнение точек между собой.

    def __repr__(self):
        """
        Метод для отладки.
        :return: Возврат точек "x" и "y".
        """
        return f"Dot({self.x}, {self.y})"


class Mine:
    """Класс по созданию мины."""

    def __init__(self, start, length):
        """
        Устанавливает параметры для мины.
        :param start: Начало мины.
        :param length: Длина мины, которая равна ее здоровью.
        """
        self.start = start  # Начало мины.
        self.length = length  # Длина мины.
        self.health = length  # Здоровье мины == длине мины.

    @property
    def dots(self):
        """
        Метод по сбору точек.
        :return: Возврат списка mine_dots.
        """
        mine_dots = []  # Создаем пустой список для сбора точек при попадании по мине.
        for i in range(self.length):  # Проходим циклом по длине мины.
            current_x = self.start.x  # Обозначение начала мины по "x".
            current_y = self.start.y  # Обозначение начала мины по "y".
            mine_dots.append(Dot(current_x, current_y))  # В случае удачи, добавляем точки в список mine_dots.
        return mine_dots  # Если не удалось, то запускаем цикл снова.

    def shooted(self, shot):
        """
        Метод стрелявшего.
        :param shot: Делает выстрел.
        :return: Возврат выстрелов.
        """
        return shot in self.dots  # Возвращает выстрелы в метод точек dots.


class Board:
    """Класс создания игровой доски."""

    def __init__(self, hide=True, size=5):
        """
        Устанавливает параметры доски.
        :param hide: Скрываем / Не скрываем доску от игрока.
        :param size: Размер самой доски.
        """
        self.hide = hide  # Нужно ли скрывать нашу доску.
        self.size = size  # Размер доски.
        self.count = 0  # Счетчик пораженных мин.
        self.board = [["_"] * size for _ in range(size)]  # Генератор списка с учетом заданных параметров.
        self.busy = []  # Занятые минами точки, или куда уже стреляли.
        self.mine = []  # Список мин на доске.
        self.scores = []  # Список с очками игрока.

    def __str__(self):
        """
        Метод создания разлиновки игровой доски.
        :return: Возврат доски.
        """
        res = ""
        res += "  | \033[94m1\033[0m | \033[94m2\033[0m | \033[94m3\033[0m | \033[94m4\033[0m | \033[94m5\033[0m |"
        for i, row in enumerate(self.board):
            res += f"\n\033[94m{i + 1}\033[0m | " + " | ".join(row) + " | "
        if self.hide:  # Если условие истинно, то скрываем нашу доску.
            res = res.replace("⊛", "_")  # Заменяем символы "⊛", на "_".
        return res  # Возвращаем.

    def out(self, d):
        """
        Метод проверки точек в пределах доски.
        :param d: Точка по оси "x" и "y".
        :return: Не возвращать если точки в правильном диапазоне координат.
        """
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))  # Не возвращаем точки, если они в нужном
        # диапазоне.

    def add_mine(self, mine):
        """
        Метод добавления мин.
        :param mine: Мина.
        :return: Возврат если попал на мину.
        """
        for d in mine.dots:  # Перебираем каждую точку в dots.
            if self.out(d) or d in self.busy:  # Если точка находится за пределами поля или в списке busy.
                raise BoardWrongMineException()  # Вызываем исключение.
        for d in mine.dots:  # Если точка существует, то.
            self.board[d.x][d.y] = "⊛"  # Ставим мину -> "⊛".
            self.busy.append(d)  # Добавляем точку в список busy.
        self.mine.append(mine)  # Добавляем в список mine.

    def shot(self, d):
        """
        Метод выстрела.
        :param d: Точка по оси "x" и "y".
        :return: Возврат если не попал на мину.
        """
        if self.out(d):  # Если точка выходит за границы доски, то:
            raise BoardOutException  # вызываем исключение.

        if d in self.busy:  # Если точка находится в busy, то:
            raise BoardUsedException  # вызываем исключение.

        self.busy.append(d)  # Если все хорошо, то добавляем точку в список busy.

        for mine in self.mine:  # Для мины в списке.
            if mine.shooted(d):  # Метод стрелка.
                mine.health -= 1  # Если попал на мину, то игра заканчивается.
                self.board[d.x][d.y] = "⊛"  # Мина -> "⊛".
                if mine.health == 0:  # Если жизнь мины == 0.
                    self.count += 1  # Добавляем в счетчик пораженных мин.
                    return True  # Возвращаем истину.

        self.board[d.x][d.y] = "\033[93m•\033[0m"  # Если не попали на мину, то ставим -> "•".
        self.scores.append(1)  # Добавляем очко в список scores, для сбора очков.
        print(f"Количество текущих очков: {sum(self.scores)}")  # Выводим текущее количество очков.
        if sum(self.scores) == 21:  # Если количество очков == 21, то:
            print(f"ПОЗДРАВЛЯЕМ! Вы набрали {sum(self.scores)} очков! ИГРА ОКОНЧЕНА!")  # Выводим сообщение с
            # поздравлением и окончанием игры.
        return False

    def begin(self):
        """
        Метод запуска.
        """
        self.busy = []  # Обнуляем список busy.


class Player:
    """Класс игрока."""

    def __init__(self, player_board):
        """
        Устанавливает доску игрока.
        :param player_board: Доска игрока.
        """
        self.player_board = player_board

    def ask(self):
        """Метод запросов."""
        raise NotImplementedError()  # Метод который должен быть у потомков этого класса.

    def move(self):
        """Метод хода."""
        while True:  # Выводим бесконечный цикл.
            try:  # Пытаемся делать постоянные выстрелы.
                target = self.ask()  # Просим координаты выстрела.
                repeat = self.player_board.shot(target)  # Повторяем выстрел.
                return repeat  # Если попали по свободным точкам, то повторяем.
            except BoardException as e:  # Если нет, то вызываем исключение.
                print(e)


class User(Player):
    """Класс пользователя. Наследуется от класса Player."""

    def ask(self):
        """
        Метод запросов.
        :return: Возврат точки по "x" и "y" с учетом -1. Для корректного отображения на доске по индексу.
        """
        while True:  # Запускаем бесконечный цикл.
            coordinates = input("Введите две координаты по 'x' и 'y': ").split()  # Запрашиваем координаты у игрока.
            if len(coordinates) != 2:  # Если координат больше или меньше двух, то:
                print("Введите две координаты!")  # выводим сообщение.
                continue  # Продолжаем.
            x, y = coordinates  # Присваиваем "x" и "y" координатам.

            if not (x.isdigit()) or not (y.isdigit()):  # Проверяем если координаты не числа.
                print("Введите числа!")  # Выводим сообщение.
                continue  # Продолжаем.

            x, y = int(x), int(y)  # Присваиваем координатам формат int.

            return Dot(x - 1, y - 1)  # Возвращаем за -1, чтобы корректно считалось по индексу.


class Game:
    """Класс создания игры."""

    def __init__(self, size=5):
        """
        Устанавливает размер генерируемой доски.
        :param size:
        """
        self.mines = [1, 1, 1, 1]  # Количество мин.
        self.size = size  # Размер генерируемой доски.
        player = self.random_board()  # Генерация самой доски.
        self.user = User(player)  # Генерация доски для игрока.

    def try_board(self):  # Метод создания доски.
        """
        Метод создания(генерации) доски.
        :return: Возврат игровой доски.
        """
        board = Board(size=self.size)  # Доска размером == size.
        attempts = 0  # Попытки создания.
        for i in self.mines:  # Запускаем цикл.
            while True:  # Вечный цикл.
                attempts += 1  # Каждый раз увеличиваем попытки на 1.
                if attempts > 2000:  # Если попыток > 2000.
                    return None  # Ничего не возвращаем.
                mine = Mine(Dot(randint(0, self.size), randint(0, self.size)), i)  # Задаем координаты нашим минам
                # на поле.
                try:
                    board.add_mine(mine)  # Добавляем мины.
                    break
                except BoardWrongMineException:  # Если не получилось, то вызываем исключение.
                    pass

        board.begin()  # Запускаем доску.
        return board

    def random_board(self):
        """
        Метод по созданию доски, если метод try_board не сработал корректно.
        :return: Возврат игровой доски.
        """
        board = None  # Если доска пустая.
        while board is None:  # Вечный цикл, если пустая доска.
            board = self.try_board()  # Пытаемся создать доску снова.
        return board

    @staticmethod
    def greetings():
        """Метод приветствия игрока. А так же инструкция по вводу координат "x" и "y"."""
        print("-" * 23)
        print("|     \033[1;93mИГРА САПЕР\033[0m      |")
        print("-" * 23)
        print("|    \033[1;34mПРИМЕР ВВОДА:\033[0m    |")
        print("-" * 23)
        print("|     \033[1;35mСТРОКА:\033[0m \033[1;95m'x'\033[0m     |")
        print("|    \033[1;34mСТОЛБЕЦ:\033[0m \033[1;94m'y'\033[0m     |")

    def loop(self):
        """Метод запуска игрового цикла."""
        num = 20  # Дается количество ходов в зависимости от размера доски.
        while True:  # Вечный цикл.
            print("-" * 23)
            print("|    \033[1;35mИГРОВОЕ ПОЛЕ\033[0m     |")
            print("-" * 23)
            print(self.user.player_board)  # Доска игрока.
            if num % 2 == 0 or num % 2 != 0:  # Постоянный ход игрока.
                print("-" * 23)
                print()
                repeat = self.user.move()  # Запускаем метод бесконечных ходов, пока не откроем все пустые ячейки или,
                # не наступим на мину.
                if repeat:  # При удачном попадании по пустым ячейкам, ход повторяется.
                    num -= 1  # Количество ходов уменьшается на 1.
            if num == 0:  # Если счетчик == 0, то:
                break  # цикл останавливается.

            if self.user.player_board.count == 1:  # Если наступили хотя бы на одну мину, то игра завершается.
                print()
                print("-" * 37)
                print("Вы наступили на МИНУ! ИГРА ОКОНЧЕНА!")
                print(f"       Вы не заработали очков.")  # Все очки сгорают при попадании на мину.
                print("-" * 37)
                break
            num -= 1

    def start(self):
        """Метод по запуску игры."""
        self.greetings()  # Приветствие и инструкция по игре.
        self.loop()  # Запуск игрового цикла.


g = Game()
g.start()

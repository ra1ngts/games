"""ИГРА В КРЕСТИКИ - НОЛИКИ (ДЛЯ 2 ИГРОКОВ)"""
# Создаем игровое поле в виде генератора пустого списка.
board = [" " * 1 for i in range(9)]
# Создаем выигрышные комбинации (привязка идет к позиции клетки, а не индексам).
win_comb = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]


# 1. Создаем функцию отрисовки игрового поля с помощью print(), а так же оформляем и выводим 'Пример ввода'
# для подсказки.
# Центровку граф осуществляем с помощью метода .center(). Поиск нужной клетки осуществляется с помощью индексов.
# Ввод осуществляется с помощью только - 'ОДНОЙ' цифры (позиции)!
def draw_board():
    print()
    print(" -------------------".center(3))
    print(" |  ПРИМЕР ВВОДА:  |".center(3))
    print(" -------------------".center(3))
    print(" |  " '1' "  |  " '2' "  |  " '3' "  |  ")
    print(" |  " '4' "  |  " '5' "  |  " '6' "  |  ")
    print(" |  " '7' "  |  " '8' "  |  " '9' "  |  ")
    print(" -------------------".center(3))
    print(" | КРЕСТИКИ-НОЛИКИ |".center(3))
    print(" -------------------".center(3))
    for i in range(3):
        print("|".center(3), board[0 + i * 3], "|".center(3), board[1 + i * 3], "|".center(3), board[2 + i * 3],
              "|".center(3))
        print(" -------------------".center(3))


# 2. Создаем функцию ввода символа, а так же проверки на ввод допустимых символов (в данном случае только
# цифры от 1 до 9 включительно. Так же осуществляем проверку на заполненность клеток.
def take_input(player_choice):
    while True:  # Запускаем вечный цикл.
        value = input("В какую клетку поставить символ - " + player_choice + "? ")  # Ввод цифр от 1 до 9 включительно.
        if not (value in "123456789"):  # Проверка на корректный ввод (только цифры). Использовал метод строки.
            print("Вы ввели недопустимый символ. Повторите.")  # Если ввод некорректный, то есть либо символы либо
            # 2 знака, пишем сообщение о 'недопустимом' символе.
            continue  # Заново запрашиваем ввод команды - value = input(....).
        value = int(value)  # Приводим строку к типу int.
        if str(board[value - 1]) in "XO":  # Проверка на заполненность клетки.
            print("Клетка уже занята!")  # Если клетка оказалась занятой, выводим сообщение о занятости клетки.
            continue  # Заново запрашиваем ввод команды - value = input(....).
        board[value - 1] = player_choice  # Если клетка свобода, записываем ее в наш список.
        break  # Остановка цикла.


# 3. Создаем функцию проверки выигрышных комбинаций с помощью цикла, проходим по всем индексам из списка win_comb.
def check_win():
    for each in win_comb:  # Для каждого 'объекта' в win_comb (цикл)
        if (board[each[0] - 1]) == (board[each[1] - 1]) == (board[each[2] - 1]):  # Если по индексам в первой
            # строке совпали все три числа: |  0  |  1  |  2  | = |  1  |  2  |  3  |
            return board[each[1] - 1]  # Возвращаем значение в доске.
    else:
        return False  # Если нет, то возвращаем False.


# 4. Создаем основную или главную функцию с телом программы.
def main():
    counter = 0  # Создаем счетчик для нумерации ходов.
    while True:  # Запускаем цикл.
        draw_board()  # Выводим функцию draw_board() для показа игрового поля.
        if counter % 2 == 0:  # Последовательность ходов. Если четный, первым ходит - 'X', если не четный - 'O'.
            take_input("X")  # Каждый четный ход ходят 'X'.
        else:
            take_input("O")  # Каждый не четный ходят 'O'.
        if counter > 3:  # Если ходов сделано больше трех, то:
            winner = check_win()  # Проверяем выигрышные комбинации.
            if winner:  # Если есть совпадение, то есть победа то:
                draw_board()  # Перерисовываем поле с последними результатами.
                print(f"{winner} Выиграл!")  # И выводим на экран сообщение - 'Кто' 'Выиграл' !
                break  # Выход из цикла
        counter += 1  # Если ходов еще не больше верхнего условия то-есть > 3.
        if counter > 8:  # Если кол-во ходов больше 8 и верхние условия не совпали.
            draw_board()  # Еще раз выводим поле на экран.
            print("Ничья!")  # И выводим сообщение - 'Ничья' !
            break  # Выход из цикла.


main()  # Запуск программы.

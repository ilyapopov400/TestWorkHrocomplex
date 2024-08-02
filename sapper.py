"""
- Сапер
"""
import random


class GamePole:
    """
    - который будет создавать и управлять игровым полем
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, n: int, m: int, total_mines: int):
        self.n = n  # строки
        self.m = m  # столбцы
        self.total_mines = total_mines
        self.__pole_cells = tuple(
            tuple(Cell() for _ in range(m)) for _ in range(n)
        )

    @property
    def pole(self):
        return self.__pole_cells

    def __del__(self):
        self.__class__.__instance = None

    def __neighbours(self, nn: int, mm: int) -> list:
        """
        - получаем координаты соседних клеток
        :param nn:
        :param mm:
        :return:
        """
        result = list()
        for n in range(self.n):
            for m in range(self.m):
                if n == nn and m == mm:
                    continue
                hypotenuse = (
                                     (nn - n) ** 2 + (mm - m) ** 2
                             ) ** 0.5
                if hypotenuse <= (2 ** 0.5):
                    result.append(
                        (n, m)
                    )
        return result

    def init_pole(self) -> None:
        """
        - для инициализации начального состояния игрового поля
        (расставляет мины и делает все клетки закрытыми)
        :return: None
        """
        list_of_mind = [True for _ in range(self.total_mines)] + [False for _ in
                                                                  range(self.n * self.m - self.total_mines)]
        random.shuffle(list_of_mind)  # перемешали список для выбора клетки с миной
        for nn in self.__pole_cells:  # расставили мины
            for mm in nn:
                mm.is_mine = list_of_mind.pop()

        for nn in range(self.n):
            for mm in range(self.m):
                count_mine = 0
                for n, m in self.__neighbours(nn, mm):  # список соседских клеток
                    if not self.__pole_cells[n][m]:
                        count_mine += 1
                self.__pole_cells[nn][mm].number = count_mine

    def open_cell(self, n: int, m: int) -> bool:
        """
        - открывает ячейку с индексами (n, m);
        нумерация индексов начинается с нуля;
        метод меняет значение атрибута __is_open объекта Cell в ячейке (n, m) на True  и всех клеток вокруг!
        """
        if not isinstance(n, int) or not isinstance(m, int) or n < 0 or m < 0 or n > self.n or m > self.m:
            raise IndexError('некорректные индексы i, j клетки игрового поля')
        cell = self.__pole_cells[n][m]
        cell.is_open = True  # открыли заданную клетку
        for neighbours in self.__neighbours(nn=n, mm=m):  # открыли клетки вокруг
            self.__pole_cells[neighbours[0]][neighbours[1]].is_open = True
        return cell

    def wine_game(self):
        result = list()
        count_mine = 0
        for i in self.__pole_cells:
            for j in i:
                result.append(j.is_open)
                if j.is_mine and j.is_open:
                    count_mine += 1
                if count_mine == self.total_mines:
                    return True

        return all(result)

    def show_pole(self) -> None:
        """
        - отображает игровое поле в консоли
        (как именно сделать - на ваше усмотрение, этот метод - домашнее задание)
        :return:
        """
        for st in self.__pole_cells:
            [print(cell, end="  ") for cell in st]
            print()


class Cell:
    def __init__(self) -> None:
        self.__is_mine = False  # - булево значение True/False; True - в клетке находится мина, False - мина отсутствует
        self.__number = 0  # - число мин вокруг клетки (целое число от 0 до 8)
        self.__is_open = False  # - флаг того, открыта клетка или закрыта: True - открыта; False - закрыта

    def __str__(self):
        if self.is_open:
            if self.is_mine:
                return "M"
            return str(self.number)
        else:
            return "."

    @property
    def is_mine(self):
        return self.__is_mine

    @is_mine.setter
    def is_mine(self, is_mine: bool):
        if not isinstance(is_mine, bool):
            raise ValueError("должно быть булево значение True/False")
        self.__is_mine = is_mine

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number: int):
        if not isinstance(number, int):
            raise ValueError("должно быть целое число от 0 до 8")
        if number not in range(0, 9):
            raise ValueError("должно быть целое число от 0 до 8")
        self.__number = number

    @property
    def is_open(self):
        return self.__is_open

    @is_open.setter
    def is_open(self, is_open: bool):
        if not isinstance(is_open, bool):
            raise ValueError("должно быть булево значение True/False")
        self.__is_open = is_open

    def __bool__(self):
        return not self.__is_mine


def mane():
    pole = GamePole(n=4, m=5, total_mines=3)
    pole.init_pole()
    pole.show_pole()

    while True:
        n = input("Наберите номер строки ")
        m = input("Наберите номер столбца ")
        if not n or not m:
            print("До свиданья!")
            break
        else:
            n = int(n) - 1
            m = int(m) - 1
            if not pole.open_cell(n=n, m=m):
                print("Вы нарвались на мину!!!")
                pole.show_pole()
                break
            if pole.wine_game():
                print("Вы выиграли!!!!!")
                pole.show_pole()
                break

            pole.show_pole()


if __name__ == "__main__":
    mane()

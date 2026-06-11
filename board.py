from cells import (
    Go, Property, Tax, Chance, CommunityChest,
    Jail, GoToJail, FreeParking
)

class Board:
    def __init__(self):
        self.cells = self._create_board()
        self.size = len(self.cells)

    def _create_board(self):
        board = []
        board.append(Go("СТАРТ (получи 200₽ и катись)"))
        board.append(Property("Улица Ленивых котов", 60, 2, "коричневый"))
        board.append(CommunityChest("Щедрая кубышка (или нет)"))
        board.append(Property("Проспект Разбитых надежд", 60, 4, "коричневый"))
        board.append(Tax("Налог на воздух", 200))
        board.append(Property("Железная дорога «Чух-чух-самолёт»", 200, 25, "ж/д"))
        board.append(Property("Восточный базар", 100, 6, "голубой"))
        board.append(Chance("Везение-невезение"))
        board.append(Property("Вермонтский сыровар", 100, 6, "голубой"))
        board.append(Property("Коннектикутский тайник", 120, 8, "голубой"))
        board.append(Jail("Тюрьма «Буханка хлеба»"))
        board.append(Property("Площадь Сломанного телефона", 140, 10, "розовый"))
        board.append(Property("Энергетическая яма (коммуналка)", 150, 20, "коммунальная"))
        board.append(Property("Авеню Бесплатного сыра", 140, 10, "розовый"))
        board.append(Property("Виргинский шкаф", 160, 12, "розовый"))
        board.append(Property("Пенсильванская колбасная", 200, 25, "ж/д"))
        board.append(CommunityChest("Сундук скелета"))
        board.append(Property("Площадь Скунса", 180, 14, "оранжевый"))
        board.append(Chance("Удача пришла, ура!"))
        board.append(Property("Теннессийский самогон", 180, 14, "оранжевый"))
        board.append(Property("Нью-Йоркский пончик", 200, 16, "оранжевый"))
        board.append(FreeParking("Парковка для единорогов"))
        board.append(Property("Кентуккийский петух", 220, 18, "красный"))
        board.append(Chance("Нежданчик"))
        board.append(Property("Индианская соусная", 220, 18, "красный"))
        board.append(Property("Иллинойский Лось", 240, 20, "красный"))
        board.append(GoToJail("Лети в тюрьму, не промахнись"))
        return board

    def get_cell(self, position):
        return self.cells[position]

    def get_jail_position(self):
        for i, cell in enumerate(self.cells):
            if isinstance(cell, Jail):
                return i
        return 10  
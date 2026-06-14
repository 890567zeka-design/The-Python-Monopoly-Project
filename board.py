from cells import Property, Tax, CellFactory


class Board:
    def __init__(self):
        self.factory = CellFactory()
        self.cells = self._create_board()
        self.size = len(self.cells)

    def _create_board(self):
        board = []

        board.append(self.factory.create_go("СТАРТ"))
        board.append(Property("Средиземноморский проспект", 60, 2, "коричневый"))
        board.append(self.factory.create_community_chest("Общественная казна"))
        board.append(Property("Балтийский проспект", 60, 4, "коричневый"))
        board.append(Tax("Налог на доход", 200))
        board.append(Property("Читающая железная дорога", 200, 25, "ж/д"))
        board.append(Property("Восточный проспект", 100, 6, "голубой"))
        board.append(self.factory.create_chance("Шанс"))
        board.append(Property("Вермонтский проспект", 100, 6, "голубой"))
        board.append(Property("Коннектикутский проспект", 120, 8, "голубой"))
        board.append(self.factory.create_jail("Тюрьма"))
        board.append(Property("Сент-Чарльз-плейс", 140, 10, "розовый"))
        board.append(Property("Электрическая компания", 150, 20, "коммунальная"))
        board.append(Property("Стейтс-авеню", 140, 10, "розовый"))
        board.append(Property("Виргиния-авеню", 160, 12, "розовый"))
        board.append(Property("Пенсильванская железная дорога", 200, 25, "ж/д"))
        board.append(self.factory.create_community_chest("Общественная казна"))
        board.append(Property("Сент-Джеймс-плейс", 180, 14, "оранжевый"))
        board.append(self.factory.create_chance("Шанс"))
        board.append(Property("Теннесси-авеню", 180, 14, "оранжевый"))
        board.append(Property("Нью-Йорк-авеню", 200, 16, "оранжевый"))
        board.append(self.factory.create_free_parking("Бесплатная стоянка"))
        board.append(Property("Кентукки-авеню", 220, 18, "красный"))
        board.append(self.factory.create_chance("Шанс"))
        board.append(Property("Индиана-авеню", 220, 18, "красный"))
        board.append(Property("Иллинойс-авеню", 240, 20, "красный"))
        board.append(self.factory.create_go_to_jail("Идите в тюрьму"))
        board.append(Property("Атлантик-авеню", 260, 22, "жёлтый"))
        board.append(Property("Вентнор-авеню", 260, 22, "жёлтый"))
        board.append(Property("Марвин-гарденс", 280, 24, "жёлтый"))

        return board

    def get_cell(self, position):
        return self.cells[position]

    def get_jail_position(self):
        for i, cell in enumerate(self.cells):
            if cell.cell_type == "jail":
                return i
        return 10

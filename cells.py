class Cell:
    """Базовый класс для всех клеток."""

    def __init__(self, name: str, cell_type: str = "simple"):
        self.name = name
        self.cell_type = cell_type

    def land_on(self, player, game):
        """Действие при попадании на клетку. Переопределяется в зависимости от типа."""
        if self.cell_type == "property":
            self._handle_property(player, game)
        elif self.cell_type == "tax":
            self._handle_tax(player, game)
        elif self.cell_type == "chance":
            game.draw_chance_card(player)
        elif self.cell_type == "community":
            game.draw_community_chest_card(player)
        elif self.cell_type == "jail":
            if not player.in_jail:
                game.ui.message(f"{player.name} посетил тюрьму (просто зашёл в гости).")
        elif self.cell_type == "go_to_jail":
            player.in_jail = True
            player.position = game.board.get_jail_position()
            game.ui.message(f"{player.name} отправляется в тюрьму!")
        elif self.cell_type == "free_parking":
            pass
        elif self.cell_type == "go":
            pass

    def _handle_property(self, player, game):
        """Обработка попадания на клетку-собственность ."""
        if self.owner is None:
            game.ui.prompt_buy_property(player, self)
        elif self.owner != player and not self.mortgaged:
            if not player.pay(self.rent, self.owner):
                game.handle_bankruptcy(player)

    def _handle_tax(self, player, game):
        """Обработка попадания на налоговую клетку."""
        if not player.pay(self.amount):
            game.handle_bankruptcy(player)

    def __str__(self):
        if self.cell_type == "property":
            owner_name = self.owner.name if self.owner else "свободна"
            return f"{self.name} ({self.price}₽) владелец: {owner_name}"
        return self.name


class Property(Cell):
    """Класс для покупаемых улиц ."""

    def __init__(self, name: str, price: int, rent: int, color: str = ""):
        super().__init__(name, cell_type="property")
        self.price = price
        self.rent = rent
        self.color = color
        self.owner = None
        self.mortgaged = False


class Tax(Cell):
    """Класс для налоговых клеток."""

    def __init__(self, name: str, amount: int):
        super().__init__(name, cell_type="tax")
        self.amount = amount


class CellFactory:
    """Фабрика для создания клеток разных типов."""

    def create_go(self, name: str) -> Cell:
        """Создаёт клетку СТАРТ."""
        return Cell(name, cell_type="go")

    def create_chance(self, name: str) -> Cell:
        """Создаёт клетку Шанс."""
        return Cell(name, cell_type="chance")

    def create_community_chest(self, name: str) -> Cell:
        """Создаёт клетку Общественная казна."""
        return Cell(name, cell_type="community")

    def create_jail(self, name: str) -> Cell:
        """Создаёт клетку Тюрьма."""
        return Cell(name, cell_type="jail")

    def create_go_to_jail(self, name: str) -> Cell:
        """Создаёт клетку Отправка в тюрьму."""
        return Cell(name, cell_type="go_to_jail")

    def create_free_parking(self, name: str) -> Cell:
        """Создаёт клетку Бесплатная стоянка."""
        return Cell(name, cell_type="free_parking")

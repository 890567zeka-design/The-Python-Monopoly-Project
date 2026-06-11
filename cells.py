class Cell:
    def __init__(self, name: str):
        self.name = name

    def land_on(self, player, game):
        raise NotImplementedError


class Property(Cell):
    def __init__(self, name: str, price: int, rent: int, color: str = ""):
        super().__init__(name)
        self.price = price
        self.rent = rent
        self.color = color
        self.owner = None
        self.mortgaged = False

    def land_on(self, player, game):
        if self.owner is None:
            game.ui.prompt_buy_property(player, self)
        elif self.owner != player and not self.mortgaged:
            if not player.pay(self.rent, self.owner):
                game.handle_bankruptcy(player)

    def __str__(self):
        owner_name = self.owner.name if self.owner else "свободна"
        return f"{self.name} ({self.price}₽) владелец: {owner_name}"


class Tax(Cell):
    def __init__(self, name: str, amount: int):
        super().__init__(name)
        self.amount = amount

    def land_on(self, player, game):
        if not player.pay(self.amount):
            game.handle_bankruptcy(player)


class Chance(Cell):
    def land_on(self, player, game):
        game.draw_chance_card(player)


class CommunityChest(Cell):
    def land_on(self, player, game):
        game.draw_community_chest_card(player)


class Go(Cell):
    def land_on(self, player, game):
        pass


class Jail(Cell):
    def land_on(self, player, game):
        if not player.in_jail:
            game.ui.message(f"{player.name} посетил тюрьму (просто зашёл в гости).")


class GoToJail(Cell):
    def land_on(self, player, game):
        player.in_jail = True
        player.position = game.board.get_jail_position()
        game.ui.message(f"{player.name} отправляется в тюрьму!")


class FreeParking(Cell):
    def land_on(self, player, game):
        pass
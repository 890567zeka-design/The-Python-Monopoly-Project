class Player:
    """Игрок: деньги, позиция, собственность и состояние."""

    def __init__(self, name: str):
        self.name = name
        self.money = 1500        
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.bankrupt = False

    def pay(self, amount: int, receiver=None) -> bool:
        if self.money >= amount:
            self.money -= amount
            if receiver:
                receiver.receive(amount)
            return True
        else:
            self.bankrupt = True
            return False

    def receive(self, amount: int):
        self.money += amount

    def move(self, steps: int, board_size: int) -> int:
        new_pos = self.position + steps
        if new_pos >= board_size:
            self.receive(200)      
            new_pos -= board_size
        self.position = new_pos
        return self.position

    def buy_property(self, cell):
        if self.money >= cell.price and cell.owner is None:
            self.money -= cell.price
            cell.owner = self
            self.properties.append(cell.name)
            return True
        return False

    def __str__(self):
        return f"{self.name}: {self.money}₽ | позиция {self.position}"
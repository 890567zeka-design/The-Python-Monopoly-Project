import random

class Card:
    def __init__(self, description: str, action_func):
        self.description = description
        self.action = action_func

    def apply(self, player, game):
        game.ui.message(f"Карта: {self.description}")
        self.action(player, game)


def _advance_to_go(player, game):
    player.position = 0
    player.receive(200)
    game.ui.message(f"{player.name} перемещается на клетку СТАРТ и получает 200₽.")

def _bank_pays_50(player, game):
    player.receive(50)
    game.ui.message("Банк выплачивает 50₽.")

def _pay_bank_50(player, game):
    if not player.pay(50):
        game.handle_bankruptcy(player)
    else:
        game.ui.message("Штраф 50₽ списан.")

def _advance_to_illinois(player, game):
    target = 25 if len(game.board.cells) > 25 else 5
    player.position = target
    game.ui.message(f"{player.name} перемещается на {game.board.cells[target].name}")

def _get_out_of_jail(player, game):
    player.in_jail = False
    player.jail_turns = 0
    game.ui.message("Вы получили карту выхода из тюрьмы (используйте, когда будете в тюрьме).")


chance_cards = [
    Card("Продвигайтесь на СТАРТ и получите 200₽", _advance_to_go),
    Card("Банк выплачивает вам 50₽", _bank_pays_50),
    Card("Штраф 50₽", _pay_bank_50),
    Card("Переместитесь на Иллинойс-авеню", _advance_to_illinois),
    Card("Выход из тюрьмы", _get_out_of_jail),
]

community_cards = [
    Card("Вы выиграли в конкурсе 100₽", lambda p,g: p.receive(100)),
    Card("Ошибка врача – штраф 50₽", lambda p,g: p.pay(50) or g.handle_bankruptcy(p)),
    Card("С вашего счёта списано 30₽", lambda p,g: p.pay(30) or g.handle_bankruptcy(p)),
    Card("Выход из тюрьмы", _get_out_of_jail),
]

def shuffle_cards(deck):
    return random.sample(deck, len(deck))
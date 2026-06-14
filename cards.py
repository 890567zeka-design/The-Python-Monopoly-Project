import random

class Card:
    """Базовый класс для всех карт."""

    def __init__(self, card_id: int, description: str, action_method):
        self.id = card_id
        self.description = description
        self.action_method = action_method

    def apply(self, player, game):
        game.ui.message(f"Карта #{self.id}: {self.description}")
        self.action_method(player, game)


class ChanceCard(Card):
    """Карта Шанс."""
    pass


class CommunityChestCard(Card):
    """Карта Общественная казна."""
    pass


class CardActions:
    """Контейнер для всех действий карт."""

    def advance_to_go(self, player, game):
        player.position = 0
        player.receive(200)
        game.ui.message(f"{player.name} перемещается на клетку СТАРТ и получает 200₽.")

    def bank_pays_50(self, player, game):
        player.receive(50)
        game.ui.message("Банк выплачивает 50₽.")

    def bank_pays_100(self, player, game):
        player.receive(100)
        game.ui.message("Банк выплачивает 100₽.")

    def bank_pays_150(self, player, game):
        player.receive(150)
        game.ui.message("Банк выплачивает 150₽.")

    def bank_pays_200(self, player, game):
        player.receive(200)
        game.ui.message("Банк выплачивает 200₽.")

    def receive_20(self, player, game):
        player.receive(20)
        game.ui.message("Банк выплачивает 20₽.")

    def pay_bank_20(self, player, game):
        if not player.pay(20):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Штраф 20₽ списан.")

    def pay_bank_30(self, player, game):
        if not player.pay(30):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("С вашего счёта списано 30₽.")

    def pay_bank_50(self, player, game):
        if not player.pay(50):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Штраф 50₽ списан.")

    def pay_bank_80(self, player, game):
        if not player.pay(80):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Штраф 80₽ списан.")

    def pay_bank_100(self, player, game):
        if not player.pay(100):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Штраф 100₽ списан.")

    def pay_bank_150(self, player, game):
        if not player.pay(150):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Штраф 150₽ списан.")

    def advance_to_illinois(self, player, game):
        target = 25
        if target < len(game.board.cells):
            player.position = target
            game.ui.message(f"{player.name} перемещается на {game.board.cells[target].name}")
        else:
            game.ui.message("Ошибка: клетка не найдена")

    def advance_to_jail(self, player, game):
        player.in_jail = True
        player.position = game.board.get_jail_position()
        game.ui.message(f"{player.name} отправляется в тюрьму!")

    def advance_to_railroad(self, player, game):
        """Перемещение на ближайшую железную дорогу (индексы 5 и 15)."""
        railroads = [5, 15]
        current = player.position
        for rr in sorted(railroads):
            if rr > current:
                player.position = rr
                game.ui.message(f"{player.name} перемещается на {game.board.cells[rr].name}")
                return
        player.position = railroads[0]
        game.ui.message(f"{player.name} перемещается на {game.board.cells[railroads[0]].name}")

    def advance_to_nearest_utility(self, player, game):
        """Перемещение на ближайшую коммунальную услугу (индекс 12)."""
        utilities = [12]
        current = player.position
        for u in sorted(utilities):
            if u > current:
                player.position = u
                game.ui.message(f"{player.name} перемещается на {game.board.cells[u].name}")
                return
        player.position = utilities[0]
        game.ui.message(f"{player.name} перемещается на {game.board.cells[utilities[0]].name}")

    def go_back_3(self, player, game):
        new_pos = player.position - 3
        if new_pos < 0:
            new_pos = 0
        player.position = new_pos
        game.ui.message(f"{player.name} перемещается назад на 3 клетки. Новая позиция: {new_pos + 1}")

    def get_out_of_jail(self, player, game):
        player.in_jail = False
        player.jail_turns = 0
        game.ui.message("Вы получили карту выхода из тюрьмы!")

    def everyone_pays(self, player, game):
        """Каждый игрок платит 50₽ текущему игроку ."""
        total = 0
        for p in game.players:
            if p != player and not p.bankrupt:
                if p.pay(50, player):
                    game.ui.message(f"{p.name} платит 50₽ {player.name}")
                    total += 50
                else:
                    game.ui.message(f"{p.name} не может заплатить и банкротится!")
        game.ui.message(f"{player.name} получил {total}₽ от других игроков!")

    def street_repairs(self, player, game):
        """Штраф 25₽ за каждую купленную улицу."""
        fine = len(player.properties) * 25
        if fine > 0:
            if not player.pay(fine):
                game.handle_bankruptcy(player)
            else:
                game.ui.message(f"Вы заплатили {fine}₽ за ремонт улиц.")
        else:
            game.ui.message("У вас нет улиц, ремонт не требуется.")

    def birthday_gift(self, player, game):
        """Все игроки дарят по 10₽ ."""
        total = 0
        for p in game.players:
            if p != player and not p.bankrupt:
                if p.pay(10, player):
                    game.ui.message(f"{p.name} дарит 10₽ {player.name}")
                    total += 10
        game.ui.message(f"{player.name} получил {total}₽ на день рождения!")

    def lottery_win(self, player, game):
        player.receive(500)
        game.ui.message("Вы выиграли в лотерею! +500₽!")

    def tax_refund(self, player, game):
        player.receive(200)
        game.ui.message("Налоговая вернула переплату! +200₽!")

    def hospital_fees(self, player, game):
        if not player.pay(150):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Вы заплатили 150₽ за лечение в больнице.")

    def school_fees(self, player, game):
        if not player.pay(100):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Вы заплатили 100₽ за обучение.")

    def bank_error(self, player, game):
        player.receive(400)
        game.ui.message("Ошибка банка в вашу пользу! +400₽!")

    def sell_stocks(self, player, game):
        player.receive(300)
        game.ui.message("Вы выгодно продали акции! +300₽!")

    def broken_tv(self, player, game):
        if not player.pay(80):
            game.handle_bankruptcy(player)
        else:
            game.ui.message("Вы разбили телевизор соседа. Штраф 80₽.")


actions = CardActions()

chance_cards = [
    ChanceCard(1, "Продвигайтесь на СТАРТ и получите 200₽", actions.advance_to_go),
    ChanceCard(2, "Банк выплачивает вам 50₽", actions.bank_pays_50),
    ChanceCard(3, "Штраф 50₽", actions.pay_bank_50),
    ChanceCard(4, "Переместитесь на Иллинойс-авеню", actions.advance_to_illinois),
    ChanceCard(5, "Переместитесь на ближайшую железную дорогу", actions.advance_to_railroad),
    ChanceCard(6, "Сделайте шаг назад на 3 клетки", actions.go_back_3),
    ChanceCard(7, "Банк выплачивает вам 100₽", actions.bank_pays_100),
    ChanceCard(8, "Штраф 100₽", actions.pay_bank_100),
    ChanceCard(9, "Выход из тюрьмы", actions.get_out_of_jail),
    ChanceCard(10, "Переместитесь на ближайшую коммунальную услугу", actions.advance_to_nearest_utility),
    ChanceCard(11, "Идите в тюрьму!", actions.advance_to_jail),
    ChanceCard(12, "Банк выплачивает вам 150₽", actions.bank_pays_150),
    ChanceCard(13, "Штраф 150₽", actions.pay_bank_150),
    ChanceCard(14, "Вы выиграли в лотерею! 500₽", actions.lottery_win),
    ChanceCard(15, "Ошибка банка! +400₽", actions.bank_error),
]

community_cards = [
    CommunityChestCard(1, "Вы выиграли в конкурсе 100₽", actions.bank_pays_100),
    CommunityChestCard(2, "Ошибка врача – штраф 50₽", actions.pay_bank_50),
    CommunityChestCard(3, "С вашего счёта списано 30₽", actions.pay_bank_30),
    CommunityChestCard(4, "Выход из тюрьмы", actions.get_out_of_jail),
    CommunityChestCard(5, "Каждый игрок платит вам 50₽", actions.everyone_pays),
    CommunityChestCard(6, "Ремонт улиц – штраф 25₽ за улицу", actions.street_repairs),
    CommunityChestCard(7, "Банк выплачивает вам 20₽", actions.receive_20),
    CommunityChestCard(8, "Вы получили наследство – 150₽", actions.bank_pays_150),
    CommunityChestCard(9, "С вас списано 100₽ на благотворительность", actions.pay_bank_100),
    CommunityChestCard(10, "День рождения! Все дарят вам по 10₽", actions.birthday_gift),
    CommunityChestCard(11, "Налоговый вычет! +200₽", actions.tax_refund),
    CommunityChestCard(12, "Больничные расходы – 150₽", actions.hospital_fees),
    CommunityChestCard(13, "Плата за обучение – 100₽", actions.school_fees),
    CommunityChestCard(14, "Выгодная сделка с акциями! +300₽", actions.sell_stocks),
    CommunityChestCard(15, "Разбили телевизор – штраф 80₽", actions.broken_tv),
]


def shuffle_cards(deck):
    """Перемешивает колоду"""
    return random.sample(deck, len(deck))

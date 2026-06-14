import random
from board import Board
from player import Player
from cards import chance_cards, community_cards, shuffle_cards

class GameUI:
    def __init__(self):
        pass

    def message(self, text):
        print(text)

    def get_int_input(self, prompt, min_val, max_val):
        while True:
            try:
                val = int(input(prompt))
                if min_val <= val <= max_val:
                    return val
                print(f"Введите число от {min_val} до {max_val}.")
            except ValueError:
                print("Введите целое число.")

    def prompt_buy_property(self, player, property_cell):
        print(f"{player.name}, вы попали на {property_cell.name}. Цена: {property_cell.price}₽")
        while True:
            answer = input("Купить? (да/нет): ").strip().lower()
            if answer == "да":
                if player.buy_property(property_cell):
                    self.message(f"{player.name} купил {property_cell.name} за {property_cell.price}₽")
                else:
                    self.message("Недостаточно денег для покупки!")
                break
            elif answer == "нет":
                self.message(f"{player.name} отказался от покупки.")
                break
            else:
                self.message("Пожалуйста, введите 'да' или 'нет'.")

    def roll_dice_with_visual(self, player):
        input(f"{player.name}, нажмите Enter, чтобы бросить кубики...")
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        faces = {
            1: ["┌─────┐", "│     │", "│  ●  │", "│     │", "└─────┘"],
            2: ["┌─────┐", "│ ●   │", "│     │", "│   ● │", "└─────┘"],
            3: ["┌─────┐", "│ ●   │", "│  ●  │", "│   ● │", "└─────┘"],
            4: ["┌─────┐", "│ ● ● │", "│     │", "│ ● ● │", "└─────┘"],
            5: ["┌─────┐", "│ ● ● │", "│  ●  │", "│ ● ● │", "└─────┘"],
            6: ["┌─────┐", "│ ● ● │", "│ ● ● │", "│ ● ● │", "└─────┘"],
        }

        lines1 = faces[dice1]
        lines2 = faces[dice2]

        print(f"\n{player.name} бросает кубики:", flush=True)
        for i in range(5):
            print(lines1[i] + "   " + lines2[i], flush=True)

        total = dice1 + dice2
        print(f"Сумма: {dice1} + {dice2} = {total}\n", flush=True)
        return total

    def show_player_status(self, players, board):
        print("\n=== СТАТУС ИГРОКОВ ===")
        for p in players:
            if not p.bankrupt:
                cell_name = board.get_cell(p.position).name
                user_position = p.position + 1
                print(f"{p.name}: {p.money}₽ | позиция {user_position} ({cell_name})")
            else:
                print(f"{p.name}: БАНКРОТ")
        print("=====================\n")

    def show_properties(self, players):
        print("=== СОБСТВЕННОСТЬ ===")
        has_property = False
        for p in players:
            if p.properties:
                has_property = True
                print(f"{p.name}: {', '.join(p.properties)}")
        if not has_property:
            print("Пока никто ничего не купил.")
        print("=====================\n")


class Game:
    def __init__(self, ui):
        self.ui = ui
        self.board = Board()
        self.players = []
        self.current_player_index = 0
        self.chance_deck = shuffle_cards(chance_cards)
        self.community_deck = shuffle_cards(community_cards)
        self.game_over = False

    def add_player(self, name):
        self.players.append(Player(name))

    def start(self):
        if len(self.players) < 2:
            self.ui.message("Должно быть минимум 2 игрока.")
            return
        self.ui.message("Игра начинается!")
        while not self.game_over:
            self.next_turn()
            if self.check_winner():
                break

    def next_turn(self):
        player = self.players[self.current_player_index]
        if player.bankrupt:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return

        self.ui.message(f"\n--- ХОД ИГРОКА {player.name.upper()} ---")
        self.ui.show_player_status(self.players, self.board)
        self.ui.show_properties(self.players)

        if player.in_jail:
            self.handle_jail_turn(player)
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return

        total = self.ui.roll_dice_with_visual(player)

        old_pos = player.position
        new_pos = player.move(total, self.board.size)
        old_user_pos = old_pos + 1
        new_user_pos = new_pos + 1
        self.ui.message(f"{player.name} перемещается с {old_user_pos} ({self.board.get_cell(old_pos).name}) на {new_user_pos} ({self.board.get_cell(new_pos).name})")

        cell = self.board.get_cell(new_pos)
        self.ui.message(f"Клетка: {cell.name}")
        cell.land_on(player, self)

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def handle_jail_turn(self, player):
        """Обработка хода игрока, находящегося в тюрьме.
        Игрок может выйти, выбросив дубль, или отсидев 3 хода."""
        self.ui.message(f"{player.name} находится в тюрьме. Попыток выйти: {player.jail_turns}")
        if player.jail_turns >= 3:
            player.in_jail = False
            player.jail_turns = 0
            self.ui.message("Вы отсидели срок, выходите!")
            return
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.ui.message(f"Бросок в тюрьме: {dice1} + {dice2}")
        if dice1 == dice2:
            player.in_jail = False
            player.jail_turns = 0
            self.ui.message("Вы выбросили дубль! Выходите из тюрьмы.")
            new_pos = player.move(dice1 + dice2, self.board.size)
            cell = self.board.get_cell(new_pos)
            cell.land_on(player, self)
        else:
            player.jail_turns += 1
            self.ui.message("Не дубль. Остаётесь в тюрьме.")

    def draw_chance_card(self, player):
        if not self.chance_deck:
            self.chance_deck = shuffle_cards(chance_cards)
        card = self.chance_deck.pop(0)
        card.apply(player, self)

    def draw_community_chest_card(self, player):
        if not self.community_deck:
            self.community_deck = shuffle_cards(community_cards)
        card = self.community_deck.pop(0)
        card.apply(player, self)

    def handle_bankruptcy(self, player):
        """Обработка банкротства игрока.
        Игрок выбывает, его собственность переходит банку ."""
        self.ui.message(f"{player.name} обанкротился!")
        player.bankrupt = True
        for prop in player.properties:
            for cell in self.board.cells:
                if hasattr(cell, 'owner') and cell.owner == player:
                    cell.owner = None
        player.properties.clear()

    def check_winner(self):
        """Проверяет, остался ли только один активный игрок.
        Если да — объявляет победителя и завершает игру."""
        active_players = [p for p in self.players if not p.bankrupt]
        if len(active_players) == 1:
            winner = active_players[0]
            self.ui.message(f"\nПоздравляем! {winner.name} ПОБЕДИЛ!")
            self.game_over = True
            return True
        return False

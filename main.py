from game import Game, GameUI
from board import Board


class MonopolyApp:
    """Главный класс приложения Упрощённая Монополия."""

    def __init__(self):
        self.ui = GameUI()

    def run(self):
        """Запуск основного цикла приложения."""
        while True:
            self._show_main_menu()
            choice = self.ui.get_int_input("Выберите действие: ", 1, 4)

            if choice == 1:
                self._new_game()
            elif choice == 2:
                self._show_rules()
            elif choice == 3:
                self._show_map()
            else:
                print("До свидания!")
                break

    def _show_main_menu(self):
        print("\n===== УПРОЩЁННАЯ МОНОПОЛИЯ =====")
        print("1. Новая игра")
        print("2. Правила игры")
        print("3. Карта")
        print("4. Выход")

    def _new_game(self):
        game = Game(self.ui)
        num = self.ui.get_int_input("Введите количество игроков (2-4): ", 2, 4)

        for i in range(num):
            name = input(f"Имя игрока {i + 1}: ").strip()
            if not name:
                name = f"Игрок{i + 1}"
            game.add_player(name)

        game.start()
        input("\nИгра завершена. Нажмите Enter, чтобы вернуться в меню...")

    def _show_rules(self):
        print("\n" + "=" * 55)
        print("ПРАВИЛА ИГРЫ")
        print("=" * 55)
        print("""
1. Игроки по очереди бросают два кубика и перемещают свою фишку.
2. При попадании на свободную улицу её можно купить (введите 'да' или 'нет').
3. Если улица принадлежит другому игроку, нужно заплатить аренду.
4. При проходе через клетку СТАРТ игрок получает 200₽.
5. Клетки:
   - НАЛОГ — нужно заплатить указанную сумму.
   - ШАНС и ОБЩЕСТВЕННАЯ КАЗНА — вытягивается карточка с событием .
   - ТЮРЬМА — можно выйти, выбросив дубль или отсидев 3 хода.
6. Игрок банкротится, если не может заплатить налог или аренду.
7. Побеждает последний оставшийся игрок.
        """)
        print("=" * 55)
        input("\nНажмите Enter, чтобы вернуться в меню...")

    def _show_map(self):
        board = Board()
        print("\n" + "=" * 55)
        print("КАРТА КЛЕТОК ")
        print("=" * 55)

        for i, cell in enumerate(board.cells):
            user_num = i + 1
            cell_type = ""
            if hasattr(cell, 'price'):
                cell_type = f" Цена: {cell.price}₽"
            elif hasattr(cell, 'amount'):
                cell_type = f" Штраф: {cell.amount}₽"

            print(f"{user_num:2d}. {cell.name}{cell_type}")

        print("=" * 55)
        input("\nНажмите Enter, чтобы вернуться в меню...")


if __name__ == "__main__":
    app = MonopolyApp()
    app.run()

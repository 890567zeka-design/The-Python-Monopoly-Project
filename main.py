from game import Game, GameUI

def main():
    ui = GameUI()
    while True:
        print("\n===== УПРОЩЁННАЯ МОНОПОЛИЯ =====")
        print("1. Новая игра")
        print("2. Выход")
        choice = ui.get_int_input("Выберите действие: ", 1, 2)

        if choice == 1:
            new_game(ui)
        else:
            print("До свидания!")
            break

def new_game(ui):
    game = Game(ui)
    num = ui.get_int_input("Введите количество игроков (2-4): ", 2, 4)
    for i in range(num):
        name = input(f"Имя игрока {i+1}: ").strip()
        if not name:
            name = f"Игрок{i+1}"
        game.add_player(name)
    game.start()
    input("\nИгра завершена. Нажмите Enter, чтобы вернуться в меню...")

if __name__ == "__main__":
    main()
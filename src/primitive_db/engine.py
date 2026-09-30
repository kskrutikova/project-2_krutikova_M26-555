"""Игровой цикл и точка входа в пользовательский интерфейс."""

import prompt

HELP_TEXT = """***
<command> exit - выйти из программы
<command> help - справочная информация"""


def welcome() -> None:
    """Запускает основной цикл взаимодействия с пользователем."""
    print("Первая попытка запустить проект!")
    print()
    print(HELP_TEXT)

    while True:
        command = prompt.string("Введите команду: ")

        if command == "exit":
            print("Выход из программы.")
            break

        if command == "help":
            print(HELP_TEXT)
            continue

        print(f"Неизвестная команда: {command}. Введите 'help' для справки.")

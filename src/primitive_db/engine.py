"""Игровой цикл и точка входа в пользовательский интерфейс."""

import shlex

import prompt

from src.primitive_db.constants import METADATA_FILE
from src.primitive_db.core import create_table, drop_table, list_tables
from src.primitive_db.utils import load_metadata, save_metadata


def print_help() -> None:
    """Печатает справку по командам управления таблицами."""
    print()
    print("***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print()
    print("Общие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")
    print()


def run() -> None:
    """Запускает основной цикл взаимодействия с пользователем."""
    metadata = load_metadata(METADATA_FILE)

    while True:
        user_input = prompt.string("Введите команду: ")

        if not user_input:
            continue

        args = shlex.split(user_input)
        command = args[0]

        if command == "exit":
            print("Выход из программы.")
            break

        if command == "help":
            print_help()
            continue

        if command == "create_table":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue

            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(METADATA_FILE, metadata)
            continue

        if command == "drop_table":
            if len(args) != 2:
                print("Ошибка: укажите имя таблицы.")
                continue

            metadata = drop_table(metadata, args[1])
            save_metadata(METADATA_FILE, metadata)
            continue

        if command == "list_tables":
            if len(args) != 1:
                print("Ошибка: команда list_tables не принимает аргументы.")
                continue

            list_tables(metadata)
            continue

        print(f"Функции {command} нет. Попробуйте снова.")

"""Игровой цикл и точка входа в пользовательский интерфейс."""

import shlex

import prompt
from prettytable import PrettyTable

from src.primitive_db.constants import METADATA_FILE
from src.primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from src.primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help() -> None:
    """Печатает справку по командам управления таблицами."""
    print()
    print("***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert <имя_таблицы> <значения...> - добавить запись")
    print("<command> select <имя_таблицы> [where <условие>] - выбрать записи")
    print("<command> update <имя_таблицы> set <условие> where <условие> - обновить")
    print("<command> delete <имя_таблицы> where <условие> - удалить записи")
    print("<command> info <имя_таблицы> - описание таблицы")
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

            table_name = args[1]
            updated_metadata = drop_table(metadata, table_name)

            if updated_metadata is not None:
                metadata = updated_metadata
                save_metadata(METADATA_FILE, metadata)
                delete_table_data(table_name)

            continue

        if command == "list_tables":
            if len(args) != 1:
                print("Ошибка: команда list_tables не принимает аргументы.")
                continue

            list_tables(metadata)
            continue

        if command == "insert":
            if len(args) < 3:
                print("Ошибка: укажите имя таблицы и значения.")
                continue

            table_name = args[1]
            values = args[2:]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            if not values:
                print("Ошибка: укажите хотя бы одно поле в формате key=value.")
                continue

            parsed = {}
            for v in values:
                if "=" not in v:
                    print(f"Ошибка: аргумент '{v}' должен быть в формате key=value.")
                    break
                key, val = v.split("=", 1)
                parsed[key] = val
            else:
                table_data = load_table_data(table_name)
                table_data = insert(metadata, table_name, table_data, parsed)
                save_table_data(table_name, table_data)

            continue

        if command == "select":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)

            if len(args) >= 4 and args[2] == "where":
                where_clause = " ".join(args[3:])
            else:
                where_clause = None

            result = select(table_data, where_clause)

            table = PrettyTable()
            if result:
                table.field_names = result[0].keys()
                for record in result:
                    table.add_row(record.values())

            print(table)
            continue

        if command == "update":
            if len(args) < 6 or args[2] != "set" or args[4] != "where":
                print("Ошибка: формат update <таблица> set <условие> where <условие>.")
                continue

            table_name = args[1]
            set_clause = args[3]
            where_clause = args[5]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)
            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)
            continue

        if command == "delete":
            if len(args) < 4 or args[2] != "where":
                print("Ошибка: формат delete <таблица> where <условие>.")
                continue

            table_name = args[1]
            where_clause = " ".join(args[3:])

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)
            updated_table_data = delete(table_data, where_clause)

            if updated_table_data is not None:
                save_table_data(table_name, updated_table_data)

            continue

        if command == "info":
            if len(args) != 2:
                print("Ошибка: укажите имя таблицы.")
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            columns = metadata[table_name]
            print(f'Таблица "{table_name}":')
            for col_name, col_type in columns:
                print(f"  {col_name}:{col_type}")
            continue

        print(f"Функции {command} нет. Попробуйте снова.")

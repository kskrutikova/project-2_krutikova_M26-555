"""Игровой цикл и точка входа в пользовательский интерфейс."""

import shlex

import prompt
from prettytable import PrettyTable

from src.primitive_db.constants import METADATA_FILE
from src.primitive_db.core import (
    create_cacher,
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
    """Печатает справку по командам приложения."""
    print()
    print("***Операции с данными***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print(
        "<command> insert into <имя_таблицы> "
        "values (<значение1>, <значение2>, ...) - создать запись"
    )
    print(
        "<command> select from <имя_таблицы> "
        "[where <столбец> = <значение>] - выбрать записи"
    )
    print(
        "<command> update <имя_таблицы> "
        "set <столбец> = <значение> "
        "where <столбец> = <значение> - обновить запись"
    )
    print(
        "<command> delete from <имя_таблицы> "
        "where <столбец> = <значение> - удалить запись"
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    print()
    print("Общие команды:")
    print("<command> help - справочная информация")
    print("<command> exit - выход из программы")
    print()


def run() -> None:
    """Запускает основной цикл взаимодействия с пользователем."""
    metadata = load_metadata(METADATA_FILE)
    cache_result = create_cacher()

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
                cache_result.clear_cache()

            continue

        if command == "list_tables":
            if len(args) != 1:
                print("Ошибка: команда list_tables не принимает аргументы.")
                continue

            list_tables(metadata)
            continue

        if command == "insert":
            if len(args) < 5 or args[1] != "into" or args[3] != "values":
                print("Ошибка: формат insert into <таблица> values (<значения>).")
                continue

            table_name = args[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            values_text = " ".join(args[4:]).strip()

            if not (values_text.startswith("(") and values_text.endswith(")")):
                print("Ошибка: значения должны быть указаны в скобках.")
                continue

            values_text = values_text[1:-1].strip()

            if not values_text:
                print("Ошибка: укажите значения.")
                continue

            values = [value.strip() for value in values_text.split(",")]

            columns = metadata[table_name][1:]
            if len(values) != len(columns):
                print(
                    "Ошибка: количество значений должно соответствовать "
                    "количеству столбцов."
                )
                continue

            parsed = {
                column_name: value for (column_name, _), value in zip(columns, values)
            }

            table_data = load_table_data(table_name)
            updated_table_data = insert(
                metadata,
                table_name,
                table_data,
                parsed,
            )

            if updated_table_data is not None:
                save_table_data(table_name, updated_table_data)
                cache_result.clear_cache()

            continue

        if command == "select":
            if len(args) < 3 or args[1] != "from":
                print("Ошибка: формат select from <таблица> [where <условие>].")
                continue

            table_name = args[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)

            if len(args) > 3:
                if args[3] != "where" or len(args) < 5:
                    print(
                        "Ошибка: условие должно иметь формат "
                        "where <столбец> = <значение>."
                    )
                    continue

                where_clause = " ".join(args[4:])
            else:
                where_clause = None

            cache_key = (table_name, where_clause)

            result = cache_result(
                cache_key,
                lambda: select(table_data, where_clause),
            )

            table = PrettyTable()
            if result:
                table.field_names = result[0].keys()
                for record in result:
                    table.add_row(record.values())

            print(table)
            continue

        if command == "update":
            if len(args) < 6 or args[2] != "set":
                print("Ошибка: формат update <таблица> set <условие> where <условие>.")
                continue

            try:
                where_index = args.index("where", 3)
            except ValueError:
                print("Ошибка: формат update <таблица> set <условие> where <условие>.")
                continue

            if where_index <= 3 or where_index == len(args) - 1:
                print("Ошибка: формат update <таблица> set <условие> where <условие>.")
                continue

            table_name = args[1]
            set_clause = " ".join(args[3:where_index])
            where_clause = " ".join(args[where_index + 1 :])

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)
            old_table_data = table_data.copy()

            updated_table_data = update(
                table_data,
                set_clause,
                where_clause,
            )

            if updated_table_data is not None:
                changed_ids = [
                    old_record["ID"]
                    for old_record, new_record in zip(
                        old_table_data,
                        updated_table_data,
                    )
                    if old_record != new_record
                ]

                save_table_data(table_name, updated_table_data)
                cache_result.clear_cache()

                for record_id in changed_ids:
                    print(
                        f"Запись с ID={record_id} "
                        f'в таблице "{table_name}" успешно обновлена.'
                    )

            continue

        if command == "delete":
            if len(args) < 5 or args[1] != "from" or args[3] != "where":
                print("Ошибка: формат delete from <таблица> where <условие>.")
                continue

            table_name = args[2]
            where_clause = " ".join(args[4:])

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)
            old_table_data = table_data.copy()

            updated_table_data = delete(
                table_data,
                where_clause,
            )

            if updated_table_data is not None:
                remaining_ids = {record["ID"] for record in updated_table_data}

                deleted_ids = [
                    record["ID"]
                    for record in old_table_data
                    if record["ID"] not in remaining_ids
                ]

                save_table_data(table_name, updated_table_data)
                cache_result.clear_cache()

                for record_id in deleted_ids:
                    print(
                        f"Запись с ID={record_id} "
                        f'успешно удалена из таблицы "{table_name}".'
                    )

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
            columns_repr = ", ".join(
                f"{col_name}:{col_type}" for col_name, col_type in columns
            )
            table_data = load_table_data(table_name)

            print(f"Таблица: {table_name}")
            print(f"Столбцы: {columns_repr}")
            print(f"Количество записей: {len(table_data)}")
            continue

        print(f"Функции {command} нет. Попробуйте снова.")

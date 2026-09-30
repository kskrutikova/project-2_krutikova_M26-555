from src.primitive_db.constants import VALID_TYPES


def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict:
    """Создаёт таблицу в метаданных.

    :param metadata: текущий словарь метаданных
    :param table_name: имя создаваемой таблицы
    :param columns: список столбцов в формате ["name:type", ...]
    :return: обновлённый словарь метаданных
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = [("ID", "int")]

    for column in columns:
        name, col_type = column.split(":", 1)
        if col_type not in VALID_TYPES:
            print(
                f'Ошибка: Недопустимый тип "{col_type}" для столбца "{name}".'
                f" Допустимые типы: {', '.join(sorted(VALID_TYPES))}."
            )
            return metadata
        parsed_columns.append((name, col_type))

    metadata[table_name] = parsed_columns

    columns_repr = ", ".join(f"{name}:{ctype}" for name, ctype in parsed_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_repr}')

    return metadata


def drop_table(metadata: dict, table_name: str) -> dict:
    """Удаляет таблицу из метаданных.

    :param metadata: текущий словарь метаданных
    :param table_name: имя удаляемой таблицы
    :return: обновлённый словарь метаданных
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata: dict) -> None:
    """Печатает список всех таблиц.

    :param metadata: текущий словарь метаданных
    """
    if not metadata:
        print("Список таблиц пуст.")
        return

    for table_name in metadata:
        print(f"- {table_name}")


def insert(
    metadata: dict,
    table_name: str,
    table_data: list[dict],
    values: list[str],
) -> list[dict]:
    """Добавляет новую запись в таблицу.

    :param metadata: метаданные
    :param table_name: имя таблицы
    :param table_data: текущие данные таблицы (список записей)
    :param values: значения столбцов в порядке их описания (без ID)
    :return: обновлённый список записей
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name]
    # columns[0] — это ID, дальше пользовательские столбцы
    data_columns = columns[1:]

    if len(values) != len(data_columns):
        print(
            f"Ошибка: ожидается {len(data_columns)} значений, получено {len(values)}."
        )
        return table_data

    # Вычисляем новый ID
    max_id = 0
    for record in table_data:
        if record.get("ID", 0) > max_id:
            max_id = record["ID"]
    new_id = max_id + 1

    new_record = {"ID": new_id}
    for (col_name, _), value in zip(data_columns, values):
        new_record[col_name] = value

    return table_data + [new_record]


def select(
    table_data: list[dict],
    where_clause: str | None = None,
) -> list[dict]:
    """Выбирает записи из таблицы.

    :param table_data: данные таблицы
    :param where_clause: условие вида "column=value" или None
    :return: список записей, удовлетворяющих условию
    """
    if where_clause is None:
        return table_data

    if "=" not in where_clause:
        print(f"Ошибка: некорректное условие where: {where_clause}")
        return table_data

    column, value = where_clause.split("=", 1)

    result = []
    for record in table_data:
        if str(record.get(column)) == value:
            result.append(record)

    return result


def update(
    table_data: list[dict],
    set_clause: str,
    where_clause: str,
) -> list[dict]:
    """Обновляет записи в таблице.

    :param table_data: данные таблицы
    :param set_clause: условие обновления вида "column=value"
    :param where_clause: условие отбора вида "column=value"
    :return: новый список записей с обновлёнными значениями
    """
    if "=" not in set_clause or "=" not in where_clause:
        print("Ошибка: некорректное условие update.")
        return table_data

    set_col, set_value = set_clause.split("=", 1)
    where_col, where_value = where_clause.split("=", 1)

    new_data = []
    for record in table_data:
        if str(record.get(where_col)) == where_value:
            new_record = record.copy()
            new_record[set_col] = set_value
            new_data.append(new_record)
        else:
            new_data.append(record)

    return new_data


def delete(
    table_data: list[dict],
    where_clause: str,
) -> list[dict]:
    """Удаляет записи из таблицы.

    :param table_data: данные таблицы
    :param where_clause: условие отбора вида "column=value"
    :return: новый список записей без удалённых
    """
    if "=" not in where_clause:
        print("Ошибка: некорректное условие delete.")
        return table_data

    where_col, where_value = where_clause.split("=", 1)

    return [
        record for record in table_data if str(record.get(where_col)) != where_value
    ]

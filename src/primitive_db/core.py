from src.primitive_db.constants import VALID_TYPES
from src.primitive_db.decorators import confirm_action, handle_db_errors, log_time
from src.primitive_db.parser import parse_condition


@handle_db_errors
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


def _convert_value(value: str, column_type: str) -> int | str | bool:
    """Преобразует значение к типу столбца."""
    if column_type == "int":
        try:
            return int(value)
        except ValueError as error:
            raise ValueError(f'Значение "{value}" должно быть целым числом.') from error

    if column_type == "bool":
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        raise ValueError(f'Значение "{value}" должно быть true или false.')

    if column_type == "str":
        return value

    raise ValueError(f"Неизвестный тип столбца: {column_type}.")


@handle_db_errors
@log_time
@confirm_action("удаление таблицы")
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


@handle_db_errors
def list_tables(metadata: dict) -> None:
    """Печатает список всех таблиц.

    :param metadata: текущий словарь метаданных
    """
    if not metadata:
        print("Список таблиц пуст.")
        return

    for table_name in metadata:
        print(f"- {table_name}")


@handle_db_errors
@log_time
def insert(
    metadata: dict,
    table_name: str,
    table_data: list[dict],
    values: dict[str, str],
) -> list[dict]:
    """Добавляет новую запись в таблицу.

    :param metadata: метаданные
    :param table_name: имя таблицы
    :param table_data: текущие данные таблицы
    :param values: словарь {column_name: value}
    :return: обновлённый список записей
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name]
    data_columns = columns[1:]
    column_names = {column_name for column_name, _ in data_columns}

    if "ID" in values:
        print('Ошибка: столбец "ID" заполняется автоматически.')
        return table_data

    extra_columns = set(values) - column_names
    if extra_columns:
        extra_column = next(iter(extra_columns))
        print(f'Ошибка: столбец "{extra_column}" отсутствует в таблице.')
        return table_data

    for col_name, _ in data_columns:
        if col_name not in values:
            print(f"Ошибка: не указано значение для столбца {col_name}.")
            return table_data

    converted_values = {}

    for col_name, col_type in data_columns:
        converted_values[col_name] = _convert_value(
            values[col_name],
            col_type,
        )

    max_id = 0
    for record in table_data:
        if record.get("ID", 0) > max_id:
            max_id = record["ID"]

    new_id = max_id + 1
    new_record = {"ID": new_id}
    new_record.update(converted_values)

    return table_data + [new_record]


@handle_db_errors
@log_time
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

    condition = parse_condition(where_clause)
    column, value = next(iter(condition.items()))

    return [record for record in table_data if record.get(column) == value]


@handle_db_errors
@log_time
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
    set_condition = parse_condition(set_clause)
    where_condition = parse_condition(where_clause)

    set_col, set_value = next(iter(set_condition.items()))
    where_col, where_value = next(iter(where_condition.items()))

    if set_col == "ID":
        raise ValueError('Столбец "ID" нельзя изменять.')

    if table_data:
        available_columns = set(table_data[0])
        if set_col not in available_columns:
            raise ValueError(f'Столбец "{set_col}" отсутствует в таблице.')
        if where_col not in available_columns:
            raise ValueError(f'Столбец "{where_col}" отсутствует в таблице.')

    new_data = []

    for record in table_data:
        if record.get(where_col) == where_value:
            new_record = record.copy()
            new_record[set_col] = set_value
            new_data.append(new_record)
        else:
            new_data.append(record)

    return new_data


@handle_db_errors
@log_time
@confirm_action("удаление записи")
def delete(
    table_data: list[dict],
    where_clause: str,
) -> list[dict]:
    """Удаляет записи из таблицы.

    :param table_data: данные таблицы
    :param where_clause: условие отбора вида "column=value"
    :return: новый список записей без удалённых
    """
    condition = parse_condition(where_clause)
    where_col, where_value = next(iter(condition.items()))

    if table_data and where_col not in table_data[0]:
        raise ValueError(f'Столбец "{where_col}" отсутствует в таблице.')

    return [record for record in table_data if record.get(where_col) != where_value]

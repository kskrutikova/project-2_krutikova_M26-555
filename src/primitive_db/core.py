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

import json
import os

from src.primitive_db.constants import DATA_DIR


def load_metadata(filepath: str) -> dict:
    """Загружает данные из JSON-файла.

    Если файл не найден, возвращает пустой словарь.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: dict) -> None:
    """Сохраняет переданные данные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_table_data(table_name: str) -> list[dict]:
    """Загружает данные таблицы из JSON-файла."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list[dict]) -> None:
    """Сохраняет данные таблицы в JSON-файл."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def delete_table_data(table_name: str) -> None:
    """Удаляет файл данных таблицы, если он существует."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)

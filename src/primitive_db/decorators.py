"""Декораторы для операций с базой данных."""

import functools
import time
from typing import Any, Callable

import prompt


def handle_db_errors(func: Callable) -> Callable:
    """Декоратор для обработки ошибок операций с БД."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as error:
            print(f"Ошибка: Таблица или столбец {error} не найден.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")
        except Exception as error:
            print(f"Произошла непредвиденная ошибка: {error}")
        return None

    return wrapper


def confirm_action(action_name: str) -> Callable:
    """Декоратор с аргументом для подтверждения действия пользователем."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            answer = (
                prompt.string(
                    f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
                )
                .strip()
                .lower()
            )
            if answer != "y":
                print("Действие отменено.")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func: Callable) -> Callable:
    """Декоратор для замера времени выполнения функции."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        elapsed = end - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result

    return wrapper

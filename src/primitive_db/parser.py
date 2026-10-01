def parse_condition(condition: str) -> dict[str, int | str | bool]:
    """Разбирает условие вида column=value или column = value."""
    if "=" not in condition:
        raise ValueError("Условие должно содержать знак '='.")

    column, value = condition.split("=", 1)
    column = column.strip()
    value = value.strip()

    if not column:
        raise ValueError("Не указано имя столбца.")

    if not value:
        raise ValueError("Не указано значение.")

    if value.startswith('"') and value.endswith('"'):
        parsed_value: int | str | bool = value[1:-1]
    elif value.lower() == "true":
        parsed_value = True
    elif value.lower() == "false":
        parsed_value = False
    else:
        try:
            parsed_value = int(value)
        except ValueError:
            parsed_value = value

    return {column: parsed_value}

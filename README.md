# Примитивная база данных

Консольное приложение для работы с таблицами и записями.

Приложение поддерживает:

- создание таблиц;
- просмотр списка таблиц;
- удаление таблиц;
- добавление записей;
- выборку записей;
- обновление записей;
- удаление записей;
- просмотр информации о таблице;
- сохранение метаданных и данных в JSON-файлах.

## Требования

- Python 3.12 или выше;
- uv;
- Make.

## Установка

Установите зависимости командой:

```bash
make install
```

Команда выполняет:

```bash
uv sync
```

## Запуск

Запуск приложения через команду `project`:

```bash
make project
```

или:

```bash
uv run project
```

Также приложение можно запустить через команду `database`:

```bash
make database
```

или:

```bash
uv run database
```

## Хранение данных

Метаданные таблиц сохраняются в файле:

```text
db_meta.json
```

Данные таблиц сохраняются в отдельных JSON-файлах в каталоге:

```text
data/
```

Например:

```text
data/users.json
```

Каталог `data/` и файл `db_meta.json` добавлены в `.gitignore`.

## Команды приложения

### Управление таблицами

Создание таблицы:

```text
create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...
```

Поддерживаемые типы:

```text
int
str
bool
```

Пример:

```text
create_table users name:str age:int is_active:bool
```

Столбец `ID:int` добавляется автоматически.

Просмотр списка таблиц:

```text
list_tables
```

Удаление таблицы:

```text
drop_table <имя_таблицы>
```

Удаление таблицы требует подтверждения пользователя.

Просмотр информации о таблице:

```text
info <имя_таблицы>
```

Пример:

```text
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0
```

### CRUD-операции

Добавление записи:

```text
insert into <имя_таблицы> values (<значение1>, <значение2>, ...)
```

Пример:

```text
insert into users values ("Alice", 28, true)
```

Значение `ID` указывать не нужно: оно генерируется автоматически.

Выборка всех записей:

```text
select from <имя_таблицы>
```

Выборка записей по условию:

```text
select from <имя_таблицы> where <столбец> = <значение>
```

Пример:

```text
select from users where age = 28
```

Обновление записей:

```text
update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>
```

Пример:

```text
update users set age = 29 where name = "Alice"
```

Удаление записей:

```text
delete from <имя_таблицы> where <столбец> = <значение>
```

Пример:

```text
delete from users where name = "Alice"
```

Удаление записи требует подтверждения пользователя.

Справка:

```text
help
```

Выход:

```text
exit
```

## Пример работы

```text
create_table users name:str age:int is_active:bool
insert into users values ("Alice", 28, true)
insert into users values ("Bob", 30, false)
select from users
select from users where age = 28
update users set age = 29 where name = "Alice"
select from users where name = "Alice"
delete from users where name = "Bob"
y
info users
drop_table users
y
exit
```

## Структура проекта

```text
src/
└── primitive_db/
    ├── main.py
    ├── engine.py
    ├── core.py
    ├── utils.py
    ├── parser.py
    ├── decorators.py
    └── constants.py
```

Назначение модулей:

- `main.py` — точка входа;
- `engine.py` — основной цикл приложения и обработка команд;
- `core.py` — логика работы с таблицами и записями;
- `utils.py` — загрузка и сохранение данных;
- `parser.py` — разбор условий;
- `decorators.py` — декораторы;
- `constants.py` — константы проекта.

## Декораторы и кэширование

В проекте используются:

- `handle_db_errors` для обработки ошибок;
- `confirm_action` для подтверждения удаления таблиц и записей;
- `log_time` для измерения времени выполнения функций;
- замыкание `create_cacher` для кэширования результатов `select`.

## Команды Makefile

Установка зависимостей:

```bash
make install
```

Запуск приложения:

```bash
make project
make database
```

Проверка кода:

```bash
make lint
```

Сборка пакета:

```bash
make build
```

Проверка публикации без загрузки файлов:

```bash
make publish
```

Установка собранного wheel-файла:

```bash
make package-install
```

## Проверка стиля и сборка

Проверка Ruff:

```bash
make lint
```

Сборка пакета:

```bash
make build
```

Проверка публикации без фактической загрузки:

```bash
make publish
```

## Демонстрация

Полный сценарий работы приложения:

- создание таблицы;
- добавление двух записей;
- выборка всех записей;
- выборка по условию;
- обновление записи;
- удаление записи с подтверждением;
- просмотр информации о таблице;
- удаление таблицы с подтверждением.

добавить ссылку записи.
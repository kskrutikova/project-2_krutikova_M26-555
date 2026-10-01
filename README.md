# Примитивная база данных (Primitive DB)

Консольное приложение, которое имитирует базовую работу с данными. Можно создавать таблицы, добавлять в них записи, читать, обновлять и удалять, а также удалять сами таблицы.

## Установка

```bash
make install
```

## Запуск

```bash
make project
```

## Демонстрация работы

Ниже показан полный сценарий работы: создание таблицы, добавление записей, чтение, обновление, удаление записей и удаление таблицы.

перезапишу, т.к. нашлись ошибки

## Пример сценария работы

```text
create_table users name:str age:int
insert users name=Alice age=25
insert users name=Bob age=30
select users
select users where age=25
update users set age=26 where name=Alice
select users where name=Alice
delete users where name=Bob
select users
drop_table users
exit
```

## Команды приложения

`create_table <имя> <колонка:тип> ...` - Создать таблицу с указанными колонками 
`list_tables` - Показать список всех таблиц 
`drop_table <имя>` - Удалить таблицу 
`insert <имя> <колонка=значение> ...` - Добавить запись в таблицу 
`select <имя> [where <условие>]` - Выбрать записи из таблицы 
`update <имя> set <условие> where <условие>` -  Обновить записи в таблице 
`delete <имя> where <условие>` - Удалить записи из таблицы 
`info <имя>` -  Показать описание таблицы 
`help` - Справочная информация 
`exit` - Выход из программы 

## Команды Makefile

```bash
make install          # установка зависимостей
make project          # запуск приложения
make database         # запуск приложения 
make build            # сборка пакета
make package-install  # установка собранного wheel-пакета
make publish          # публикация (требуется токен PyPI)
make lint             # запуск линтера ruff
```
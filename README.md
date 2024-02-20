# Проект: `comics_server`
## Описание

Сайт с каталогом художественных произведений, таких как манга и комиксы. Так же на сайте есть возможность оставлять комментарии к произведениям, добавлять в избранное и реализована функциональность личного кабинета.

## Используется
+ Фреймворк `Flask 2.3.2`
+ База данных `SQLite`
+ Язык программирования `Python 3.11`

## Способ запуска сервера
1. Создание  файла базы данных `bd_comics`
2. Создать дерево папок в основном каталоге
    ```
   - main.py
   ...
   - bd_connect.py
   + bd_comics
   + manga
      * title_name_dir    // example
          * chapter_1     // example
          ...             // example
          * chapter_n     // example
      ```
   + Знаком `-` в примере выше отображаются исходные папки и файлы
   + Знаком `+` в примере выше показаны файлы и папки, которые необходимо создать
   + Знаком `*` в примере выше, отображены примеры папок и файлов, которые создаются автоматически
3. Запустить файл `main.py`, причем в консоле будет выведен ip-адресс на котором хостится сервер
## Структура базы данных
### Список таблиц
+ manga
+ chapters
+ pages
+ files
+ users
+ comments

### Таблица `manga`
#### Описание полей
| Название поля     | Тип поля     | NOT NULL | Primary key | UNIQUE |
|:------------------|:-------------|:--------:|:-----------:|:------:|
| manga_name        | VARCHAR(255) |          |      +      |   +    |
| rus_manga_name    | TEXT         |    +     |             |        |
| manga_description | TEXT         |    +     |             |        |
| manga_title_image | TEXT         |    +     |             |        |
| manga_types       | VARCHAR(32)  |    +     |             |        |
#### SQL-запрос для создание таблиц
```
CREATE TABLE "manga" (
	"manga_name"	VARCHAR(255) UNIQUE,
	"rus_manga_name"	TEXT NOT NULL,
	"manga_description"	TEXT NOT NULL,
	"manga_title_image"	INTEGER NOT NULL,
	"manga_types"	VARCHAR(32) NOT NULL,
	PRIMARY KEY("manga_name")
)
```

### Таблица `chapters`
#### Описание полей

| Название поля  | Тип поля     | NOT NULL | Primary key | UNIQUE |
|:---------------|:-------------|:--------:|:-----------:|:------:|
| manga_name     | VARCHAR(255) |    +     |      +      |   +    |
| chapter_number | INTEGER      |    +     |      +      |   +    |
| chapter_name   | VARCHAR(255) |    +     |             |        |
| chapter_len    | INTEGER      |    +     |             |        |
#### SQL-запрос для создание таблиц
```
CREATE TABLE chapters(
    manga_name VARCHAR(255) NOT NULL,
    chapter_name VARCHAR(255) Not Null,
    chapter_number INTEGER NOT NULL,
    chapter_len INTEGER NOT NULL,
    PRIMARY KEY (manga_name, chapter_number),
    UNIQUE (manga_name, chapter_number)
)
```

### Таблица `pages`
#### Описание полей
| Название поля  | Тип поля     | NOT NULL | Primary key | Unique |
|:---------------|:-------------|:--------:|:-----------:|:------:|
| manga_name     | VARCHAR(255) |    +     |      +      |   +    |
| chapter_number | INTEGER      |    +     |      +      |   +    |
| page_number    | INTEGER      |    +     |      +      |   +    |
| pages_image    | INTEGER      |    +     |             |        |
#### SQL-запрос для создание таблиц
```
CREATE TABLE pages(
    manga_name VARCHAR(255) NOT NULL,
    chapter_number INTEGER NOT NULL,
    page_number INTEGER NOT NULL,
    pages_image INTEGER NOT NULL,
    PRIMARY KEY (manga_name, chapter_number, page_number),
    UNIQUE (manga_name, chapter_number, page_number)

)
```

### Таблица `files`
#### Описание полей
| Название поля | Тип поля | NOT NULL | Primary key | UNIQUE | AUTOINCREMENT |
|:--------------|:---------|:--------:|:-----------:|:------:|:-------------:|
| image_id      | INTEGER  |    +     |      +      |   +    |       +       |
| image_path    | TEXT     |    +     |             |        |               |
| image_name    | TEXT     |    +     |             |        |               |
| image_format  | TEXT     |    +     |             |        |               |
#### SQL-запрос для создание таблиц
```
CREATE TABLE files (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    image_path TEXT NOT NULL,
    image_name TEXT NOT NULL,
    image_format TEXT NOT NULL
)
```

### Таблица `users`
#### Описание полей
| Название поля | Тип поля | NOT NULL | DEFAULT | Primary key | UNIQUE | AUTOINCREMENT |
|:--------------|:---------|:--------:|:-------:|:-----------:|:------:|:-------------:|
| user_id       | INTEGER  |    +     |         |      +      |   +    |       +       |
| user_name     | TEXT     |    +     |         |             |   +    |               |
| user_password | TEXT     |    +     |         |             |        |               |
| role          | INTEGER  |          |    0    |             |        |               |
#### SQL-запрос для создание таблиц
```
CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"user_name"	TEXT NOT NULL UNIQUE,
	"user_password"	TEXT NOT NULL,
	"role"	INTEGER DEFAULT 0,
	PRIMARY KEY("user_id" AUTOINCREMENT)
)
```

### Таблица `comments`
#### Описание полей
| Название поля | Тип поля     | NOT NULL |        IF         | Primary key | UNIQUE |
|:--------------|:-------------|:--------:|:-----------------:|:-----------:|--------|
| user_id       | INTEGER      |          |                   |      +      | +      |
| manga_name    | VARCHAR(255) |          |                   |      +      | +      |
| manga_rating  | INTEGER      |    +     | x >= 0 && x <= 10 |             |        |
| comment       | TEXT         |          |                   |             |        |
#### SQL-запрос для создание таблиц
```
CREATE TABLE comments(
    user_id INTEGER,
    manga_name VARCHAR(255),
    manga_rating INTEGER NOT NULL
        CHECK ( manga_rating >= 0 and manga_rating <= 10 ),
    comment TEXT,
    PRIMARY KEY (user_id, manga_name),
    UNIQUE (user_id, manga_name)
)
```
# api_yamdb
api_yamdb


# Проект «YaMDb API»

### Описание

Проект YaMDb собирает отзывы пользователей на различные произведения.

Авторы проекта:

[Сергей Надршин](https://github.com/Kubich13)

[Екатерина Танцюра](https://github.com/tantsiura)

[Рамиль Ханкильдиев](https://github.com/ramil-khan)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ramil-khan/api_yamdb.git

cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env

source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Импорт данных в БД
Для загрузки данных необходимо запустить поочередно следующие команды в консоли:

```
python api_yamdb/manage.py import_csv --paths static/data/users.csv static/data/category.csv static/data/genre.csv static/data/titles.csv  --models User Category Genre Title

python api_yamdb/manage.py import_csv --paths static/data/genre_title.csv --tables reviews_title_genre

python api_yamdb/manage.py import_csv --paths static/data/review.csv --tables reviews_review

python api_yamdb/manage.py import_csv --paths static/data/comments.csv --tables reviews_comment
```

Скрипт `import_csv` для загрузки данных из CSV в БД находится в следующей директории:
`/api_yamdb/reviews/management/commands/`

В проекте реализован функционал по загрузке файлов формата csv через Django Admin, файлы сохраняются в следующую директорию:
`/static/data/`


### Примеры запросов API

Документация и примеры запросов представлены в формате Redoc.
После запуска отладочного web-сервера проекта документация будет доступна по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/).

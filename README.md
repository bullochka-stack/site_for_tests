# Сайт для составления и прохождения тестов


## Запуск проекта
1) Клонировать репозиторий:

```
git clone https://github.com/Vendetta-source/site_for_tests.git
```

2) Создать виртуальное окружение:

```
python -m venv venv
```

3) Активировать окружение:

Windows: 
```
venv/scripts/activate
```

Linux: 
```
source\venv\bin\activate
```

4) Установить зависимости:

```
pip install -r requirements.txt
```

5) В файле settings.py заполнить необходимые данные.

6) Создать и применить миграции БД:

```
python manage.py makemigrations
python manage.py migrate
```

7) Запустить сервер:

```
python manage.py runserver
```

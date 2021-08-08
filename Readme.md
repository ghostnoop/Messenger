Python 3.8.8
Postgres 12

## Перед запуском
1. `создать файл .env и скопировать туда содержимое .env.example`
2. `в файле .env изменить данные под свою базу данных`

## Запуск
1. `pipenv shell` - инициализация виртуального окружения
2. `pipenv install` - установка зависимостей
3. `python src/manage.py migrate` - запуск миграций
4. `python src/manage.py runserver` - запуск сервера
5. `python src/manage.py createsuperuser` - создание суперпользователя


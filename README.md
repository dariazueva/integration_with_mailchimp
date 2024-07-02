# Интеграция с сервисом Mailchimp для отправки email-сообщений о регистрации пользователя

Этот проект представляет собой интеграцию Django с Mailchimp, использующую Celery для асинхронной отправки писем. Проект включает функционал отправки писем при создании нового пользователя и повторную отправку писем, которые не удалось отправить с первой попытки.

### Основной стек технологий проекта:

python, celery, redis, django, drf, poetry

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:dariazueva/integration_with_mailchimp.git
```

```
cd integration_with_mailchimp
```

Создайте файл .env и заполните его своими данными по образцу:

```
SECRET_KEY = 'ваш-секретный-ключ'

MAILCHIMP_API_KEY = 'ваш-ключ-mailchimp'
MAILCHIMP_DATA_CENTER = 'ваш-data-center-ключ'
MAILCHIMP_TEMPLATE_NAME = 'ваше_mailchimp_template_имя'
```

Cоздать и активировать виртуальное окружение:

Если у вас ещё не установлен Poetry, установите его с помощью следующей команды:
```
pip install poetry
```
```
poetry install
```
```
poetry shell
```

Примененить миграции:
```
python manage.py migrate
```

Создать суперпользователя:

```
python manage.py createsuperuser
```

Запустить проект:

```
python manage.py runserver
```

Настройка Celery:

Если у вас ещё не установлен Redis, установите его с сайта https://github.com/MicrosoftArchive/redis/releases

Запустить сервер Redis в новом терминале:

```
sudo apt-get install redis-server  # Для Ubuntu
brew install redis  # Для Mac
redis-server # Для Win
```


Открыть новый терминал и запустить Celery:

```
cd integration
celery -A integration worker -l info
```

В новом терминале запустить Celery beat:
```
celery -A integration beat -l INFO
```

Запустить тесты:

```
python manage.py test
```

## Автор
Зуева Дарья Дмитриевна
Github https://github.com/dariazueva/
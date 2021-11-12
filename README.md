# dinrplan

## Prerequisites

- Python 3.9+
- PostgreSQL
- poetry

## Installing

1. Create a PostgreSQL database
2. Set these environmental variables:

```
SECRET_KEY
DB_USER
DB_PASSWORD
```

```
poetry install
poetry run python manage.py migrate
```

## Running

```
poetry run python manage.py runserver
```

## Running tests

```
poetry run python manage.py test
```

## Deploying

```commandline
git push heroku master
```

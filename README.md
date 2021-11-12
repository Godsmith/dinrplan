# dinrplan

## Prerequisites

- Python 3.9+
- PostgreSQL
- poetry

## Installing

Create a PostgreSQL database

```commandline
cp .env.example .env
```

Set the environment variables in .env

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

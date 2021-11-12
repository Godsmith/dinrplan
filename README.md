# dinrplan

## Prerequisites

- Python 3.9+
- PostgreSQL
- poetry

## Setting up the development environment

### Create a PostgreSQL database

### Create a .env file

```commandline
cp .env.example .env
```

### Install dependencies

```
poetry install
```

### Install pre-commit

```
pre-commit install
```

### Migrate database

```
poetry run python manage.py migrate
```

## Running development server

```
poetry run python manage.py runserver
```

## Running tests

```
poetry run python manage.py test
```

## Deploying

```commandline
git push
```

Heroku is set to deploy when the Github Actions pass.

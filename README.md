# dinrplan

Meal planner/recipe database built with Python, Django and PostgreSQL

[![Tests](https://github.com/Godsmith/dinrplan/actions/workflows/tests.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/tests.yml)
[![Black](https://github.com/Godsmith/dinrplan/actions/workflows/black.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/black.yml)
[![codecov](https://codecov.io/gh/Godsmith/dinrplan/branch/master/graph/badge.svg?token=DSINFV82XT)](https://codecov.io/gh/Godsmith/dinrplan)

## Prerequisites

- Python 3.9+
- PostgreSQL
- poetry

## Setting up the development environment

### Install PostgreSQL

Make sure to remember the password.

### Create a PostgreSQL database

1. Start psql by searching for psql via the Start menu and pressing Enter
2. Press Enter, Enter, Enter, Enter, enter your password, Enter
3. `CREATE DATABASE dinrplan;`
4. Optionally create a user for the database, or just use the default user.

### Create a .env file

```commandline
cp .env.example .env
```

Edit the database user and password.

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

### Collect static files

```commandline
poetry run python manage.py collectstatic
```

### Ensure tests pass

```commandline
poetry run python manage.py test
```

## Running development server

```
poetry run python manage.py runserver
```

## Running tests

```
poetry run pytest
```

## Deploying

```commandline
git push
```

Heroku is set to deploy when the Github Actions pass.

## Miscellanous

### Starting a shell on heroku

```commandline
heroku run bash
```

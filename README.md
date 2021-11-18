# dinrplan

Meal planner utilizing Python, Django and PostgreSQL

[![Tests](https://github.com/Godsmith/dinrplan/actions/workflows/tests.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/tests.yml)
[![Black](https://github.com/Godsmith/dinrplan/actions/workflows/black.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/black.yml)
[![codecov](https://codecov.io/gh/Godsmith/dinrplan/branch/master/graph/badge.svg?token=DSINFV82XT)](https://codecov.io/gh/Godsmith/dinrplan)

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

## Miscellanous

### Starting a shell on heroku

```commandline
heroku run bash

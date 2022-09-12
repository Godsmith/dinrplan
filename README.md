# dinrplan

Meal planner/recipe database built with Python, Django and PostgreSQL

[![Tests](https://github.com/Godsmith/dinrplan/actions/workflows/tests.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/tests.yml)
[![Black](https://github.com/Godsmith/dinrplan/actions/workflows/black.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/black.yml)
[![codecov](https://codecov.io/gh/Godsmith/dinrplan/branch/master/graph/badge.svg?token=DSINFV82XT)](https://codecov.io/gh/Godsmith/dinrplan)

## Prerequisites

- Python 3.9+
- PostgreSQL
- hatch
- Heroku CLI

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
hatch env create
```

### Install pre-commit

```
hatch run pre-commit install
```

### Migrate database

```
hatch run python manage.py migrate
```

### Collect static files

```commandline
hatch run python manage.py collectstatic
```

### Install playwright

```commandline
hatch run playwright install
```

### Ensure tests pass

```commandline
hatch run pytest
```

## Running development server

```
hatch run python manage.py runserver
```

## Running tests

```
hatch run pytest
```

After changing database schema, run

```commandline
hatch run pytest --create-db
```

to force re-creation of the test database.

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

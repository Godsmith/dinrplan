# dinrplan

Personal meal planner and recipe database built with Python, Django and htmx. Users can view a weekly calendar grid, add and edit meals and recipes, drag and drop meals between days, and upload data via JSON import.

Deployed at [dinrplan.fly.dev](https://dinrplan.fly.dev).

[![Test](https://github.com/Godsmith/dinrplan/actions/workflows/test.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/test.yml)
[![pre-commit](https://github.com/Godsmith/dinrplan/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/pre-commit.yml)
[![Deploy](https://github.com/Godsmith/dinrplan/actions/workflows/deploy.yml/badge.svg)](https://github.com/Godsmith/dinrplan/actions/workflows/deploy.yml)

## Prerequisites

- Python 3.13+
- PostgreSQL
- uv

## Setting up the development environment

### Install PostgreSQL

Make sure to remember the password.

### Create a PostgreSQL database

1. Start psql by searching for psql via the Start menu and pressing Enter
2. Press Enter, Enter, Enter, Enter, enter your password, Enter
3. `CREATE DATABASE dinrplan;`
4. Optionally create a user for the database, or just use the default user.

### Create a .env file

```
cp .env.example .env
```

Edit `.env` with your database credentials. Required variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | PostgreSQL connection string, e.g. `postgres://user:pass@localhost/dinrplan` |
| `DEBUG` | Boolean, defaults to `False` |

### Install dependencies

```
uv sync
```

### Install pre-commit hooks

```
uv run pre-commit install
```

### Migrate database

```
uv run python manage.py migrate
```

### Collect static files

```
uv run python manage.py collectstatic
```

### Install Playwright browsers

```
uv run playwright install
```

### Ensure tests pass

```
uv run pytest
```

## Running the development server

```
uv run python manage.py runserver
```

## Running tests

```
uv run pytest
```

After changing the database schema, force re-creation of the test database:

```
uv run pytest --create-db
```

### Running with coverage

```
uv run coverage run --source="." -m pytest
uv run coverage xml
```

## Deploying

```
git push
```

Deployment to Fly.io is triggered automatically when all GitHub Actions checks pass on push.

Currently, the database is deployed to neon.com. To switch the database host, just update the `DATABASE_URL` secret.

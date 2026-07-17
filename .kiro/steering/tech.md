# Tech Stack

## Language & Runtime
- Python 3.9+

## Framework & Key Libraries
- **Django 4.2** — web framework, ORM, auth, admin
- **htmx 1.8** — AJAX/partial page updates without writing JS (primary interactivity layer)
- **Bootstrap 5.3** — CSS framework (dark mode enabled by default via `data-bs-theme="dark"`)
- **Selectize.js 0.13** — enhanced select inputs for meal search/assignment
- **PostgreSQL** — database (via psycopg2-binary)
- **django-environ** — environment variable / `.env` file management
- **whitenoise** — static file serving in production
- **gunicorn** — WSGI server for production

## Build & Dependency Management
- **hatch** — project/environment/script manager (replaces pip + virtualenv directly)
- Dependencies defined in `pyproject.toml`

## Testing
- **pytest + pytest-django** — test runner
- **pytest-playwright** — end-to-end browser tests (Playwright)
- **coverage / pytest-cov** — code coverage (reported to Codecov)
- Tests reuse the DB by default (`--reuse-db`); pass `--create-db` after schema changes

## Code Style
- **black** — code formatter (enforced via pre-commit and CI)
- **pre-commit** — runs black before each commit

## CI/CD
- GitHub Actions: `test.yml` (pytest + coverage), `black.yml` (format check), `deploy.yml`
- Deployment to Fly.io triggered automatically when all checks pass on push

## Common Commands

```bash
# Install dependencies
hatch env create

# Run development server
hatch run server                          # runs `python manage.py runserver`

# Run all tests
hatch run pytest

# Force test DB re-creation (after schema changes)
hatch run pytest --create-db

# Run migrations
hatch run python manage.py migrate

# Create new migrations
hatch run python manage.py makemigrations

# Collect static files
hatch run python manage.py collectstatic

# Run with coverage
hatch run coverage run --source="." -m pytest
hatch run coverage xml

# Install pre-commit hooks
hatch run pre-commit install
```

## Environment Variables
Configured via `.env` (copy from `.env.example`). Required variables:
- `SECRET_KEY` — Django secret key
- `DATABASE_URL` — PostgreSQL connection string (e.g. `postgres://user:pass@localhost/dinrplan`)
- `DEBUG` — boolean, defaults to `False`

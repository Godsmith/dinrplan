# Tech Stack

## Language & Runtime
- Python 3.13+

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
- **uv** — fast Python package and project manager
- Dependencies defined in `pyproject.toml`

## Testing
- **pytest + pytest-django** — test runner
- **pytest-playwright** — end-to-end browser tests (Playwright)
- **coverage / pytest-cov** — code coverage (reported to Codecov)
- Tests reuse the DB by default (`--reuse-db`); pass `--create-db` after schema changes

## Code Style
- **ruff** — linter and formatter (enforced via pre-commit and CI)
- **pre-commit** — runs ruff and other checks before each commit

## CI/CD
- GitHub Actions: `test.yml` (pytest + coverage), `pre-commit.yml` (linting/formatting), `deploy.yml`
- Deployment to Fly.io triggered automatically when all checks pass on push

## Common Commands

```bash
# Install dependencies
uv sync

# Run development server
uv run python manage.py runserver

# Run all tests
uv run pytest

# Force test DB re-creation (after schema changes)
uv run pytest --create-db

# Run migrations
uv run python manage.py migrate

# Create new migrations
uv run python manage.py makemigrations

# Collect static files
uv run python manage.py collectstatic

# Run with coverage
uv run coverage run --source="." -m pytest
uv run coverage xml

# Install pre-commit hooks
uv run pre-commit install
```

## Environment Variables
Configured via `.env` (copy from `.env.example`). Required variables:
- `SECRET_KEY` — Django secret key
- `DATABASE_URL` — PostgreSQL connection string (e.g. `postgres://user:pass@localhost/dinrplan`)
- `DEBUG` — boolean, defaults to `False`

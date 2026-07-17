# Project Structure

## Top-Level Layout

```
dinrplan/
├── dinrplan/          # Django project package (settings, root URLs, WSGI/ASGI)
├── planner/           # Main app — meals, days, recipes, calendar
├── accounts/          # Registration (sign-up view and form)
├── users/             # Custom User model
├── templates/         # Global templates (base.html, login, signup)
├── manage.py
├── pyproject.toml     # Dependencies and hatch config
├── pytest.ini         # Test configuration
├── Dockerfile
└── fly.toml           # Fly.io deployment config
```

## Django Apps

### `dinrplan/` (project package)
- `settings.py` — all project settings, reads from `.env` via django-environ
- `urls.py` — root URL conf; mounts `planner/`, `accounts/`, and `django.contrib.auth`

### `planner/` (main app)
- `models.py` — `Meal`, `Day`, `Category`, `Comment`
- `views.py` — all planner views (mix of function-based and class-based)
- `urls.py` — namespaced as `planner`
- `forms.py` — `UploadFileForm` for JSON import
- `templates/planner/` — all planner templates
  - `index.html` — main calendar page
  - `weeks.html` — week grid partial (htmx target)
  - `day_table_row.html` — single day row partial
  - `recipes.html` — recipe list page
  - `upload_json.html` — JSON import page
  - `modals/` — htmx-swapped partials: `edit_day.html`, `show_day.html`, `edit_meal.html`, `show_meal.html`
- `static/planner/` — `index.css`, `color_mode_toggler.js`, font, favicon
- `tests/` — all tests for the planner app
  - `conftest.py` — shared pytest fixtures (user, meal, day, recipe, logged_in_client, page)
  - `fixtures/` — JSON fixture files for days and meals
  - `test_*.py` — unit and Playwright e2e tests

### `accounts/`
- Sign-up flow only (`SignUpView`, `CustomUserCreationForm`)
- Templates live in the global `templates/registration/` directory

### `users/`
- `models.py` — `User(AbstractUser)` with `first_week_offset` and `number_of_weeks_to_show` fields
- Referenced via `AUTH_USER_MODEL = "users.User"` — always use `settings.AUTH_USER_MODEL` in FKs

### `templates/` (global)
- `base.html` — shared layout: Bootstrap, htmx, Selectize CDN links, navbar, dark mode toggle
- `registration/` — `login.html`, `signup.html`

## Key Conventions

- **Data ownership**: `Meal` has `author` FK, `Day` has `user` FK — always filter querysets by the current user
- **`get_or_create` pattern**: `Day` and `Meal` objects are often created on the fly with `get_or_create`
- **htmx partials**: views that serve htmx responses return partial templates (weeks, day rows, modals); full-page views extend `base.html`
- **URL namespacing**: use `reverse("planner:<name>")` for all planner URLs
- **Class-based views**: preferred for CRUD (Django generic CBVs); function-based views used for simpler cases (`index`)
- **Migrations**: live in each app's `migrations/` directory; always create via `makemigrations` after model changes
- **Tests**: unit tests use `logged_in_client` fixture; browser tests use `page` fixture (Playwright); all fixtures defined in `planner/tests/conftest.py`

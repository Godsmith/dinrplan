import os

import pytest
from django.utils import timezone

from planner.models import Day
from planner.models import Meal
from users.models import User

# This is needed for running Django tests with playwright
# See https://github.com/microsoft/playwright-pytest/issues/29
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def user(client, db):
    return User.objects.create_user(username="user1", password="user1")


@pytest.fixture
def meal(user):
    return Meal.objects.create(name="My recipe", author=user)


@pytest.fixture
def day(user, meal):
    day, _ = Day.objects.get_or_create(date=timezone.now().date(), user=user)
    day.meals.add(meal)
    return day


@pytest.fixture
def logged_in_user(client, user):
    client.login(username="user1", password="user1")


@pytest.fixture
def logged_in_user_on_live_server(live_server, user, page):
    page.goto(live_server.url + "/accounts/login")
    page.fill('input[name="username"]', "user1")
    page.fill('input[name="password"]', "user1")
    page.click("button[type='submit']")
    return live_server

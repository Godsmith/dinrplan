import os
from pathlib import Path

import pytest
from django.test.client import Client
from django.utils import timezone

from planner.models import Day
from planner.models import Meal
from users.models import User

# This is needed for running Django tests with playwright
# See https://github.com/microsoft/playwright-pytest/issues/29
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def page(context, user):
    client = Client()
    client.login(username="user1", password="user1")
    cookie = client.cookies["sessionid"]
    context.add_cookies(
        [
            {
                "name": "sessionid",
                "value": cookie.value,
                "secure": False,
                "domain": "localhost",
                "path": "/",
            }
        ]
    )
    return context.new_page()


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
def logged_in_client(client, user):
    client.login(username="user1", password="user1")
    return client


@pytest.fixture
def create_meal_for_today(user):
    day, _ = Day.objects.get_or_create(date=timezone.now().date(), user=user)
    meal = Meal.objects.create(
        name="My recipe",
        author=user,
        source="mysource",
        persons=8,
        time="30 min",
        ingredients="myingredients",
        steps="mysteps",
    )
    day.meals.add(meal)

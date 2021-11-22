import pytest
from django.utils import timezone

from planner.models import Day
from planner.models import Meal
from users.models import User


@pytest.fixture
def user(client, db):
    return User.objects.create_user(username="user1", password="user1")


@pytest.fixture
def meal(user):
    return Meal.objects.create(name="My recipe", author=user)


@pytest.fixture
def day(user, meal):
    day = Day.objects.create(date=timezone.now().date(), user=user)
    day.meals.add(meal)
    return day


# @pytest.fixture
# def logged_in_user:
#     client.login(username="user1", password="user1")

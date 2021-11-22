from django.urls import reverse
from django.utils import timezone
import pytest


@pytest.mark.django_db
def test_posting_name_inserts_that_meal_into_the_day(client, meal, day):
    client.login(username="user1", password="user1")

    client.post(
        reverse("planner:day", kwargs={"date": timezone.now().date()}),
        data={"select": ["My recipe"]},
    )

    assert list(day.meals.all()) == [meal]


@pytest.mark.django_db
def test_show_current_day_text(client, meal, day):
    client.login(username="user1", password="user1")

    response = client.get(
        reverse("planner:day", kwargs={"date": timezone.now().date()})
    )

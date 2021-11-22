from pathlib import Path

import pytest
from django.urls import reverse

from planner.models import Day
from planner.models import Meal


@pytest.mark.django_db
def test_upload_creates_meal_and_day(client, user):
    client.login(username="user1", password="user1")
    fixtures = Path(__file__).parent / "fixtures"
    with open(fixtures / "meals.json", "rb") as meals_file:
        with open(fixtures / "days.json", "rb") as days_file:
            client.post(
                reverse("planner:upload"),
                data={"meals": meals_file, "days": days_file},
            )

    assert Meal.objects.all()[0].name == "Vegobiffar med kryddsmör"
    assert Day.objects.all()[0].date.isoformat() == "2020-02-18"

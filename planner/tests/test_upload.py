from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from planner.models import Meal, Day
from users.models import User


class UploadTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        self.client.login(username="user1", password="user1")

    def test_upload_creates_meal_and_day(self):
        fixtures = Path(__file__).parent / "fixtures"
        with open(fixtures / "meals.json", "rb") as meals_file:
            with open(fixtures / "days.json", "rb") as days_file:
                self.client.post(
                    reverse("planner:upload"),
                    data={"meals": meals_file, "days": days_file},
                )

        self.assertEqual(Meal.objects.all()[0].name, "Vegobiffar med kryddsmör")
        self.assertEqual(Day.objects.all()[0].date.isoformat(), "2020-02-18")

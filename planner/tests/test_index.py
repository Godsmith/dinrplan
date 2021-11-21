from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from planner.models import Meal, Day
from users.models import User


class MainViewTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        meal = Meal.objects.create(name="My recipe", author=user1)
        day = Day.objects.create(date=timezone.now().date(), user=user1)
        day.meals.add(meal)

    def test_todays_recipe_is_not_shown_on_main_page_if_not_logged_in(self):
        response = self.client.get("/")

        self.assertNotIn("My recipe", str(response.content))

    def test_todays_recipe_is_shown_on_main_page_if_logged_in(self):
        self.client.login(username="user1", password="user1")

        response = self.client.get("/")

        self.assertInHTML("My recipe", str(response.content))

    def test_posting_week_offset_and_count_updates_database(self):
        self.client.login(username="user1", password="user1")

        self.client.post(
            reverse("planner:update_weeks"),
            data={"first-week-offset": ["2"], "number-of-weeks-to-show": ["6"]},
        )

        monday_current_week = timezone.now().date() - timedelta(
            days=timezone.now().date().weekday()
        )
        monday_first_week_shown = monday_current_week + timedelta(days=-2 * 7)
        monday_last_week_shown = monday_current_week + timedelta(days=3 * 7)

        response = self.client.get("/")

        self.assertIn(monday_first_week_shown.isoformat(), str(response.content))
        self.assertIn(monday_last_week_shown.isoformat(), str(response.content))
        self.assertEqual(str(response.content).count("Monday"), 6)

        self.assertIn("My recipe", str(response.content))

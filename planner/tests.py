from datetime import timedelta
from pathlib import Path

from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from users.models import User

from .models import Meal, Day


class MealModelTests(TestCase):
    def test_default_persons_is_4(self):
        m = Meal()
        self.assertEquals(m.persons, 4)


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


class DayViewTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        self.meal = Meal.objects.create(name="My recipe", author=user1)
        self.day = Day.objects.create(date=timezone.now().date(), user=user1)

    def test_posting_name_inserts_that_meal_into_the_day(self):
        self.client.login(username="user1", password="user1")

        self.client.post(
            reverse("planner:day", kwargs={"date": timezone.now().date()}),
            data={"select": ["My recipe"]},
        )

        self.assertEqual(list(self.day.meals.all()), [self.meal])

    def test_show_current_day_text(self):
        self.client.login(username="user1", password="user1")
        self.day.meals.add(self.meal)

        response = self.client.get(
            reverse("planner:day", kwargs={"date": timezone.now().date()})
        )

        self.assertIn("My recipe", str(response.content))


class ShowMealTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        self.meal = Meal.objects.create(
            name="My recipe",
            author=user1,
            source="mysource",
            persons=8,
            time="30 min",
            ingredients="myingredients",
            steps="mysteps",
        )
        self.day = Day.objects.create(date=timezone.now().date(), user=user1)
        self.client.login(username="user1", password="user1")

    def test_shows_all_properties(self):
        response = self.client.get(
            reverse("planner:showmeal", kwargs={"pk": self.meal.pk})
        )
        for text in [
            "My recipe",
            "mysource",
            "8",
            "30 min",
            "myingredients",
            "mysteps",
        ]:
            with self.subTest():
                self.assertIn(text, str(response.content))

    def test_posting_comment_shows_that_comment(self):
        self.client.post(
            reverse("planner:createcomment", kwargs={"pk": self.meal.pk}),
            data={"text": "My comment text"},
        )
        response = self.client.get(
            reverse("planner:showmeal", kwargs={"pk": self.meal.pk})
        )
        for text in ["user1", "My comment text"]:
            with self.subTest():
                self.assertIn(text, str(response.content))


class UploadTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        self.client.login(username="user1", password="user1")

    def test_upload_creates_meal_and_day(self):
        fixtures = Path(__file__).parent / "tests" / "fixtures"
        with open(fixtures / "meals.json", "rb") as meals_file:
            with open(fixtures / "days.json", "rb") as days_file:
                self.client.post(
                    reverse("planner:upload"),
                    data={"meals": meals_file, "days": days_file},
                )

        self.assertEqual(Meal.objects.all()[0].name, "Vegobiffar med kryddsmör")
        self.assertEqual(Day.objects.all()[0].date.isoformat(), "2020-02-18")

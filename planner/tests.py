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


class DayViewTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        self.meal = Meal.objects.create(name="My recipe", author=user1)
        self.day = Day.objects.create(date=timezone.now().date(), user=user1)

    def test_posting_name_inserts_that_meal_into_the_day(self):
        self.client.login(username="user1", password="user1")

        self.client.post(
            reverse("planner:day", kwargs={"date": timezone.now().date()}),
            data={"text": "My recipe"},
        )

        self.assertEqual(list(self.day.meals.all()), [self.meal])

    def test_show_current_day_text(self):
        self.client.login(username="user1", password="user1")
        self.day.meals.add(self.meal)

        response = self.client.get(
            reverse("planner:day", kwargs={"date": timezone.now().date()})
        )

        self.assertIn("My recipe", str(response.content))

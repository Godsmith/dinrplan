from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from planner.models import Meal, Day
from users.models import User


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

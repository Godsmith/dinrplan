from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from planner.models import Meal, Day
from users.models import User


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

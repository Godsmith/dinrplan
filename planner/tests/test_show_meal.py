import pytest
from django.urls import reverse

from planner.models import Meal


@pytest.fixture
def meal_with_all_attributes(client, user, day):
    client.login(username="user1", password="user1")
    meal = Meal.objects.create(
        name="My recipe",
        author=user,
        source="mysource",
        persons=8,
        time="30 min",
        ingredients="myingredients",
        steps="mysteps",
    )
    return meal


def test_shows_all_properties(client, meal_with_all_attributes):
    response = client.get(
        reverse("planner:showmeal", kwargs={"pk": meal_with_all_attributes.pk})
    )
    for text in [
        "My recipe",
        "mysource",
        "8",
        "30 min",
        "myingredients",
        "mysteps",
    ]:
        assert text in str(response.content)


def test_posting_comment_shows_that_comment(client, meal_with_all_attributes):
    client.post(
        reverse("planner:create_comment", kwargs={"pk": meal_with_all_attributes.pk}),
        data={"text": "My comment text"},
    )
    response = client.get(
        reverse("planner:showmeal", kwargs={"pk": meal_with_all_attributes.pk})
    )
    for text in ["user1", "My comment text"]:
        assert text in str(response.content)

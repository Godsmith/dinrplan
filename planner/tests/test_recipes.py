import pytest

from planner.models import Meal


@pytest.fixture
def create_meal_for_today(day, user):
    meal = Meal.objects.create(
        name="My recipe",
        author=user,
        source="mysource",
        persons=8,
        time="30 min",
        ingredients="myingredients",
        steps="mysteps",
    )
    day.meals.add(meal)


def test_not_created_recipes_are_not_visible_on_recipes_page(
    logged_in_user_on_live_server, page, day, user
):
    # Arrange

    # Act
    page.goto(logged_in_user_on_live_server.url + "/recipes")

    # Assert
    assert "My recipe" not in page.content()


def test_recipes_are_visible_on_recipes_page(
    logged_in_user_on_live_server, page, create_meal_for_today
):
    # Arrange

    # Act
    page.goto(logged_in_user_on_live_server.url + "/recipes")

    # Assert
    assert "My recipe" in page.content()


def test_deleting_meal_removes_it_from_list(
    logged_in_user_on_live_server, page, create_meal_for_today
):
    # Arrange
    page.goto(logged_in_user_on_live_server.url + "/recipes")
    page.check("input[type='checkbox']")
    page.on("dialog", lambda dialog: dialog.accept())

    # Act
    page.click("#delete-selected")

    # Assert
    assert "My recipe" not in page.content()

from planner.models import Meal


def test_not_created_recipes_are_not_visible_on_recipes_page(
    logged_in_user_on_live_server, page, day, user
):
    # Arrange

    # Act
    page.goto(logged_in_user_on_live_server.url + "/recipes")

    # Assert
    assert "My recipe" not in page.content()


def test_recipes_are_visible_on_recipes_page(
    logged_in_user_on_live_server, page, day, user
):
    # Arrange
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

    # Act
    page.goto(logged_in_user_on_live_server.url + "/recipes")

    # Assert
    assert "My recipe" in page.content()

from planner.models import Meal


def test_meals_without_source_has_class_does_not_exist(
    logged_in_user_on_live_server, day, page
):
    page.goto(logged_in_user_on_live_server.url)

    assert page.is_visible(".does-not-exist")
    assert not page.is_visible(".exists")


def test_meals_with_source_has_class_exists(
    logged_in_user_on_live_server, day, page, user
):
    meal, _ = Meal.objects.get_or_create(name="My recipe", author=user)
    meal.source = "my_source"
    meal.save()

    page.goto(logged_in_user_on_live_server.url)

    assert not page.is_visible(".does-not-exist")
    assert page.is_visible(".exists")


def test_adding_source_to_meal_makes_that_meal_exist(
    logged_in_user_on_live_server, day, user, page
):
    page.goto(logged_in_user_on_live_server.url)
    page.click(".does-not-exist")
    page.fill('input[name="source"]', "my_source")
    page.click('button[form="update-meal"]')

    assert not page.is_visible(".does-not-exist")
    assert page.is_visible(".exists")


def test_clicking_meal_that_does_not_exist_opens_edit_dialog(
    logged_in_user_on_live_server, day, user, page
):
    page.goto(logged_in_user_on_live_server.url)

    assert not page.is_visible("input.name")

    page.click(".does-not-exist")

    assert not page.is_visible("input.name")


def test_clicking_meal_that_exists_opens_edit_dialog(
    logged_in_user_on_live_server, day, user, page
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
    page.goto(logged_in_user_on_live_server.url)
    assert not page.is_visible("input.name")

    # Act
    page.click(".exists")

    # Assert
    page.wait_for_load_state("networkidle")
    assert "Source" in str(page.content())

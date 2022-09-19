from playwright.sync_api import Page

from planner.models import Category
from planner.models import Meal


def test_meals_without_source_has_class_does_not_exist(logged_in_client, day):
    response = logged_in_client.get("/")

    assert "does-not-exist" in str(response.content)
    assert "exists" not in str(response.content)


def test_meals_with_source_has_class_exists(logged_in_client, create_meal_for_today):
    response = logged_in_client.get("/")

    assert "exists" in str(response.content)
    assert "does-not-exist" not in str(response.content)


def test_adding_source_to_meal_makes_that_meal_exist(live_server, day, page: Page):
    page.goto(live_server.url)
    page.click(".does-not-exist")
    page.fill('input[name="source"]', "my_source")
    page.click('button[form="update-meal"]')
    page.wait_for_selector(".does-not-exist", state="hidden")

    assert page.is_visible(".exists")


def test_clicking_meal_that_does_not_exist_opens_edit_dialog(live_server, day, page):
    page.goto(live_server.url)

    assert not page.is_visible("input.name")

    page.click(".does-not-exist")

    # TODO: is this correct? Should there be a "not" here?
    assert not page.is_visible("input.name")


def test_clicking_meal_that_exists_opens_show_dialog(live_server, day, user, page):
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
    page.goto(live_server.url)
    assert not page.is_visible("input.name")

    # Act
    page.click(".exists")

    # Assert
    page.wait_for_load_state("networkidle")

    # TODO: this is a poor way of testing if this modal is open, check for an id instead
    assert "Source" in str(page.content())


def test_add_category_to_meal(live_server, day, user, page: Page):
    # Arrange
    Category.objects.create(name="Vegetariskt")
    page.goto(live_server.url)
    page.click(".does-not-exist")

    # Act
    page.click(".selectize-input")
    page.type(".selectize-input", "Vegetariskt")
    page.keyboard.press("Enter")
    page.click('button[form="update-meal"]')
    page.wait_for_selector('button[form="update-meal"]', state="hidden")

    # Assert
    assert Meal.objects.all()[0].categories.all()[0].name == "Vegetariskt"

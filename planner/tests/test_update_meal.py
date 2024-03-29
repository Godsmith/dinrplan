from playwright.sync_api import Page

from planner.models import Category
from planner.models import Meal


def test_meal_has_class_text_danger(logged_in_client, create_meal_for_today):
    response = logged_in_client.get("/")

    assert "text-danger" in str(response.content)
    assert "text-primary" not in str(response.content)


def test_recipe_has_class_text_primary(logged_in_client, create_recipe_for_today):
    response = logged_in_client.get("/")

    assert "text-primary" in str(response.content)
    assert "text-danger" not in str(response.content)


def test_editing_and_pressing_ok_to_meal_makes_that_meal_exist(
    live_server, day, page: Page
):
    page.goto(live_server.url)
    page.click(".text-danger")
    page.click('button[form="update-meal"]')
    page.wait_for_selector(".text-danger", state="hidden")

    assert page.is_visible(".text-primary")


def test_create_empty_meal(live_server, day, page: Page):
    page.goto(live_server.url)
    page.click(".text-danger")
    page.click('button[form="update-meal"]')

    page.wait_for_selector(".text-primary", state="visible")


def test_clicking_meal_that_does_not_exist_opens_edit_dialog(live_server, day, page):
    page.goto(live_server.url)

    assert not page.is_visible("input.name")

    page.click(".text-danger")

    # TODO: is this correct? Should there be a "not" here?
    assert not page.is_visible("input.name")


def test_clicking_meal_that_exists_opens_show_dialog(live_server, day, user, page):
    # Arrange
    meal = Meal.objects.create(name="My recipe", author=user, is_recipe=True)
    day.meals.add(meal)
    page.goto(live_server.url)
    assert not page.is_visible("input.name")

    # Act
    page.click(".text-primary")

    # Assert
    page.wait_for_load_state("networkidle")

    # TODO: this is a poor way of testing if this modal is open, check for an id instead
    assert "Source" in str(page.content())


def test_add_category_to_meal(live_server, day, user, page: Page):
    # Arrange
    Category.objects.create(name="Vegetariskt")
    page.goto(live_server.url)
    page.click(".text-danger")

    # Act
    page.click(".selectize-input")
    page.type(".selectize-input", "Vegetariskt")
    page.keyboard.press("Enter")
    page.click('button[form="update-meal"]')
    page.wait_for_selector('button[form="update-meal"]', state="hidden")

    # Assert
    assert Meal.objects.all()[0].categories.all()[0].name == "Vegetariskt"

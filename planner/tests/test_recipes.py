import pytest

from planner.models import Meal


def test_meal_modal_is_hidden_by_default(live_server, page, create_meal_for_today):
    # Arrange
    page.goto(live_server.url + "/recipes")

    # Act

    # Assert
    assert page.is_hidden(".modal")


def test_clicking_recipe_opens_modal(live_server, page, create_meal_for_today):
    # Arrange
    page.goto(live_server.url + "/recipes")

    # Act
    page.click(".exists")
    page.wait_for_load_state("networkidle")
    page.click("#edit-meal")
    page.wait_for_load_state("networkidle")
    page.click("button[form='update-meal']")

    # Assert
    assert "recipes" in page.url


def test_submitting_edited_recipe_returns_to_recipes_page(
    live_server, page, create_meal_for_today
):
    # Arrange
    page.goto(live_server.url + "/recipes")

    # Act
    page.click(".exists")
    page.wait_for_load_state("networkidle")

    # Assert
    assert page.is_visible(".modal")


def test_not_created_recipes_are_not_visible_on_recipes_page(
    logged_in_client, page, day
):
    # Arrange

    # Act
    response = logged_in_client.get("/recipes")

    # Assert
    assert "My recipe" not in str(response.content)


def test_recipes_are_visible_on_recipes_page(logged_in_client, create_meal_for_today):
    # Arrange

    # Act
    response = logged_in_client.get("/recipes")

    # Assert
    assert "My recipe" in str(response.content)


def test_deleting_meal_removes_it_from_list(live_server, page, create_meal_for_today):
    # Arrange
    page.goto(live_server.url + "/recipes")
    page.check("input[type='checkbox']")
    page.on("dialog", lambda dialog: dialog.accept())

    # Act
    page.click("#delete-selected")

    # Assert
    assert "My recipe" not in page.content()

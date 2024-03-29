def test_modal_is_hidden_by_default(live_server, page, create_recipe_for_today):
    # Arrange
    page.goto(live_server.url + "/recipes")

    # Act

    # Assert
    assert page.is_hidden(".modal")


def test_clicking_recipe_opens_modal(live_server, page, create_recipe_for_today):
    # Arrange
    page.goto(live_server.url + "/recipes")

    # Act
    page.click(".text-primary")
    page.click("#edit-meal")
    page.click("button[form='update-meal']")

    # Assert
    assert "recipes" in page.url


def test_submitting_edited_recipe_returns_to_recipes_page(
    live_server, page, create_recipe_for_today
):
    # Arrange
    page.goto(live_server.url + "/recipes")

    # Act
    page.click(".text-primary")
    page.wait_for_load_state("networkidle")

    # Assert
    assert page.is_visible(".modal")


def test_meals_that_are_not_recipes_are_not_visible_on_recipes_page(
    logged_in_client, page, create_meal_for_today
):
    # Arrange

    # Act
    response = logged_in_client.get("/recipes")

    # Assert
    assert "Meal for today" not in str(response.content)


def test_recipes_are_visible_on_recipes_page(logged_in_client, create_recipe_for_today):
    # Arrange

    # Act
    response = logged_in_client.get("/recipes")

    # Assert
    assert "Recipe for today" in str(response.content)


def test_deleting_meal_removes_it_from_list(live_server, page, create_recipe_for_today):
    # Arrange
    page.goto(f"{live_server.url}/recipes")
    page.on("dialog", lambda dialog: dialog.accept())

    # Act
    page.click("button.recipe")
    page.click(".dropdown-item.delete")

    # Assert
    assert "Recipe for today" not in page.content()


class TestAddMeal:
    def test_show_14_days(self, live_server, page, recipe):
        # Arrange
        page.goto(f"{live_server.url}/recipes")

        # Act
        page.click("button.recipe")
        page.click(".dropdown-item.add-to-day")

        # Assert
        assert page.locator(".dropdown-item.add-meal").count() == 14

    def test_add_meal_to_day(self, live_server, page, recipe):
        # Arrange
        page.goto(f"{live_server.url}/recipes")

        # Act
        # Add the first recipe to the first available day (tomorrow)
        page.click("button.recipe")
        page.click(".dropdown-item.add-to-day")
        page.click(".dropdown-item.add-meal")

        # Assert
        page.goto(live_server.url)
        assert "Recipe for today" in page.content()

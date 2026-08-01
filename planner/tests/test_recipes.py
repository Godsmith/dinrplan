from planner.models import Day
from planner.models import Meal


class TestRecipesSorting:
    def test_recipes_sorted_by_times_cooked_descending(self, logged_in_client, user):
        # Arrange
        rarely = Meal.objects.create(name="Rarely cooked", author=user, is_recipe=True)
        often = Meal.objects.create(name="Often cooked", author=user, is_recipe=True)

        day1, _ = Day.objects.get_or_create(date="2026-01-01", user=user)
        day2, _ = Day.objects.get_or_create(date="2026-01-02", user=user)
        day3, _ = Day.objects.get_or_create(date="2026-01-03", user=user)

        day1.meals.add(rarely)  # 1 time
        day1.meals.add(often)
        day2.meals.add(often)
        day3.meals.add(often)  # 3 times

        # Act
        response = logged_in_client.get("/recipes")
        meals = list(response.context["meals"])

        # Assert
        assert meals.index(often) < meals.index(rarely)

    def test_recipes_with_equal_times_sorted_by_last_cooked_descending(
        self, logged_in_client, user
    ):
        # Arrange
        older = Meal.objects.create(name="Older", author=user, is_recipe=True)
        newer = Meal.objects.create(name="Newer", author=user, is_recipe=True)

        day_old, _ = Day.objects.get_or_create(date="2026-01-01", user=user)
        day_new, _ = Day.objects.get_or_create(date="2026-06-01", user=user)

        day_old.meals.add(older)
        day_new.meals.add(newer)

        # Act
        response = logged_in_client.get("/recipes")
        meals = list(response.context["meals"])

        # Assert
        assert meals.index(newer) < meals.index(older)

    def test_never_cooked_recipe_shows_empty_last_cooked(self, logged_in_client, user):
        # Arrange
        Meal.objects.create(name="Never cooked", author=user, is_recipe=True)

        # Act
        response = logged_in_client.get("/recipes")
        meals = list(response.context["meals"])

        # Assert
        assert meals[0].last_cooked is None
        assert meals[0].times_cooked == 0

    def test_times_cooked_only_counts_current_users_days(
        self, logged_in_client, user, client, db
    ):
        # Arrange — another user also cooks the same recipe
        from users.models import User

        other_user = User.objects.create_user(username="other", password="other")
        Meal.objects.create(name="Shared name", author=user, is_recipe=True)

        their_recipe = Meal.objects.create(
            name="Shared name", author=other_user, is_recipe=True
        )
        other_day, _ = Day.objects.get_or_create(date="2026-01-01", user=other_user)
        other_day.meals.add(their_recipe)

        # Act
        response = logged_in_client.get("/recipes")
        meals = list(response.context["meals"])

        # Assert — current user's recipe shows 0, not 1
        assert meals[0].times_cooked == 0


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

from django.urls import reverse
from django.utils import timezone
from playwright.sync_api import Page


def test_all_modals_are_hidden_by_default(live_server, page, create_meal_for_today):
    # Arrange
    page.goto(live_server.url)

    # Act

    # Assert
    assert page.is_hidden(".selectize-input")


def test_clicking_edit_day_button_shows_input_for_editing_day(live_server, day, page):
    # Arrange
    date = timezone.now().date().isoformat()
    page.goto(live_server.url)

    # Act
    page.click(f"a.day-{date}")
    page.wait_for_load_state("networkidle")

    # Assert
    assert page.is_visible(".selectize-input")


def test_clicking_empty_day_shows_input_for_editing_day(live_server, day, page: Page):
    # Arrange
    tomorrow = (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
    page.goto(live_server.url)

    # Act
    page.click(f"div.day-{tomorrow}")

    # Assert
    assert page.wait_for_selector(".selectize-input", state="visible")


def test_clicking_day_with_meal_does_not_show_input_for_editing_day(
    live_server, day, page: Page
):
    # Arrange
    today = timezone.now().date().isoformat()
    page.goto(live_server.url)

    # Act
    page.click(f"div.day-{today}")
    page.wait_for_load_state("networkidle")

    # Assert
    assert page.is_hidden(".selectize-input")


def test_clicking_edit_day_button_twice_hides_input_for_editing_day_again(
    live_server, day, page: Page
):
    # Arrange
    date = timezone.now().date().isoformat()
    page.goto(live_server.url)

    # Act
    page.click(f"a.day-{date}")
    page.click(f"a.day-{date}")

    # Assert
    page.wait_for_selector(".selectize-input", state="hidden")


def test_clicking_edit_day_button_reloading_the_page_and_clicking_again_shows_input(
    live_server, day, page: Page
):
    """Previously, the edit state of a day was preserved in the session when reloading
    the page even though the edit button was hidden, creating a discrepancy between what
    was shown and what was stored.
    """
    # Arrange
    date = timezone.now().date().isoformat()
    page.goto(live_server.url)

    # Act
    page.click(f"a.day-{date}")
    page.goto(live_server.url)
    page.click(f"a.day-{date}")
    page.wait_for_load_state("networkidle")

    # Assert
    assert page.is_visible(".selectize-input")


def test_editing_two_days_and_then_pressing_edit_cancels_just_one_edit(
    live_server, day, page: Page
):
    # Given a logged in user on the main page
    page.goto(live_server.url)

    # When clicking the first and second edit buttons
    page.locator(".edit-day").first.click()
    page.locator(".edit-day").nth(1).click()
    # Waiting for load state not always working here for some reason, so wait
    # a specific time instaed
    page.wait_for_selector(".selectize-input")
    page.wait_for_timeout(100)
    # Then there shall be two selectize inputs
    assert page.locator(".selectize-input").count() == 2

    # When one edit button is pressed
    page.locator(".edit-day").first.click()
    page.wait_for_timeout(100)

    # There is just one cancel button visible
    assert page.locator(".selectize-input").count() == 1


def test_posting_name_inserts_that_meal_into_the_day(logged_in_client, meal, day):
    logged_in_client.post(
        reverse("planner:edit_day", kwargs={"date": timezone.now().date()}),
        data={"select": ["Meal for today"]},
    )

    assert list(day.meals.all()) == [meal]


def test_show_current_day_text(logged_in_client, meal, day):
    logged_in_client.get(
        reverse("planner:edit_day", kwargs={"date": timezone.now().date()})
    )

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


def test_editing_two_days_and_then_pressing_cancel_closes_just_one_edit(
    live_server, day, page: Page
):
    # Given a logged in user on the main page
    page.goto(live_server.url)

    # When clicking the first and second edit buttons
    page.locator(".edit-day").first.click()
    page.locator(".edit-day").nth(1).click()
    # Waiting for load state not always working here for some reason, so wait
    # a specific time instaed
    page.wait_for_timeout(100)
    # Then there shall be two cancel buttons visible
    assert page.locator(".cancel-edit-day").count() == 2

    # When one cancel button is pressed
    page.locator(".cancel-edit-day").first.click()
    page.wait_for_timeout(100)

    # There is just one cancel button visible
    assert page.locator(".cancel-edit-day").count() == 1


def test_posting_name_inserts_that_meal_into_the_day(logged_in_client, meal, day):
    logged_in_client.post(
        reverse("planner:edit_day", kwargs={"date": timezone.now().date()}),
        data={"select": ["Recipe for today"]},
    )

    assert list(day.meals.all()) == [meal]


def test_show_current_day_text(logged_in_client, meal, day):
    logged_in_client.get(
        reverse("planner:edit_day", kwargs={"date": timezone.now().date()})
    )

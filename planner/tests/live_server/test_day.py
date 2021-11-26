from django.utils import timezone


def test_all_modals_are_hidden_by_default(
    logged_in_user_on_live_server, page, create_meal_for_today
):
    # Arrange
    page.goto(logged_in_user_on_live_server.url)

    # Act

    # Assert
    assert page.is_hidden(".selectize-input")


def test_clicking_edit_day_button_shows_input_for_editing_day(
    logged_in_user_on_live_server, day, user, page
):
    # Arrange
    date = timezone.now().date().isoformat()
    page.goto(logged_in_user_on_live_server.url)

    # Act
    page.click(f"a.day-{date}")
    page.wait_for_load_state("networkidle")

    # Assert
    assert page.is_visible(".selectize-input")

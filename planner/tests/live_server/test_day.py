from django.utils import timezone


def test_all_modals_are_hidden_by_default(
    logged_in_user_on_live_server, page, create_meal_for_today
):
    # Arrange
    page.goto(logged_in_user_on_live_server.url)

    # Act

    # Assert
    assert page.is_hidden(".selectize-input")


def test_clicking_day_opens_day_modal(logged_in_user_on_live_server, day, user, page):
    page.goto(logged_in_user_on_live_server.url)
    # Arrange
    date = timezone.now().date().isoformat()

    # Act
    page.click(f"a.day-{date}")
    page.wait_for_load_state("networkidle")

    # Assert
    assert page.is_visible(".selectize-input")

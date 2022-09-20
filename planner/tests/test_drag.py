from django.utils import timezone
from playwright.sync_api import Page


def test_drag(create_meal_for_today_and_tomorrow, live_server, page: Page):
    """When dragging one day on top of another, the planned meals for the days shall switch."""
    today = timezone.now().date().isoformat()
    tomorrow = (timezone.now().date() + timezone.timedelta(days=1)).isoformat()

    # Given a logged in user on the main page
    page.goto(live_server.url)

    # When dragging today's table cell on top of tomorrow's table cell
    page.dispatch_event(f"td.day-{today}", "dragstart")
    page.dispatch_event(f"td.day-{tomorrow}", "drop")
    page.wait_for_load_state("networkidle")

    # Then the name of the meals shall be exchanged
    assert page.text_content(f"td.day-{tomorrow} a") == "Meal for today"
    assert page.text_content(f"td.day-{today} a") == "Meal for tomorrow"

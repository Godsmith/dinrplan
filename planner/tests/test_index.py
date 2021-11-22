from datetime import timedelta

from django.urls import reverse
from django.utils import timezone


def test_todays_recipe_is_not_shown_on_main_page_if_not_logged_in(client, day):
    response = client.get("/")

    assert "My recipe" not in str(response.content)


def test_todays_recipe_is_shown_on_main_page_if_logged_in(client, day):
    client.login(username="user1", password="user1")

    response = client.get("/")

    assert "My recipe" in str(response.content)


def test_posting_week_offset_and_count_updates_database(client, day):
    client.login(username="user1", password="user1")

    client.post(
        reverse("planner:update_weeks"),
        data={"first-week-offset": ["2"], "number-of-weeks-to-show": ["6"]},
    )

    monday_current_week = timezone.now().date() - timedelta(
        days=timezone.now().date().weekday()
    )
    monday_first_week_shown = monday_current_week + timedelta(days=-2 * 7)
    monday_last_week_shown = monday_current_week + timedelta(days=3 * 7)

    response = client.get("/")

    assert monday_first_week_shown.isoformat() in str(response.content)
    assert monday_last_week_shown.isoformat() in str(response.content)
    assert str(response.content).count("Monday") == 6

    assert "My recipe" in str(response.content)


# def test_changing_the_dropbox_controlling_how_many_weeks_are_displayed_changes_how_many_weeks_are_displayed(
#     client, user
# ):
#     client.login(username="user1", password="user1")

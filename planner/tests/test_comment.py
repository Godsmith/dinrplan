import pytest
from playwright.sync_api import Page


@pytest.fixture
def visible_comment_form(live_server, create_recipe_for_today, page: Page):
    page.goto(live_server.url)
    page.click("a.exists")
    page.click("a.comment-show")
    page.wait_for_selector("button.comment-submit")


def test_clicking_comment_button_shows_create_comment_form(visible_comment_form):
    pass


def test_clicking_submit_button_shows_created_comment(visible_comment_form, page: Page):
    # Arrange
    page.type("textarea", "mycomment")

    # Act
    page.click("button.comment-submit")

    # Assert
    assert page.text_content("div.comment-text") == "mycomment"

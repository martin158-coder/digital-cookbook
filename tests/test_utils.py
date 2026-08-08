from utils import get_pages, search_name, increment_field


def test_get_pages_exact():
    assert get_pages(20, 5) == 4


def test_get_pages_with_remainder():
    assert get_pages(21, 5) == 5


def test_search_name_found():
    names = [
        {"name": "Martin"},
        {"name": "Ana"}
    ]

    assert search_name("Martin", names) is True


def test_search_name_not_found():
    names = [
        {"name": "Martin"},
        {"name": "Ana"}
    ]

    assert search_name("Pedro", names) is None


def test_increment_upvotes():
    current = [
        {"upvotes": 4},
        {"downvotes": 2}
    ]

    assert increment_field("upvotes", current) == 5
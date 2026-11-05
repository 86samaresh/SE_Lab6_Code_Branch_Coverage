
import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# Existing test cases
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_low_score_is_clean():
    assert classify(1) == "clean"


# Score message tests
def test_spam_words():
    assert score_message("FREE prize", False, 0) == 4


def test_uppercase_word():
    assert score_message("HELLO", False, 0) == 1


def test_link_count_above_three():
    assert score_message("hello", False, 4) == 4


def test_link_count_between_one_and_three():
    assert score_message("hello", False, 2) == 1


def test_known_sender():
    assert score_message("hello", True, 0) == 0


def test_known_sender_negative_score():
    assert score_message("free", True, 0) == 0


# Classification tests
def test_classify_spam():
    assert classify(8) == "spam"


def test_classify_suspicious():
    assert classify(4) == "suspicious"


# Inbox tests
def test_filter_inbox():
    messages = [
        ("FREE winner prize urgent", False, 0),
        ("FREE prize", False, 0),
        ("hello", False, 0)
    ]
    assert filter_inbox(messages) == {
        "spam": 1,
        "suspicious": 1,
        "clean": 1
    }


def test_filter_empty_inbox():
    assert filter_inbox([]) == {
        "spam": 0,
        "suspicious": 0,
        "clean": 0
    }


# Inbox status tests
def test_inbox_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_inbox_flooded():
    assert inbox_status({"spam": 6, "suspicious": 2, "clean": 2}) == "flooded"


def test_inbox_noisy():
    assert inbox_status({"spam": 3, "suspicious": 4, "clean": 3}) == "noisy"


def test_inbox_healthy():
    assert inbox_status({"spam": 1, "suspicious": 3, "clean": 6}) == "healthy"


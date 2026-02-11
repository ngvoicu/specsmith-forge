"""Tests for core/slugify.py."""

from specsmith.core.slugify import slugify


def test_basic():
    assert slugify("User Auth System") == "user-auth-system"


def test_strips_special_chars():
    assert slugify("Fix Upload Bug!") == "fix-upload-bug"


def test_collapses_spaces():
    assert slugify("  lots   of   spaces  ") == "lots-of-spaces"


def test_collapses_hyphens():
    assert slugify("a--b---c") == "a-b-c"


def test_strips_leading_trailing_hyphens():
    assert slugify("-hello-") == "hello"


def test_empty():
    assert slugify("") == ""


def test_unicode_stripped():
    assert slugify("café latte") == "caf-latte"

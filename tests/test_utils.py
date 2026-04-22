"""Tests for utility functions."""

from src.utils import format_currency


def test_format_currency_millions():
    assert format_currency(1250000) == "$1.25M"
    assert format_currency(1000000) == "$1.00M"


def test_format_currency_negative_millions():
    assert format_currency(-1250000) == "-$1.25M"


def test_format_currency_thousands():
    assert format_currency(500000) == "$500.00k"
    assert format_currency(500) == "$0.50k"
    assert format_currency(0) == "$0.00k"


def test_format_currency_negative_thousands():
    assert format_currency(-500000) == "$-500.00k"

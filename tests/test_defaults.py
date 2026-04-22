"""Tests for default configurations."""

from src.defaults import get_singapore_default_inputs


def test_get_singapore_default_inputs():
    defaults = get_singapore_default_inputs()
    assert isinstance(defaults, dict)
    assert defaults["current_age"] == 30
    assert "retire_age" in defaults
    assert "life_expectancy" in defaults
    assert "ra_target" in defaults

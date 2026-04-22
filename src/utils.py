"""Utility functions for the FIRE Calculator.

Commonly used formatting and helper functions.
"""


def format_currency(value: float) -> str:
    """Dynamically formats currency values for display.

    - >= 1M: "$1.25M"
    - < 1M:  "$500k"

    Args:
        value: The numeric currency value to format.

    Returns:
        A string representation of the currency.
    """
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value <= -1_000_000:  # Handle negative millions
        return f"-${abs(value) / 1_000_000:.2f}M"
    else:
        return f"${value / 1_000:.2f}k"

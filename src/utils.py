# src/utils.py


def format_currency(value: float) -> str:
    """
    Dynamically formats currency:
    - >= 1M: "$1.25M"
    - < 1M:  "$500k"
    """
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value <= -1_000_000:  # Handle negative millions
        return f"-${abs(value) / 1_000_000:.2f}M"
    else:
        return f"${value / 1_000:.0f}k"

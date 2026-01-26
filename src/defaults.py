# src/defaults.py


def get_singapore_default_inputs() -> dict:
    """Returns a dictionary of standard values for a typical SG FIRE starter."""
    return {
        # Personal
        "current_age": 30,
        "retire_age": 55,  # Standard "Early" retire at CPF unlock
        "life_expectancy": 85,
        "inflation_rate": 2.5,  # Standard long-term avg
        # Lifestyle
        "spend_bridge": 3000.0,
        "spend_unlock": 3500.0,
        "spend_late": 3500.0,
        # Assets (Moderate Starter)
        "cash_inv": 50000.0,
        "cash_apy": 6.0,
        "cash_topup": 2000.0,
        "oa_bal": 60000.0,
        "oa_inv": 0.0,
        "oa_apy": 4.0,  # Endowus/Amundi low risk
        "oa_topup": 1200.0,
        "sa_bal": 30000.0,
        "sa_inv": 0.0,
        "sa_apy": 4.0,
        "sa_topup": 400.0,
        # Settings
        "ra_target": 205800.0,  # Approx FRS 2024
        "payout_age": 65,
        # Liabilities (HDB Example)
        "house_loan_amt": 300000.0,
        "house_start_age": 30,
        "house_downpayment": 0.0,  # Already paid
        "house_tenure": 25,
        "house_rate": 2.6,
        "car_loan_amt": 0.0,
        "car_start_age": 40,
        "car_downpayment": 0.0,
        "car_tenure": 7,
        "car_rate": 2.78,
    }

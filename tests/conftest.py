import pytest
from src.models import SimulationInputs


@pytest.fixture
def default_inputs():
    """Returns a standard set of inputs updated for the new model structure."""
    return SimulationInputs(
        # Personal
        current_age=30,
        retire_age=40,
        life_expectancy=85,
        inflation_rate=0.025,  # 2.5%
        # Lifestyle (NEW: 3 Phases)
        spend_bridge=3000.0,
        spend_unlock=3500.0,
        spend_late=3500.0,
        # Balances
        sa_bal=50000.0,
        sa_inv=10000.0,
        oa_bal=20000.0,
        oa_inv=50000.0,
        cash_inv=100000.0,
        # Monthly Inflows (Top-ups)
        sa_topup=500.0,
        oa_topup=1000.0,
        cash_topup=2000.0,
        # Growth Rates
        sa_apy=0.04,
        oa_apy=0.06,
        cash_apy=0.08,
        # Settings
        ra_target=200000.0,  # FIXED: Renamed from frs_target
        payout_age=65,  # NEW: Required field
        # Liabilities (Defaults to 0 for clean baseline tests)
        house_loan_amt=0.0,
        house_start_age=35,
        house_downpayment=0.0,
        house_tenure=30,
        house_rate=0.026,
        car_loan_amt=0.0,
        car_start_age=40,
        car_downpayment=0.0,
        car_tenure=5,
        car_rate=0.0278,
    )

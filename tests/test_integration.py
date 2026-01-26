import pytest
from src.models import SimulationInputs
from src.engine import run_simulation

# FIXED: Imported create_liquidity_runway instead of create_lifestyle_chart
from src.plotting import create_nav_chart, create_liquidity_runway


def test_full_simulation_flow():
    # 1. Setup Standard Inputs
    inputs = SimulationInputs(
        current_age=30,
        retire_age=55,
        life_expectancy=85,
        inflation_rate=0.025,
        # Lifestyle
        spend_bridge=3000,
        spend_unlock=3500,
        spend_late=3500,
        # Assets
        sa_bal=30000,
        sa_inv=0,
        oa_bal=60000,
        oa_inv=0,
        cash_inv=50000,
        # Topups
        sa_topup=400,
        oa_topup=1200,
        cash_topup=2000,
        # Rates
        sa_apy=0.04,
        oa_apy=0.025,
        cash_apy=0.06,
        # Settings
        ra_target=200000,
        payout_age=65,
        # Liabilities
        house_loan_amt=300000,
        house_start_age=30,
        house_downpayment=0,
        house_tenure=25,
        house_rate=0.026,
        car_loan_amt=0,
        car_start_age=40,
        car_downpayment=0,
        car_tenure=7,
        car_rate=0.0278,
    )

    # 2. Run Engine
    df = run_simulation(inputs)

    # 3. Assert Data Integrity
    assert not df.empty
    assert "Net_Worth" in df.columns
    assert "Liquid_Cash_Balance" in df.columns
    assert "CPF_Life_Payout_Annual" in df.columns  # Ensure new column exists

    # 4. Smoke Test Plotting Functions (Ensure they don't crash)
    try:
        fig1 = create_nav_chart(df, inputs.retire_age)
        # FIXED: Calling the new function with correct arguments
        fig2 = create_liquidity_runway(df, inputs.retire_age, inputs.payout_age)

        assert fig1 is not None
        assert fig2 is not None
    except Exception as e:
        pytest.fail(f"Plotting generation failed: {e}")

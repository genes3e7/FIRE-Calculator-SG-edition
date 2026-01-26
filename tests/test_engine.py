# tests/test_engine.py
import pytest
from src.engine import run_simulation


def test_simulation_duration(default_inputs):
    """Ensure dataframe has exactly one row per year from current_age to life_expectancy."""
    df = run_simulation(default_inputs)
    expected_years = default_inputs.life_expectancy - default_inputs.current_age + 1
    assert len(df) == expected_years
    assert df.iloc[0]["Age"] == default_inputs.current_age
    assert df.iloc[-1]["Age"] == default_inputs.life_expectancy


def test_accumulation_phase(default_inputs):
    """Test that wealth grows when working (Age 30)."""
    # Run for 1 year only effectively
    default_inputs.life_expectancy = 31
    default_inputs.retire_age = 40  # Still working

    df = run_simulation(default_inputs)

    # Check Cash Growth Calculation for Year 1
    # Formula: (Start + Inflow) * Growth? Or Inflow is monthly.
    # The engine logic:
    # 1. Add Inflows: 100k + (2k * 12) = 124k
    # 2. Grow: 124k * 1.08 = 133,920

    expected_cash = (default_inputs.cash_inv + (default_inputs.cash_topup * 12)) * (
        1 + default_inputs.cash_apy
    )

    # Allow small floating point tolerance
    assert df.iloc[0]["Liquid_Cash_Balance"] == pytest.approx(expected_cash, rel=1e-4)


def test_retirement_stops_inflows(default_inputs):
    """Test that monthly top-ups stop after retirement age."""
    default_inputs.current_age = 60
    default_inputs.retire_age = 60  # Retire immediately
    default_inputs.life_expectancy = 61

    # FIXED: Set spending to 0 so we can isolate the "Inflow Stopping" logic.
    # Otherwise, the engine subtracts living expenses ($3500*12 = 42k), causing the mismatch.
    default_inputs.spend_unlock = 0
    default_inputs.spend_late = 0

    df = run_simulation(default_inputs)

    # Initial Cash: 100k.
    # Should NOT add 24k topup.
    # Should only grow by APY (8%).
    expected_cash = default_inputs.cash_inv * (1 + default_inputs.cash_apy)

    assert df.iloc[0]["Liquid_Cash_Balance"] == pytest.approx(expected_cash, rel=1e-4)


def test_house_loan_deductions(default_inputs):
    """Test that mortgage reduces total OA compared to a no-loan scenario."""
    # Setup common inputs
    default_inputs.house_start_age = 30
    default_inputs.house_downpayment = 0

    # 1. Run Baseline (No Loan)
    default_inputs.house_loan_amt = 0
    df_baseline = run_simulation(default_inputs)
    oa_baseline = df_baseline.iloc[0]["OA_Total"]

    # 2. Run Test Case (Big Loan)
    default_inputs.house_loan_amt = 500000
    df_loan = run_simulation(default_inputs)
    oa_loan = df_loan.iloc[0]["OA_Total"]

    # 3. Assert Loan Scenario is poorer than Baseline
    assert oa_loan < oa_baseline, (
        f"OA with loan ({oa_loan}) should be less than OA without loan ({oa_baseline})"
    )


def test_house_downpayment_cash(default_inputs):
    """Test that cash downpayment hits in the specific purchase year."""
    default_inputs.house_start_age = 32
    default_inputs.house_downpayment = 50000

    df = run_simulation(default_inputs)

    # Age 30, 31: Normal growth
    # Age 32: Massive drop expected

    cash_31 = df[df["Age"] == 31].iloc[0]["Liquid_Cash_Balance"]
    cash_32 = df[df["Age"] == 32].iloc[0]["Liquid_Cash_Balance"]

    # Roughly: Cash_31 + Inflows + Growth - Downpayment
    # If we just check that 32 is significantly lower than expected trend
    assert cash_32 < (cash_31 + 24000)  # It should drop, not grow by inflows


def test_frs_lock_at_55(default_inputs):
    """Test that FRS is created at age 55 and SA/OA are deducted."""
    default_inputs.current_age = 54
    default_inputs.life_expectancy = 56
    default_inputs.ra_target = 100000  # Updated from frs_target
    # Ensure we have enough SA
    default_inputs.sa_bal = 150000

    df = run_simulation(default_inputs)

    row_55 = df[df["Age"] == 55].iloc[0]

    # Check FRS bucket exists
    assert row_55["FRS_RA"] >= 100000

    # Check SA was drained/reduced
    # SA started at 150k. FRS took 100k. SA should be ~50k (plus growth)
    assert row_55["SA_Total"] < 100000  # It should have dropped significantly

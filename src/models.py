# src/models.py
from dataclasses import dataclass


@dataclass
class SimulationInputs:
    # Personal
    current_age: int
    retire_age: int
    life_expectancy: int
    inflation_rate: float

    # Lifestyle Phases
    spend_bridge: float
    spend_unlock: float
    spend_late: float

    # CPF & Investments
    sa_bal: float
    sa_inv: float
    oa_bal: float
    oa_inv: float
    cash_inv: float

    sa_topup: float
    oa_topup: float
    cash_topup: float

    sa_apy: float
    oa_apy: float
    cash_apy: float

    # Retirement Settings (UPDATED)
    ra_target: float  # Renamed from frs_target
    payout_age: int  # New input (65-70)

    # Liabilities
    house_loan_amt: float
    house_start_age: int
    house_downpayment: float
    house_tenure: int
    house_rate: float

    car_loan_amt: float
    car_start_age: int
    car_downpayment: float
    car_tenure: int
    car_rate: float

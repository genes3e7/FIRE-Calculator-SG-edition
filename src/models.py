"""Data models for the FIRE Calculator simulation.

Defines the structure of inputs used throughout the engine and sidebar.
"""

from dataclasses import dataclass


@dataclass
class SimulationInputs:
    """Container for all user-configurable simulation parameters.

    Attributes:
        current_age: User's current age.
        retire_age: Target retirement age.
        life_expectancy: End of simulation age.
        inflation_rate: Annual inflation rate (e.g., 0.03 for 3%).
        spend_bridge: Monthly spending from retirement to age 55.
        spend_unlock: Monthly spending from age 55 to payout age.
        spend_late: Monthly spending from payout age onwards.
        sa_bal: Liquid CPF Special Account balance.
        sa_inv: Invested CPF Special Account balance.
        oa_bal: Liquid CPF Ordinary Account balance.
        oa_inv: Invested CPF Ordinary Account balance.
        cash_inv: Total cash/investment balance outside CPF.
        sa_topup: Monthly contributions to SA.
        oa_topup: Monthly contributions to OA.
        cash_topup: Monthly cash savings/investments.
        sa_apy: Annual percentage yield for invested SA.
        oa_apy: Annual percentage yield for invested OA.
        cash_apy: Annual percentage yield for cash investments.
        ra_target: Retirement Account target amount at age 55.
        payout_age: Age when CPF Life payouts begin.
        house_loan_amt: Total principal of the housing loan.
        house_start_age: Age when the housing loan starts.
        house_downpayment: Initial cash downpayment for the house.
        house_tenure: Duration of the housing loan in years.
        house_rate: Annual interest rate for the housing loan.
        car_loan_amt: Total principal of the car loan.
        car_start_age: Age when the car loan starts.
        car_downpayment: Initial cash downpayment for the car.
        car_tenure: Duration of the car loan in years.
        car_rate: Annual interest rate for the car loan.
    """

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

    # Retirement Settings
    ra_target: float
    payout_age: int

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

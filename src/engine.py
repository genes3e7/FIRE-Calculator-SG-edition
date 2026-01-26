import pandas as pd
import numpy_financial as npf
from src.models import SimulationInputs
from src.constants import SA_BASE_RATE, OA_BASE_RATE


def run_simulation(inputs: SimulationInputs) -> pd.DataFrame:
    ages = list(range(inputs.current_age, inputs.life_expectancy + 1))
    data = []

    # Initialize State
    curr_sa = inputs.sa_bal
    curr_sa_inv = inputs.sa_inv
    curr_oa = inputs.oa_bal
    curr_oa_inv = inputs.oa_inv
    curr_cash = inputs.cash_inv

    frs_locked = False
    frs_balance = 0.0
    cpf_life_annual_payout = 0.0

    # Loan Calculators
    house_pmt = 0
    if inputs.house_loan_amt > 0:
        house_pmt = (
            -npf.pmt(
                inputs.house_rate / 12, inputs.house_tenure * 12, inputs.house_loan_amt
            )
            * 12
        )

    car_pmt = 0
    if inputs.car_loan_amt > 0:
        car_pmt = (
            inputs.car_loan_amt
            + (inputs.car_loan_amt * inputs.car_rate * inputs.car_tenure)
        ) / inputs.car_tenure

    for age in ages:
        is_retired = age >= inputs.retire_age

        # 0. Spending Targets
        if age < 55:
            target_spend_today = inputs.spend_bridge
        elif age < inputs.payout_age:
            target_spend_today = inputs.spend_unlock
        else:
            target_spend_today = inputs.spend_late

        deflator = (1 + inputs.inflation_rate) ** (age - inputs.current_age)
        annual_spend_nominal = target_spend_today * 12 * deflator

        # 1. Inflows
        if not is_retired:
            curr_sa_inv += inputs.sa_topup * 12
            curr_oa_inv += inputs.oa_topup * 12
            curr_cash += inputs.cash_topup * 12

        # 2. Growth
        curr_sa_inv *= 1 + inputs.sa_apy
        curr_oa_inv *= 1 + inputs.oa_apy
        curr_cash *= 1 + inputs.cash_apy
        curr_sa *= 1 + SA_BASE_RATE
        curr_oa *= 1 + OA_BASE_RATE

        # 3. Withdrawals
        if is_retired:
            spend_needed = annual_spend_nominal

            # Payout Offset
            if age >= inputs.payout_age:
                spend_needed -= cpf_life_annual_payout
                if spend_needed < 0:
                    spend_needed = 0

            # Deduct Cash
            if curr_cash >= spend_needed:
                curr_cash -= spend_needed
                spend_needed = 0
            else:
                spend_needed -= curr_cash
                curr_cash = 0

            # Deduct CPF Surplus
            if age >= 55 and spend_needed > 0:
                total_oa = curr_oa + curr_oa_inv
                if total_oa >= spend_needed:
                    if curr_oa >= spend_needed:
                        curr_oa -= spend_needed
                    else:
                        needed = spend_needed - curr_oa
                        curr_oa = 0
                        curr_oa_inv -= needed
                    spend_needed = 0
                else:
                    spend_needed -= total_oa
                    curr_oa = 0
                    curr_oa_inv = 0

                    total_sa = curr_sa + curr_sa_inv
                    if total_sa >= spend_needed:
                        if curr_sa >= spend_needed:
                            curr_sa -= spend_needed
                        else:
                            needed = spend_needed - curr_sa
                            curr_sa = 0
                            curr_sa_inv -= needed
                        spend_needed = 0
                    else:
                        curr_sa = 0
                        curr_sa_inv = 0

        # 4. Liabilities
        if age == inputs.house_start_age:
            curr_cash -= inputs.house_downpayment
        if (
            inputs.house_start_age
            <= age
            < (inputs.house_start_age + inputs.house_tenure)
        ):
            if curr_oa >= house_pmt:
                curr_oa -= house_pmt
            elif (curr_oa + curr_oa_inv) >= house_pmt:
                needed = house_pmt - curr_oa
                curr_oa = 0
                curr_oa_inv -= needed
            else:
                remaining = house_pmt - curr_oa - curr_oa_inv
                curr_oa = 0
                curr_oa_inv = 0
                curr_cash -= remaining

        if age == inputs.car_start_age:
            curr_cash -= inputs.car_downpayment
        if inputs.car_start_age <= age < (inputs.car_start_age + inputs.car_tenure):
            curr_cash -= car_pmt

        # 5. RA Logic
        if age == 55 and not frs_locked:
            needed = inputs.ra_target
            if curr_sa >= needed:
                curr_sa -= needed
                frs_balance = needed
                needed = 0
            else:
                frs_balance += curr_sa
                needed -= curr_sa
                curr_sa = 0
            if needed > 0:
                if curr_oa >= needed:
                    curr_oa -= needed
                    frs_balance += needed
                    needed = 0
                else:
                    frs_balance += curr_oa
                    needed -= curr_oa
                    curr_oa = 0
            frs_locked = True

        if frs_locked and age < inputs.payout_age:
            frs_balance *= 1.04

        if age == inputs.payout_age and frs_balance > 0:
            deferral_bonus = 1.0 + ((age - 65) * 0.07)
            base_payout_rate = 0.075
            cpf_life_annual_payout = frs_balance * base_payout_rate * deferral_bonus
            frs_balance = 0.0

        data.append(
            {
                "Age": age,
                "Liquid_Cash_Balance": max(0, curr_cash),
                "OA_Total": curr_oa + curr_oa_inv,
                "SA_Total": curr_sa + curr_sa_inv,
                "FRS_RA": frs_balance,
                "Net_Worth": max(0, curr_cash)
                + curr_oa
                + curr_oa_inv
                + curr_sa
                + curr_sa_inv
                + frs_balance,
                "Phase_Target": target_spend_today,
                "CPF_Life_Payout_Annual": cpf_life_annual_payout,  # Exported for UI
            }
        )

    return pd.DataFrame(data)

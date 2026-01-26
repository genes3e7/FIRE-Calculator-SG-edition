# src/engine.py
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

        # 3. AUTOMATIC OPTIMAL WITHDRAWALS (Legal & Optimal)
        if is_retired:
            spend_needed = annual_spend_nominal

            # Offset by CPF Life payout if applicable
            if age >= inputs.payout_age:
                spend_needed = max(0, spend_needed - cpf_life_annual_payout)

            if spend_needed > 0:
                # FIXED: Cash is the ONLY source allowed before 55
                sources = [["cash", curr_cash, inputs.cash_apy]]

                # After 55, CPF surplus becomes spendable cash
                if age >= 55:
                    sources.append(["oa_liq", curr_oa, OA_BASE_RATE])
                    sources.append(["oa_inv", curr_oa_inv, inputs.oa_apy])
                    sources.append(["sa_liq", curr_sa, SA_BASE_RATE])
                    sources.append(["sa_inv", curr_sa_inv, inputs.sa_apy])

                # SORT: Lowest yield first (Mathematically Optimal)
                sources.sort(key=lambda x: x[2])

                for source in sources:
                    if spend_needed <= 0:
                        break
                    
                    acc_id, bal, apy = source
                    take = min(bal, spend_needed)
                    
                    if acc_id == "cash": curr_cash -= take
                    elif acc_id == "oa_inv": curr_oa_inv -= take
                    elif acc_id == "oa_liq": curr_oa -= take
                    elif acc_id == "sa_liq": curr_sa -= take
                    elif acc_id == "sa_inv": curr_sa_inv -= take
                    
                    spend_needed -= take

        # 4. Liabilities (CPF Usage is allowed for Housing before 55)
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

        # 5. RA Logic: Transfer at 55
        if age == 55 and not frs_locked:
            needed = inputs.ra_target
            for acc in ["sa_liq", "sa_inv", "oa_liq", "oa_inv"]:
                if needed <= 0: break
                
                if acc == "sa_liq":
                    take = min(curr_sa, needed); curr_sa -= take
                elif acc == "sa_inv":
                    take = min(curr_sa_inv, needed); curr_sa_inv -= take
                elif acc == "oa_liq":
                    take = min(curr_oa, needed); curr_oa -= take
                elif acc == "oa_inv":
                    take = min(curr_oa_inv, needed); curr_oa_inv -= take
                
                frs_balance += take
                needed -= take
            frs_locked = True

        if frs_locked and age < inputs.payout_age:
            frs_balance *= 1.04

        if age == inputs.payout_age and frs_balance > 0:
            deferral_bonus = 1.0 + ((age - 65) * 0.07)
            base_payout_rate = 0.075
            cpf_life_annual_payout = frs_balance * base_payout_rate * deferral_bonus
            frs_balance = 0.0

        data.append({
            "Age": age,
            "Liquid_Cash_Balance": max(0, curr_cash),
            "OA_Total": curr_oa + curr_oa_inv,
            "SA_Total": curr_sa + curr_sa_inv,
            "FRS_RA": frs_balance,
            "Net_Worth": max(0, curr_cash) + curr_oa + curr_oa_inv + curr_sa + curr_sa_inv + frs_balance,
            "Phase_Target": target_spend_today,
            "CPF_Life_Payout_Annual": cpf_life_annual_payout,
        })

    return pd.DataFrame(data)

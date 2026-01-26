import streamlit as st
import json
from src.models import SimulationInputs
from src.defaults import get_singapore_default_inputs


def render_sidebar() -> SimulationInputs:
    # --- HELPER: Initialize Session State ---
    if "current_age" not in st.session_state:
        defaults = get_singapore_default_inputs()
        for key, value in defaults.items():
            st.session_state[key] = value

    with st.sidebar:
        st.title("⚙️ Controls")

        # --- SECTION 0: DATA MANAGER ---
        with st.expander("📂 Import / Export / Defaults", expanded=False):
            if st.button("Reset to Typical SG Stats"):
                defaults = get_singapore_default_inputs()
                for key, value in defaults.items():
                    st.session_state[key] = value
                st.rerun()

            current_config = {
                k: st.session_state[k]
                for k in get_singapore_default_inputs().keys()
                if k in st.session_state
            }
            json_string = json.dumps(current_config, indent=2)
            st.download_button(
                "Download Settings (JSON)",
                json_string,
                "fire_config.json",
                "application/json",
            )

            uploaded_file = st.file_uploader("Upload Config", type=["json"])
            if uploaded_file is not None:
                try:
                    data = json.load(uploaded_file)
                    for key, value in data.items():
                        st.session_state[key] = value
                    st.success("Loaded!")
                    if st.button("Apply Loaded Settings"):
                        st.rerun()
                except Exception as e:
                    st.error(f"Error loading file: {e}")

        # --- SECTION 1: PERSONAL ---
        st.header("1. Personal Details")
        c1, c2 = st.columns(2)
        c1.number_input("Current Age", 20, 80, key="current_age")
        c2.number_input("Retire Age", 30, 80, key="retire_age")

        c3, c4 = st.columns(2)
        c3.number_input("Life Expectancy", 70, 110, key="life_expectancy")
        c4.number_input("Inflation (%)", 0.0, 15.0, step=0.1, key="inflation_rate")

        # --- SECTION 2: LIFESTYLE ---
        st.header("2. Lifestyle ($ Today)")
        st.number_input(
            "Bridge Spend (Retire-55)", 0, 50000, step=100, key="spend_bridge"
        )
        st.number_input(
            "Unlock Spend (55-Payout)", 0, 50000, step=100, key="spend_unlock"
        )
        st.number_input("Late Spend (Payout+)", 0, 50000, step=100, key="spend_late")

        # --- SECTION 3: CPF SETTINGS ---
        st.header("3. CPF Settings")
        st.number_input("Target RA Amount @ 55", 0, 1000000, step=1000, key="ra_target")
        st.slider("Payout Start Age", 65, 70, key="payout_age")

        # --- SECTION 4: ASSETS (EXPLICIT SPLIT) ---
        st.header("4. Assets Breakdown")

        # CASH
        st.subheader("💵 Cash")
        c_bal, c_apy = st.columns([2, 1])
        c_bal.number_input("Total Cash Balance", 0, 10000000, step=1000, key="cash_inv")
        c_apy.number_input("APY %", 0.0, 20.0, step=0.1, key="cash_apy")
        st.number_input("Monthly Cash Top-up", 0, 50000, key="cash_topup")

        # CPF OA
        st.subheader("🏠 CPF OA")
        st.caption("Liquid earns 2.5%. Invested earns custom rate.")

        o_liq, o_inv = st.columns(2)
        o_liq.number_input("Liquid OA (2.5%)", 0, 5000000, step=1000, key="oa_bal")
        o_inv.number_input("Invested OA", 0, 5000000, step=1000, key="oa_inv")

        o_apy_col, o_top_col = st.columns([1, 2])
        o_apy_col.number_input("Inv APY %", 0.0, 20.0, step=0.1, key="oa_apy")
        o_top_col.number_input("Monthly OA Top-up", 0, 50000, key="oa_topup")

        # CPF SA
        st.subheader("🛡️ CPF SA")
        st.caption("Liquid earns 4.0%. Invested earns custom rate.")

        s_liq, s_inv = st.columns(2)
        s_liq.number_input("Liquid SA (4.0%)", 0, 5000000, step=1000, key="sa_bal")
        s_inv.number_input("Invested SA", 0, 5000000, step=1000, key="sa_inv")

        s_apy_col, s_top_col = st.columns([1, 2])
        s_apy_col.number_input("Inv APY %", 0.0, 20.0, step=0.1, key="sa_apy")
        s_top_col.number_input("Monthly SA Top-up", 0, 50000, key="sa_topup")

        # --- SECTION 5: LIABILITIES ---
        st.header("5. Liabilities")

        # HOUSE LOAN
        st.markdown("**House Loan**")
        st.number_input(
            "Remaining Amount",
            0,
            5000000,
            key="house_loan_amt",
            label_visibility="collapsed",
        )

        if st.session_state.house_loan_amt > 0:
            h1, h2, h3 = st.columns(3)
            h1.number_input("Start Age", 20, 70, key="house_start_age")
            h2.number_input("Tenure", 1, 40, key="house_tenure")
            h3.number_input("Rate %", 0.0, 10.0, step=0.1, key="house_rate")
            # RESTORED: Downpayment Field
            st.number_input("Downpayment (Cash)", 0, 1000000, key="house_downpayment")

        st.markdown("---")

        # CAR LOAN
        st.markdown("**Car Loan**")
        st.number_input(
            "Remaining Amount",
            0,
            500000,
            key="car_loan_amt",
            label_visibility="collapsed",
        )

        if st.session_state.car_loan_amt > 0:
            c1, c2, c3 = st.columns(3)
            c1.number_input("Start Age", 20, 70, key="car_start_age")
            c2.number_input("Tenure", 1, 10, key="car_tenure")
            c3.number_input("Rate %", 0.0, 10.0, step=0.1, key="car_rate")
            # RESTORED: Downpayment Field
            st.number_input("Downpayment (Cash)", 0, 200000, key="car_downpayment")

    # Pack into Object
    return SimulationInputs(
        current_age=st.session_state.current_age,
        retire_age=st.session_state.retire_age,
        life_expectancy=st.session_state.life_expectancy,
        inflation_rate=st.session_state.inflation_rate / 100.0,
        spend_bridge=st.session_state.spend_bridge,
        spend_unlock=st.session_state.spend_unlock,
        spend_late=st.session_state.spend_late,
        sa_bal=st.session_state.sa_bal,
        sa_inv=st.session_state.sa_inv,
        oa_bal=st.session_state.oa_bal,
        oa_inv=st.session_state.oa_inv,
        cash_inv=st.session_state.cash_inv,
        sa_topup=st.session_state.sa_topup,
        oa_topup=st.session_state.oa_topup,
        cash_topup=st.session_state.cash_topup,
        sa_apy=st.session_state.sa_apy / 100.0,
        oa_apy=st.session_state.oa_apy / 100.0,
        cash_apy=st.session_state.cash_apy / 100.0,
        ra_target=st.session_state.ra_target,
        payout_age=st.session_state.payout_age,
        house_loan_amt=st.session_state.house_loan_amt,
        house_start_age=st.session_state.house_start_age,
        house_downpayment=st.session_state.get("house_downpayment", 0),
        house_tenure=st.session_state.get("house_tenure", 25),
        house_rate=st.session_state.get("house_rate", 2.6) / 100.0,
        car_loan_amt=st.session_state.car_loan_amt,
        car_start_age=st.session_state.get("car_start_age", 30),
        car_downpayment=st.session_state.get("car_downpayment", 0),
        car_tenure=st.session_state.get("car_tenure", 7),
        car_rate=st.session_state.get("car_rate", 2.78) / 100.0,
    )

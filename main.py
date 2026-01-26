import streamlit as st
from src.sidebar import render_sidebar
from src.engine import run_simulation
from src.plotting import create_nav_chart, create_liquidity_runway
from src.utils import format_currency


def main():
    st.set_page_config(page_title="FIRE Master Calculator", layout="wide")
    st.title("🔥 Modular FIRE Calculator")

    inputs = render_sidebar()
    df_results = run_simulation(inputs)

    # --- FEATURE: CONFIGURATION SNAPSHOT ---
    with st.expander(
        "📝 View Configuration (Click to Expand for Screenshot)", expanded=False
    ):
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown("### 👤 Personal")
            st.write(f"**Age:** {inputs.current_age} → {inputs.retire_age}")
            st.write(f"**Life Expectancy:** {inputs.life_expectancy}")
            st.write(f"**Inflation:** {inputs.inflation_rate * 100:.1f}%")

        with c2:
            st.markdown("### 💰 Assets & Growth")
            st.write(
                f"**Cash:** {format_currency(inputs.cash_inv)} (@ {inputs.cash_apy * 100:.1f}%)"
            )
            st.write(
                f"**OA:** {format_currency(inputs.oa_bal + inputs.oa_inv)} (@ {inputs.oa_apy * 100:.1f}%)"
            )
            st.write(
                f"**SA:** {format_currency(inputs.sa_bal + inputs.sa_inv)} (@ {inputs.sa_apy * 100:.1f}%)"
            )

        with c3:
            st.markdown("### 💸 Lifestyle ($ Today)")
            st.write(f"**Bridge:** {format_currency(inputs.spend_bridge)}/m")
            st.write(f"**Unlock:** {format_currency(inputs.spend_unlock)}/m")
            st.write(f"**Late:** {format_currency(inputs.spend_late)}/m")

            # CPF LIFE DISPLAY
            payout_row = df_results[df_results["Age"] == inputs.payout_age]
            if not payout_row.empty:
                annual_payout = payout_row.iloc[0]["CPF_Life_Payout_Annual"]
                monthly_payout = annual_payout / 12
                st.write(f"**CPF Life:** {format_currency(monthly_payout)}/m")
                st.caption(f"*(Nominal starting value at Age {inputs.payout_age})*")

        with c4:
            st.markdown("### 🏠 Liabilities & Rates")

            # House Display
            house_str = f"**House:** {format_currency(inputs.house_loan_amt)} (@ {inputs.house_rate * 100:.1f}%)"
            st.write(house_str)
            if inputs.house_downpayment > 0:
                st.caption(
                    f"↳ Downpayment: {format_currency(inputs.house_downpayment)}"
                )

            # Car Display
            car_str = f"**Car:** {format_currency(inputs.car_loan_amt)} (@ {inputs.car_rate * 100:.1f}%)"
            st.write(car_str)
            if inputs.car_downpayment > 0:
                st.caption(f"↳ Downpayment: {format_currency(inputs.car_downpayment)}")

            st.write(f"**RA Target:** {format_currency(inputs.ra_target)}")
            st.write(f"**Payout Age:** {inputs.payout_age}")

    # --- MAIN DASHBOARD ---
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("📊 Net Worth Projection")
        # FIXED: Replaced use_container_width=True with width="stretch"
        st.plotly_chart(
            create_nav_chart(df_results, inputs.retire_age), width="stretch"
        )

        st.subheader("🛣️ Liquidity Runway (The 3 Phases)")
        st.caption(
            "This chart shows exactly how much money is 'unlocked' and available to spend in each phase."
        )
        # FIXED: Replaced use_container_width=True with width="stretch"
        st.plotly_chart(
            create_liquidity_runway(df_results, inputs.retire_age, inputs.payout_age),
            width="stretch",
        )

    with col2:
        st.subheader("🔎 Key Stats")

        def get_row(age):
            row = df_results[df_results["Age"] == age]
            return row.iloc[0] if not row.empty else None

        retire_row = get_row(inputs.retire_age)
        if retire_row is not None:
            st.metric("Net Worth @ Retire", format_currency(retire_row["Net_Worth"]))
            st.metric(
                "Bridge Cash Start", format_currency(retire_row["Liquid_Cash_Balance"])
            )

        age55_row = get_row(55)
        if age55_row is not None:
            # Check if Bridge Failed (Cash at 54 should be > 0)
            row_54 = get_row(54)
            bridge_safe = (
                row_54["Liquid_Cash_Balance"] > 0 if row_54 is not None else False
            )

            cash_left = row_54["Liquid_Cash_Balance"]

            st.metric(
                "Bridge Outcome (Age 55)",
                "SAFE" if bridge_safe else "FAILED",
                delta=f"Cash Left: {format_currency(cash_left)}",
                delta_color="normal" if bridge_safe else "inverse",
            )

            surplus = age55_row["OA_Total"] + age55_row["SA_Total"]
            st.metric("CPF Surplus Unlocked", format_currency(surplus))


if __name__ == "__main__":
    main()

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_nav_chart(df: pd.DataFrame, retire_age: int):
    # Standard Net Worth Chart
    fig = px.area(
        df,
        x="Age",
        y=["Liquid_Cash_Balance", "OA_Total", "SA_Total", "FRS_RA"],
        labels={"value": "Amount ($)", "variable": "Asset Class"},
        color_discrete_map={
            "Liquid_Cash_Balance": "#00CC96",  # Green
            "OA_Total": "#636EFA",  # Blue
            "SA_Total": "#EF553B",  # Red
            "FRS_RA": "#AB63FA",  # Purple
        },
    )

    # Vertical Lines
    fig.add_vline(
        x=retire_age, line_dash="dash", line_color="white", annotation_text="Retirement"
    )
    fig.add_vline(x=55, line_dash="dot", line_color="white", annotation_text="Age 55")

    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_liquidity_runway(df: pd.DataFrame, retire_age: int, payout_age: int = 65):
    # 1. Prepare Data
    plot_df = df[df["Age"] >= retire_age].copy()

    plot_df["Accessible_Funds"] = plot_df.apply(
        lambda row: row["Liquid_Cash_Balance"]
        if row["Age"] < 55
        else (row["Liquid_Cash_Balance"] + row["OA_Total"] + row["SA_Total"]),
        axis=1,
    )

    fig = go.Figure()

    # 2. Plot the Liquidity Line
    fig.add_trace(
        go.Scatter(
            x=plot_df["Age"],
            y=plot_df["Accessible_Funds"],
            mode="lines",
            name="Accessible Funds",
            line=dict(color="#00CC96", width=4),
            fill="tozeroy",
            fillcolor="rgba(0, 204, 150, 0.1)",
        )
    )

    # 3. Add Phase Background Zones (No overlapping text)

    # Phase 1: Bridge (Retire -> 55)
    fig.add_vrect(
        x0=retire_age, x1=55, fillcolor="Red", opacity=0.05, layer="below", line_width=0
    )

    # Phase 2: Unlock (55 -> Payout Age)
    fig.add_vrect(
        x0=55,
        x1=payout_age,
        fillcolor="Yellow",
        opacity=0.1,
        layer="below",
        line_width=0,
    )

    # Phase 3: Late (Payout Age+)
    fig.add_vrect(
        x0=payout_age,
        x1=plot_df["Age"].max(),
        fillcolor="Green",
        opacity=0.05,
        layer="below",
        line_width=0,
    )

    # 4. Add Clean Labels Above Chart
    # We calculate the mid-point of each phase to center the text

    # Phase 1 Label
    p1_center = retire_age + (55 - retire_age) / 2
    fig.add_annotation(
        x=p1_center,
        y=1.08,
        xref="x",
        yref="paper",
        text="<b>PHASE 1: BRIDGE</b>",
        showarrow=False,
        font=dict(size=12, color="#D32F2F"),
    )

    # Phase 2 Label
    p2_center = 55 + (payout_age - 55) / 2
    fig.add_annotation(
        x=p2_center,
        y=1.08,
        xref="x",
        yref="paper",
        text="<b>PHASE 2: UNLOCK</b>",
        showarrow=False,
        font=dict(size=12, color="#FBC02D"),
    )

    # Phase 3 Label
    p3_center = payout_age + (plot_df["Age"].max() - payout_age) / 2
    fig.add_annotation(
        x=p3_center,
        y=1.08,
        xref="x",
        yref="paper",
        text="<b>PHASE 3: CPF LIFE</b>",
        showarrow=False,
        font=dict(size=12, color="#388E3C"),
    )

    fig.update_layout(
        title="<b>Total Accessible Liquidity</b> (Spending Power)",
        xaxis_title="Age",
        yaxis_title="Accessible Amount ($)",
        hovermode="x unified",
        showlegend=False,
        margin=dict(t=50),  # Add top margin for labels
    )

    return fig

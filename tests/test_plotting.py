"""Tests for plotting functions."""

import plotly.graph_objects as go

from src.engine import run_simulation
from src.plotting import create_liquidity_runway, create_nav_chart


def test_create_nav_chart(default_inputs):
    df = run_simulation(default_inputs)
    fig = create_nav_chart(df, default_inputs.retire_age)
    assert isinstance(fig, go.Figure)


def test_create_liquidity_runway(default_inputs):
    df = run_simulation(default_inputs)
    fig = create_liquidity_runway(
        df, default_inputs.retire_age, default_inputs.payout_age
    )
    assert isinstance(fig, go.Figure)

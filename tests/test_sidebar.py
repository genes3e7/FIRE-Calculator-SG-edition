"""Tests for the sidebar component."""

from unittest.mock import MagicMock, patch

import pytest

from src.sidebar import render_sidebar


@pytest.fixture
def mock_streamlit():
    """Mocks streamlit components and session state."""
    with (
        patch("src.sidebar.st") as mock_st,
    ):
        # Setup session state mock
        # Mocking an object that behaves like session_state
        class SessionState(dict):
            def __getattr__(self, name):
                return self.get(name)

        mock_st.session_state = SessionState(
            {
                "current_age": 30,
                "retire_age": 55,
                "life_expectancy": 85,
                "inflation_rate": 2.5,
                "spend_bridge": 3000,
                "spend_unlock": 3500,
                "spend_late": 3500,
                "ra_target": 200000,
                "payout_age": 65,
                "cash_inv": 50000,
                "cash_apy": 6.0,
                "cash_topup": 2000,
                "oa_bal": 60000,
                "oa_inv": 0,
                "oa_apy": 4.0,
                "oa_topup": 1200,
                "sa_bal": 30000,
                "sa_inv": 0,
                "sa_apy": 4.0,
                "sa_topup": 400,
                "house_loan_amt": 300000,
                "house_start_age": 30,
                "house_downpayment": 0,
                "house_tenure": 25,
                "house_rate": 2.6,
                "car_loan_amt": 0,
                "car_start_age": 40,
                "car_downpayment": 0,
                "car_tenure": 7,
                "car_rate": 2.78,
            }
        )

        # Mock st.columns to return the right number of mocks
        def mock_columns(spec):
            num = spec if isinstance(spec, int) else len(spec)
            return [MagicMock() for _ in range(num)]

        mock_st.columns.side_effect = mock_columns

        # Mock st.sidebar context manager
        mock_st.sidebar = MagicMock()
        mock_st.sidebar.__enter__.return_value = MagicMock()

        yield mock_st


def test_render_sidebar_basic(mock_streamlit):
    """Test that render_sidebar returns SimulationInputs with correct values."""
    inputs = render_sidebar()

    assert inputs.current_age == 30
    assert inputs.retire_age == 55
    assert inputs.inflation_rate == pytest.approx(0.025)
    assert inputs.cash_inv == 50000
    assert inputs.cash_apy == pytest.approx(0.06)
    assert inputs.house_loan_amt == 300000
    assert inputs.house_rate == pytest.approx(0.026)

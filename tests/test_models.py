# tests/test_models.py


def test_simulation_inputs_initialization(default_inputs):
    """Test that the data class initializes with correct types."""
    assert isinstance(default_inputs.current_age, int)
    assert isinstance(default_inputs.cash_inv, float)
    assert default_inputs.retire_age == 40

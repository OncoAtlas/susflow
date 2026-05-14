import pytest
from susflow.core import validator

def test_validate_invalid_uf():
    """Should raise an error for an unknown UF."""
    with pytest.raises(ValueError, match="inválida"):
        validator.validate_params("SIM", "ZZ", 2023)

def test_validate_future_year():
    with pytest.raises(ValueError, match="ainda não está disponível"): # Adjusted here
        validator.validate_params("SIM", "PB", 2099)

def test_validate_sim_monthly_error():
    """Annual systems should ignore the month or warn (depending on the implementation)."""
    # If we configured normalization, we test the return value
    uf, year, month = validator.validate_params("SIM", "PB", 2023, month=5)
    assert month == 0  # Should have normalized to annual
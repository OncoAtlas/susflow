import pytest
from susflow.core import validator

def test_validate_invalid_uf():
    """Deve levantar erro para UF inexistente."""
    with pytest.raises(ValueError, match="inválida"):
        validator.validate_params("SIM", "ZZ", 2023)

def test_validate_future_year():
    with pytest.raises(ValueError, match="ainda não está disponível"): # Ajustado aqui
        validator.validate_params("SIM", "PB", 2099)

def test_validate_sim_monthly_error():
    """Sistemas anuais devem ignorar mês ou avisar (dependendo da implementação)."""
    # Se configuramos para normalizar, testamos o retorno
    uf, year, month = validator.validate_params("SIM", "PB", 2023, month=5)
    assert month == 0  # Deve ter normalizado para anual
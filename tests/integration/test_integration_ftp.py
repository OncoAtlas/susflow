import os
import pytest

from susflow import ftp as _ftp


RUN_INTEGRATION = os.getenv("RUN_INTEGRATION", "false").lower() == "true"


@pytest.mark.skipif(not RUN_INTEGRATION, reason="Integration tests disabled by default")
def test_listar_real_ftp():
    # This test will run only when RUN_INTEGRATION=true in the environment
    files = _ftp.listar("/")
    assert isinstance(files, list)

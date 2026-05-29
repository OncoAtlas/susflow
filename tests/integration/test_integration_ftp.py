import os

import pytest

from susflow import ftp as _ftp

RUN_INTEGRATION = os.getenv("RUN_INTEGRATION", "false").lower() == "true"


@pytest.mark.skipif(not RUN_INTEGRATION, reason="Integration tests disabled by default")
def test_list_files_real_ftp():
    files = _ftp.list_files("/")
    assert isinstance(files, list)

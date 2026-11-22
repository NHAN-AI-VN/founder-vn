from pathlib import Path

import pytest


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """A temporary project root; the path-locked layer works under <root>/founder/."""
    return tmp_path

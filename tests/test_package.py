import importlib.metadata

import founder_vn


def test_package_has_single_source_version() -> None:
    assert importlib.metadata.version("founder-vn") == founder_vn.__version__

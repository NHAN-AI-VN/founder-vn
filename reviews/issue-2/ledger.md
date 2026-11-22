# Review closure ledger — #2 scaffold, CLI/MCP parity, release path

S1 FIXED — witnessed red by mutation (`DID NOT RAISE RuntimeError` for the network guard, `DID NOT RAISE AssertionError` for the golden runner), restored green (7 passed), blind spots and licenses recorded in the evidence file; commit 0a4a1ab.
S2 FIXED — `project_version` in `scripts/skill_lint.py` now reads `[tool.hatch.version].path` when the version is dynamic; `tests/test_skill_lint.py` red before (`assert 0 == 1`), green after (34 passed); commit 5de51b0.
S3 FIXED — `tests/test_package.py` compares `importlib.metadata.version("founder-vn")` with `founder_vn.__version__`; the literal `"0.1.0"` asserts are gone from both tests; red under a mutated `__version__` (`'0.1.0' == '0.1.1'`); commit 0e7f0f5.

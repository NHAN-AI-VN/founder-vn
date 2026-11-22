"""The release workflow publishes by trusted publishing only, and only for v<__version__>."""

import re
from pathlib import Path

import pytest

WORKFLOW = "release.yml"


@pytest.fixture
def workflow(project_root: Path) -> str:
    path = Path(__file__).parent.parent / ".github" / "workflows" / WORKFLOW
    return path.read_text(encoding="utf-8")


def test_release_triggers_on_version_tag_push(workflow: str) -> None:
    assert re.search(r"tags:\s*\[\s*['\"]v\*['\"]\s*\]", workflow)


def test_release_uses_oidc_trusted_publishing_without_a_token(workflow: str) -> None:
    assert "id-token: write" in workflow
    assert "pypa/gh-action-pypi-publish" in workflow
    assert "environment: pypi" in workflow
    assert not re.search(r"password|PYPI_API_TOKEN|secrets\.", workflow, re.IGNORECASE)


def test_release_builds_with_uv_and_checks_tag_against_version(workflow: str) -> None:
    assert "uv build" in workflow
    assert "GITHUB_REF_NAME" in workflow
    assert 'v${version}"' in workflow or "v$version" in workflow

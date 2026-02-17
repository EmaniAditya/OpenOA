from pathlib import Path
import re

from fastapi.testclient import TestClient

from deploy.app.main import app

client = TestClient(app)
OPENOA_INIT = Path(__file__).resolve().parents[2] / "openoa" / "__init__.py"
VERSION_REGEX = re.compile(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", re.MULTILINE)


def expected_openoa_version() -> str:
    content = OPENOA_INIT.read_text(encoding="utf-8")
    match = VERSION_REGEX.search(content)
    assert match is not None
    return match.group(1)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "openoa-interview"
    assert "timestamp" in payload


def test_version() -> None:
    response = client.get("/api/version")
    assert response.status_code == 200
    payload = response.json()
    assert payload["package"] == "openoa"
    assert payload["version"] == expected_openoa_version()


def test_methods() -> None:
    response = client.get("/api/methods")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["methods"], list)
    assert "MonteCarloAEP" in payload["methods"]


def test_frontend_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

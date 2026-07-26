"""Optional HTTP adapter over api.v1 (EP-003)."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest

from boardcomposer.api.http import create_app

SAMPLES = Path("data/samples")
CSV = SAMPLES / "batch_inbox" / "basic_boards.csv"


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.delenv("BOARDCOMPOSER_API_KEY", raising=False)
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["auth_required"] is False
    assert "api_version" in payload


def test_openapi(client):
    response = client.get("/v1/openapi.json")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["openapi"].startswith("3.")
    assert "/v1/run" in payload["paths"]


def test_run_json_export(client):
    data = {
        "strategy": "balanced",
        "top": "1",
        "format": "json",
    }
    with CSV.open("rb") as handle:
        response = client.post(
            "/v1/run",
            data={**data, "file": (handle, "basic_boards.csv")},
            content_type="multipart/form-data",
        )
    assert response.status_code == 200
    assert response.is_json
    payload = response.get_json()
    assert "placements" in payload
    assert payload["complete"] is True


def test_run_requires_api_key_when_configured(monkeypatch):
    monkeypatch.setenv("BOARDCOMPOSER_API_KEY", "secret-token")
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        denied = client.get("/health")
        assert denied.status_code == 200

        with CSV.open("rb") as handle:
            unauthorized = client.post(
                "/v1/run",
                data={"file": (handle, "basic_boards.csv")},
                content_type="multipart/form-data",
            )
        assert unauthorized.status_code == 401

        with CSV.open("rb") as handle:
            ok = client.post(
                "/v1/run",
                data={"file": (handle, "basic_boards.csv"), "format": "json"},
                content_type="multipart/form-data",
                headers={"X-API-Key": "secret-token"},
            )
        assert ok.status_code == 200


def test_run_rejects_bad_extension(client):
    response = client.post(
        "/v1/run",
        data={"file": (BytesIO(b"nope"), "notes.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "unsupported_type"


def test_http_cli_help():
    from boardcomposer.http_cli import main

    assert main(["--help"]) == 0

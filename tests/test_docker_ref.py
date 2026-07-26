"""Reference HTTP container assets (EP-003 SPR-003)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dockerfile_is_http_only_reference():
    text = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "python:3.13-slim" in text
    assert "boardcomposer.http_cli" in text
    assert "pip install" in text and "flask" in text.lower()
    assert (
        "pip install" in text
        and "pyside6" not in text.split("pip install", 1)[1].lower()
    )
    assert "USER app" in text
    assert "HEALTHCHECK" in text


def test_compose_and_threat_doc_exist():
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    assert "boardcomposer-http" in compose
    assert "BOARDCOMPOSER_API_KEY" in compose

    doc = (ROOT / "docs/masterplan/DOC-010-HTTP-Amenazas.md").read_text(
        encoding="utf-8"
    )
    assert "EP-003" in doc
    assert "BOARDCOMPOSER_API_KEY" in doc
    assert "USER app" in doc


def test_serve_docker_script_executable():
    script = ROOT / "scripts/serve_docker.sh"
    assert script.is_file()
    assert script.stat().st_mode & 0o111

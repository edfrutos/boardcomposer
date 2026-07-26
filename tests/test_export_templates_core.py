"""Core headless reader for Studio export templates (EP-002 SPR-002)."""

from __future__ import annotations

from pathlib import Path

from boardcomposer.io.export_templates import (
    find_export_template,
    load_export_templates,
    parse_export_templates_payload,
)

SAMPLES = Path("data/samples/export_templates.json")


def test_load_sample_export_templates():
    templates = load_export_templates(SAMPLES)
    assert len(templates) >= 2
    names = {(t.client, t.name) for t in templates}
    assert ("", "JSON completo") in names
    assert ("Demo", "SVG sin retales") in names


def test_find_export_template_by_client():
    general = find_export_template("JSON completo", path=SAMPLES)
    assert general is not None
    assert general.format == "json"
    assert general.include_offcuts is True

    scoped = find_export_template("SVG sin retales", client="Demo", path=SAMPLES)
    assert scoped is not None
    assert scoped.format == "svg"
    assert scoped.include_offcuts is False

    missing = find_export_template("SVG sin retales", path=SAMPLES)
    assert missing is None


def test_parse_share_pack():
    templates = parse_export_templates_payload(
        {
            "version": 1,
            "kind": "boardcomposer.export_templates",
            "templates": [
                {"name": "CSV", "format": "csv", "client": "Acme"},
            ],
        }
    )
    assert len(templates) == 1
    assert templates[0].client == "Acme"
    assert templates[0].format == "csv"

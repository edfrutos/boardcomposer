"""Structural diff between two ``.bcproj`` revisions (FLW-006 debt).

Compares migrated project JSON (ADR-015) without Qt. Not a full JSON patch:
focuses on inventory, pieces, placements, and project metadata that matter
when auditing saves between sessions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from boardcomposer.io.bcproj import migrate_bcproj_dict

_META_KEYS = ("version", "project_id", "name")
_BOARD_FIELDS = (
    "board_id",
    "length_mm",
    "width_mm",
    "thickness_mm",
    "quantity",
    "material",
)
_PIECE_FIELDS = (
    "piece_id",
    "length_mm",
    "width_mm",
    "thickness_mm",
    "material",
)


@dataclass(frozen=True)
class BcprojChange:
    path: str
    kind: str  # added | removed | changed
    before: Any = None
    after: Any = None


@dataclass
class BcprojDiff:
    left: str
    right: str
    identical: bool
    changes: list[BcprojChange] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "left": self.left,
            "right": self.right,
            "identical": self.identical,
            "change_count": len(self.changes),
            "changes": [asdict(change) for change in self.changes],
        }

    def summary_lines(self) -> list[str]:
        if self.identical:
            return [f"identical: {self.left} == {self.right}"]
        lines = [
            f"diff: {self.left} → {self.right}",
            f"changes: {len(self.changes)}",
        ]
        for change in self.changes:
            if change.kind == "changed":
                lines.append(f"  ~ {change.path}: {change.before!r} → {change.after!r}")
            elif change.kind == "added":
                lines.append(f"  + {change.path}: {change.after!r}")
            else:
                lines.append(f"  - {change.path}: {change.before!r}")
        return lines


def load_bcproj_dict(path: str | Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"bcproj must be a JSON object: {path}")
    return migrate_bcproj_dict(payload)


def diff_bcproj(
    left: str | Path | dict,
    right: str | Path | dict,
    *,
    left_label: str | None = None,
    right_label: str | None = None,
) -> BcprojDiff:
    """Compare two ``.bcproj`` paths or already-loaded dicts."""
    left_data, left_name = _coerce(left, left_label)
    right_data, right_name = _coerce(right, right_label)
    changes: list[BcprojChange] = []

    for key in _META_KEYS:
        _compare_scalar(changes, key, left_data.get(key), right_data.get(key))

    _diff_indexed(
        changes,
        section="boards",
        left_items=left_data.get("boards", []),
        right_items=right_data.get("boards", []),
        id_key="board_id",
        fields=_BOARD_FIELDS,
    )
    _diff_indexed(
        changes,
        section="pieces",
        left_items=left_data.get("pieces", []),
        right_items=right_data.get("pieces", []),
        id_key="piece_id",
        fields=_PIECE_FIELDS,
    )

    left_placements = left_data.get("placements", []) or []
    right_placements = right_data.get("placements", []) or []
    if len(left_placements) != len(right_placements):
        changes.append(
            BcprojChange(
                path="placements.count",
                kind="changed",
                before=len(left_placements),
                after=len(right_placements),
            )
        )
    else:
        left_fp = [_placement_fingerprint(item) for item in left_placements]
        right_fp = [_placement_fingerprint(item) for item in right_placements]
        if left_fp != right_fp:
            changes.append(
                BcprojChange(
                    path="placements",
                    kind="changed",
                    before=left_fp,
                    after=right_fp,
                )
            )

    return BcprojDiff(
        left=left_name,
        right=right_name,
        identical=not changes,
        changes=changes,
    )


def _coerce(value: str | Path | dict, label: str | None) -> tuple[dict, str]:
    if isinstance(value, dict):
        return migrate_bcproj_dict(value), label or "<dict>"
    path = Path(value)
    return load_bcproj_dict(path), label or str(path)


def _compare_scalar(
    changes: list[BcprojChange], path: str, before: Any, after: Any
) -> None:
    if before != after:
        changes.append(
            BcprojChange(path=path, kind="changed", before=before, after=after)
        )


def _item_key(item: dict, id_key: str, index: int) -> str:
    raw = item.get(id_key)
    if raw is None or str(raw).strip() == "":
        return f"#{index}"
    return str(raw)


def _normalize_item(item: dict, fields: tuple[str, ...]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for field_name in fields:
        if field_name in item:
            value = item[field_name]
            if field_name.endswith("_mm"):
                normalized[field_name] = float(value)
            elif field_name == "quantity":
                normalized[field_name] = int(value)
            else:
                normalized[field_name] = value
    return normalized


def _diff_indexed(
    changes: list[BcprojChange],
    *,
    section: str,
    left_items: list,
    right_items: list,
    id_key: str,
    fields: tuple[str, ...],
) -> None:
    left_map: dict[str, dict] = {}
    right_map: dict[str, dict] = {}
    for index, item in enumerate(left_items or []):
        if isinstance(item, dict):
            left_map[_item_key(item, id_key, index)] = _normalize_item(item, fields)
    for index, item in enumerate(right_items or []):
        if isinstance(item, dict):
            right_map[_item_key(item, id_key, index)] = _normalize_item(item, fields)

    for key in sorted(set(left_map) | set(right_map), key=str):
        path = f"{section}.{key}"
        if key not in left_map:
            changes.append(BcprojChange(path=path, kind="added", after=right_map[key]))
        elif key not in right_map:
            changes.append(
                BcprojChange(path=path, kind="removed", before=left_map[key])
            )
        elif left_map[key] != right_map[key]:
            before = left_map[key]
            after = right_map[key]
            for field_name in fields:
                if before.get(field_name) != after.get(field_name):
                    changes.append(
                        BcprojChange(
                            path=f"{path}.{field_name}",
                            kind="changed",
                            before=before.get(field_name),
                            after=after.get(field_name),
                        )
                    )


def _placement_fingerprint(item: dict) -> tuple:
    return (
        item.get("piece_id") or item.get("board_id"),
        item.get("x_mm"),
        item.get("y_mm"),
        item.get("rotated"),
        item.get("rotation"),
        item.get("board_id"),
        item.get("board_instance"),
        item.get("stock_panel_index"),
    )

"""Tests for studio.recent_files — in-memory and disk-persisted behaviour."""

import json


from studio.recent_files import RecentFilesManager


def _manager(tmp_path, *, max_items: int = 5) -> RecentFilesManager:
    """Return a manager backed by a temp path (no global side effects)."""
    return RecentFilesManager(path=tmp_path / "recent.json", max_items=max_items)


# ---------------------------------------------------------------------------
# In-memory add / order / cap
# ---------------------------------------------------------------------------


def test_add_single_entry(tmp_path):
    mgr = _manager(tmp_path)
    mgr.add("/a/project.bcproj")
    assert mgr.files == ["/a/project.bcproj"]


def test_add_moves_existing_to_front(tmp_path):
    mgr = _manager(tmp_path)
    mgr.add("/a.bcproj")
    mgr.add("/b.bcproj")
    mgr.add("/a.bcproj")
    assert mgr.files[0] == "/a.bcproj"
    assert mgr.files.count("/a.bcproj") == 1


def test_add_respects_max_items(tmp_path):
    mgr = _manager(tmp_path, max_items=3)
    for i in range(5):
        mgr.add(f"/p{i}.bcproj")
    assert len(mgr.files) == 3


def test_clear_empties_list(tmp_path):
    mgr = _manager(tmp_path)
    mgr.add("/a.bcproj")
    mgr.clear()
    assert mgr.files == []


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------


def test_remove_present_entry(tmp_path):
    mgr = _manager(tmp_path)
    mgr.add("/a.bcproj")
    assert mgr.remove("/a.bcproj") is True
    assert mgr.files == []


def test_remove_absent_entry_returns_false(tmp_path):
    mgr = _manager(tmp_path)
    assert mgr.remove("/nonexistent.bcproj") is False


# ---------------------------------------------------------------------------
# prune_missing / existing_files
# ---------------------------------------------------------------------------


def test_prune_missing_removes_nonexistent(tmp_path):
    mgr = _manager(tmp_path)
    real = tmp_path / "real.bcproj"
    real.write_text("{}")
    mgr.add(str(real))
    mgr.add("/ghost.bcproj")
    removed = mgr.prune_missing()
    assert removed == 1
    assert str(real) in mgr.files
    assert "/ghost.bcproj" not in mgr.files


def test_existing_files_filters_nonexistent(tmp_path):
    mgr = _manager(tmp_path)
    real = tmp_path / "real.bcproj"
    real.write_text("{}")
    mgr.add(str(real))
    mgr.add("/gone.bcproj")
    assert mgr.existing_files() == [str(real)]


# ---------------------------------------------------------------------------
# Disk persistence — save / load round-trip
# ---------------------------------------------------------------------------


def test_save_and_reload(tmp_path):
    mgr = _manager(tmp_path)
    mgr.add("/a.bcproj")
    mgr.add("/b.bcproj")

    mgr2 = _manager(tmp_path)
    assert mgr2.files == ["/b.bcproj", "/a.bcproj"]


def test_load_tolerates_corrupt_json(tmp_path):
    path = tmp_path / "recent.json"
    path.write_text("NOT JSON", encoding="utf-8")
    mgr = RecentFilesManager(path=path)
    assert mgr.files == []


def test_load_tolerates_non_list_json(tmp_path):
    path = tmp_path / "recent.json"
    path.write_text('{"key": "value"}', encoding="utf-8")
    mgr = RecentFilesManager(path=path)
    assert mgr.files == []


def test_load_skips_non_string_entries(tmp_path):
    path = tmp_path / "recent.json"
    path.write_text(
        json.dumps(["/ok.bcproj", 42, None, "/also-ok.bcproj"]), encoding="utf-8"
    )
    mgr = RecentFilesManager(path=path)
    assert mgr.files == ["/ok.bcproj", "/also-ok.bcproj"]


def test_save_creates_parent_dir(tmp_path):
    nested = tmp_path / "nested" / "dir" / "recent.json"
    mgr = RecentFilesManager(path=nested)
    mgr.add("/x.bcproj")
    assert nested.is_file()

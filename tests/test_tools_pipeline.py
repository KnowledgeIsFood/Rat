from __future__ import annotations

import contextlib
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import emit_shanhaijing_chapters as emit
from tools import render_shanhaijing_docs as render


def _creature_row(**overrides: str) -> dict[str, str]:
    row = {
        "chapter_group": "nanshan_jing",
        "kind_zh": "异兽",
        "id": "test_creature",
        "name_zh": "测试兽",
        "aliases_zh": "别名一|别名二",
        "corpus_zh": "五藏山經",
        "jing_zh": "南山經",
        "section_zh": "南山經之首",
        "mountain_zh": "测试山",
        "literature_appearance_zh": "状如测试。",
        "traits_effects_zh": "用于测试。",
        "habitat_ecology_zh": "测试环境。",
        "food_web_zh": "测试食物链。",
        "trophic_role_zh": "测试角色",
        "artistic_portrait_note_zh": "测试美术要点。",
        "related_zh": "关联一|关联二",
        "sources_note_zh": "测试来源。",
    }
    row.update(overrides)
    return row


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = emit.REQUIRED_COLUMNS + ["aliases_zh", "related_zh", "sources_note_zh"]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


@contextlib.contextmanager
def _patched_attr(module: object, **values: object):
    original = {name: getattr(module, name) for name in values}
    try:
        for name, value in values.items():
            setattr(module, name, value)
        yield
    finally:
        for name, value in original.items():
            setattr(module, name, value)


class EmitShanhaijingChaptersTest(unittest.TestCase):
    def test_main_emits_default_and_extra_chapter_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "creatures_master.csv"
            out_dir = root / "chapters"
            _write_csv(
                csv_path,
                [
                    _creature_row(),
                    _creature_row(
                        chapter_group="custom_group",
                        id="custom_creature",
                        aliases_zh="",
                        related_zh="",
                    ),
                ],
            )

            with _patched_attr(emit, CSV_PATH=csv_path, OUT_DIR=out_dir):
                with contextlib.redirect_stdout(io.StringIO()):
                    emit.main()

            nanshan = json.loads((out_dir / "nanshan_jing.json").read_text(encoding="utf-8"))
            custom = json.loads((out_dir / "custom_group.json").read_text(encoding="utf-8"))

            self.assertEqual(["test_creature"], [c["id"] for c in nanshan["creatures"]])
            self.assertEqual(["别名一", "别名二"], nanshan["creatures"][0]["aliases_zh"])
            self.assertEqual(["custom_creature"], [c["id"] for c in custom["creatures"]])

    def test_validate_rows_rejects_duplicate_ids(self) -> None:
        rows = [_creature_row(), _creature_row(chapter_group="xishan_jing")]

        with self.assertRaisesRegex(SystemExit, "Duplicate id across CSV"):
            emit.validate_rows(rows)


class RenderShanhaijingDocsTest(unittest.TestCase):
    def test_render_writes_catalog_docs_and_godot_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapter_dir = root / "chapters"
            out_by_id = root / "docs" / "by_id"
            out_catalog = root / "docs" / "CATALOG.md"
            godot_data = root / "game" / "creatures_catalog.json"
            chapter_dir.mkdir()

            in_theme = emit.row_to_creature(_creature_row())
            outside_theme = emit.row_to_creature(
                _creature_row(
                    chapter_group="haijing",
                    id="outside_theme",
                    jing_zh="海内西經",
                    kind_zh="奇禽",
                )
            )
            (chapter_dir / "nanshan_jing.json").write_text(
                json.dumps({"creatures": [in_theme]}, ensure_ascii=False),
                encoding="utf-8",
            )
            (chapter_dir / "haijing.json").write_text(
                json.dumps({"creatures": [outside_theme]}, ensure_ascii=False),
                encoding="utf-8",
            )

            with _patched_attr(
                render,
                CHAPTER_DIR=chapter_dir,
                OUT_BY_ID=out_by_id,
                OUT_CATALOG=out_catalog,
                GODOT_DATA=godot_data,
            ):
                creatures = render.load_creatures()
                render.validate(creatures)
                render.write_outputs(creatures)

            payload = json.loads(godot_data.read_text(encoding="utf-8"))

            self.assertEqual("rat.shanhaijing.catalog.v2", payload["schema"])
            self.assertEqual(2, payload["entry_count"])
            self.assertEqual(1, payload["theme_scope"]["entry_count_in_theme"])
            self.assertEqual({"奇禽": 1, "异兽": 1}, payload["kind_counts"])
            self.assertTrue((out_by_id / "test_creature.md").is_file())
            self.assertIn("测试兽", out_catalog.read_text(encoding="utf-8"))

    def test_validate_rejects_missing_required_text(self) -> None:
        creature = emit.row_to_creature(_creature_row(name_zh=""))

        with self.assertRaisesRegex(SystemExit, "missing or empty string field 'name_zh'"):
            render.validate([creature])


if __name__ == "__main__":
    unittest.main()

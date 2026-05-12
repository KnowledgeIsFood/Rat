#!/usr/bin/env python3
"""Read tabular creature data and emit data/shanhaijing/chapters/*.json."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "shanhaijing" / "creatures_master.csv"
OUT_DIR = ROOT / "data" / "shanhaijing" / "chapters"

# Output JSON basenames (without .json) that this pipeline knows about.
# 默认输出顺序：五藏山经（动物）→ 五篇草木分组 → 海经/大荒（扩展，非主线主题）
DEFAULT_CHAPTER_GROUPS = [
    "nanshan_jing",
    "xishan_jing",
    "beishan_jing",
    "dongshan_jing",
    "zhongshan_jing",
    "plants_nanshan_jing",
    "plants_xishan_jing",
    "plants_beishan_jing",
    "plants_dongshan_jing",
    "plants_zhongshan_jing",
    "plants_wucang_misc",
    "haijing",
    "dahuang_jing",
]

REQUIRED_COLUMNS = [
    "chapter_group",
    "kind_zh",
    "id",
    "name_zh",
    "corpus_zh",
    "jing_zh",
    "section_zh",
    "mountain_zh",
    "literature_appearance_zh",
    "traits_effects_zh",
    "habitat_ecology_zh",
    "food_web_zh",
    "trophic_role_zh",
    "artistic_portrait_note_zh",
]


def split_pipe(cell: str | None) -> list[str] | None:
    if cell is None:
        return None
    s = str(cell).strip()
    if not s:
        return None
    parts = [p.strip() for p in s.split("|") if p.strip()]
    return parts or None


def load_rows() -> list[dict[str, str]]:
    if not CSV_PATH.is_file():
        raise SystemExit(f"Missing CSV: {CSV_PATH}")
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise SystemExit("CSV has no header row")
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        extra_ok = {"aliases_zh", "related_zh", "sources_note_zh"}
        unknown = [c for c in reader.fieldnames if c not in REQUIRED_COLUMNS and c not in extra_ok]
        if unknown:
            raise SystemExit(f"Unknown CSV columns: {unknown}")
        if missing:
            raise SystemExit(f"CSV missing required columns: {missing}")
        return list(reader)


def row_to_creature(row: dict[str, str]) -> dict:
    keys_out = [k for k in REQUIRED_COLUMNS if k != "chapter_group"]
    c: dict = {k: (row.get(k) or "").strip() for k in keys_out}
    aliases = split_pipe(row.get("aliases_zh"))
    if aliases:
        c["aliases_zh"] = aliases
    related = split_pipe(row.get("related_zh"))
    if related:
        c["related_zh"] = related
    note = (row.get("sources_note_zh") or "").strip()
    if note:
        c["sources_note_zh"] = note
    return c


def validate_rows(rows: list[dict[str, str]]) -> None:
    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        for col in REQUIRED_COLUMNS:
            if col == "chapter_group":
                continue
            val = (row.get(col) or "").strip()
            if not val:
                raise SystemExit(f"Row {i}: empty required field '{col}' (id={row.get('id')!r})")
        cg = (row.get("chapter_group") or "").strip()
        if not cg:
            raise SystemExit(f"Row {i}: empty chapter_group")
        cid = row["id"].strip()
        if cid in seen:
            raise SystemExit(f"Duplicate id across CSV: {cid}")
        seen.add(cid)


def dump_chapter(name: str, creatures: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump({"creatures": creatures}, f, ensure_ascii=False, indent=2)
    print(f"wrote {path} ({len(creatures)})")


def main() -> None:
    rows = load_rows()
    validate_rows(rows)

    by_group: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        cg = row["chapter_group"].strip()
        by_group[cg].append(row_to_creature(row))

    # Emit known chapter files (including empty lists if a group disappears).
    for name in DEFAULT_CHAPTER_GROUPS:
        dump_chapter(name, by_group.get(name, []))

    extra = sorted(set(by_group) - set(DEFAULT_CHAPTER_GROUPS))
    if extra:
        for name in extra:
            dump_chapter(name, by_group[name])
        print("note: extra chapter_group keys written:", ", ".join(extra))


if __name__ == "__main__":
    main()

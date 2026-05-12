#!/usr/bin/env python3
"""Merge chapter JSON, validate fields, emit Markdown catalog + Godot catalog JSON."""

from __future__ import annotations

import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "data" / "shanhaijing" / "chapters"
OUT_BY_ID = ROOT / "docs" / "shanhaijing" / "creatures" / "by_id"
OUT_CATALOG = ROOT / "docs" / "shanhaijing" / "CATALOG.md"
GODOT_DATA = ROOT / "game" / "data" / "creatures_catalog.json"

# 游戏主线：五藏山经五篇（与 jing_zh 字段一致）
THEME_PRIMARY_JING_ZH: frozenset[str] = frozenset(
    {"南山經", "西山經", "北山經", "东山經", "中山經"}
)

REQUIRED_KEYS = (
    "id",
    "kind_zh",
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
)


def load_creatures() -> list[dict]:
    if not CHAPTER_DIR.is_dir():
        raise SystemExit(f"Missing chapter dir: {CHAPTER_DIR}")
    creatures: list[dict] = []
    for path in sorted(CHAPTER_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            doc = json.load(f)
        arr = doc.get("creatures")
        if not isinstance(arr, list):
            raise SystemExit(f"{path}: expected top-level 'creatures' array")
        for c in arr:
            if not isinstance(c, dict):
                raise SystemExit(f"{path}: creature must be object")
            c["_source_file"] = path.name
            creatures.append(c)
    return creatures


def validate(creatures: list[dict]) -> None:
    seen: set[str] = set()
    for c in creatures:
        cid = c.get("id", "")
        for k in REQUIRED_KEYS:
            if k not in c or not isinstance(c[k], str) or not str(c[k]).strip():
                raise SystemExit(f"creature '{cid}': missing or empty string field '{k}'")
        if cid in seen:
            raise SystemExit(f"duplicate id: {cid}")
        seen.add(cid)


def md_escape(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def render_creature_md(c: dict) -> str:
    aliases = c.get("aliases_zh")
    aliases_line = ""
    if isinstance(aliases, list) and aliases:
        aliases_line = f"- **异名 / 别名**：{'、'.join(aliases)}\n"
    related = c.get("related_zh")
    related_block = ""
    if isinstance(related, list) and related:
        related_block = "\n## 关联\n\n" + "\n".join(f"- {x}" for x in related) + "\n"
    disclaimer = c.get(
        "sources_note_zh",
        "本条目为游戏设计侧整理的通行本大意与生态推演，非权威逐字校勘；制作剧情请以选定注本为准。",
    )
    body = f"""# {c["name_zh"]}

- **稳定 ID**：`{c["id"]}`
- **类目**：{c["kind_zh"]}
- **所属典籍**：{c["corpus_zh"]} · {c["jing_zh"]}
- **篇段 / 列系**：{c["section_zh"]}
- **所在山川 / 水域**：{c["mountain_zh"]}
{aliases_line}
## 文述画像（据经籍大意）

{md_escape(c["literature_appearance_zh"])}

## 特点与异效（经载 / 传说）

{md_escape(c["traits_effects_zh"])}

## 生态环境（推演）

{md_escape(c["habitat_ecology_zh"])}

## 生物链与种间关系（推演）

{md_escape(c["food_web_zh"])}

- **营养级角色（设计标签）**：{c["trophic_role_zh"]}

## 美术画像要点（由文言转化为可视要素）

{md_escape(c["artistic_portrait_note_zh"])}
{related_block}
## 资料说明

{md_escape(str(disclaimer))}

---
*源数据文件：* `{c.get("_source_file", "")}`
"""
    return body.lstrip()


def write_outputs(creatures: list[dict]) -> None:
    OUT_BY_ID.mkdir(parents=True, exist_ok=True)
    for p in OUT_BY_ID.glob("*.md"):
        p.unlink()

    for c in creatures:
        out = OUT_BY_ID / f"{c['id']}.md"
        out.write_text(render_creature_md(c), encoding="utf-8")

    lines: list[str] = []
    lines.append("# 山海经条目目录（自动生成）\n")
    lines.append("\n**游戏主线范围**为 **五藏山经**：《南山经》《西山经》《北山经》《东山经》《中山经》。见 `docs/shanhaijing/游戏主题-五藏山经.md`。\n")
    lines.append("\n按 **类目（`kind_zh`）** 与 **篇名（`jing_zh`）** 分组；条目文件位于 `creatures/by_id/`。\n")

    by_kind: dict[str, list[dict]] = defaultdict(list)
    for c in creatures:
        by_kind[c["kind_zh"]].append(c)

    for kind in sorted(by_kind.keys()):
        lines.append(f"\n## 类目：{kind}\n")
        by_jing: dict[str, list[dict]] = defaultdict(list)
        for c in by_kind[kind]:
            by_jing.setdefault(c["jing_zh"], []).append(c)
        for jing in sorted(by_jing.keys()):
            lines.append(f"\n### {jing}\n")
            for c in sorted(by_jing[jing], key=lambda x: x["id"]):
                lines.append(
                    f"- [{c['name_zh']}](creatures/by_id/{c['id']}.md) — `{c['id']}` — {c['mountain_zh']}"
                )

    OUT_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    OUT_CATALOG.write_text("\n".join(lines) + "\n", encoding="utf-8")

    kind_counts: dict[str, int] = defaultdict(int)
    for c in creatures:
        kind_counts[c["kind_zh"]] += 1

    in_theme = sum(1 for c in creatures if c.get("jing_zh") in THEME_PRIMARY_JING_ZH)
    out_theme = len(creatures) - in_theme
    theme_scope = {
        "title_zh": "五藏山经（游戏主线）",
        "jing_zh": sorted(THEME_PRIMARY_JING_ZH),
        "entry_count_in_theme": in_theme,
        "entry_count_outside_theme": out_theme,
        "entry_count_total": len(creatures),
    }

    GODOT_DATA.parent.mkdir(parents=True, exist_ok=True)
    entries = [{k: v for k, v in c.items() if not k.startswith("_")} for c in creatures]
    payload = {
        "schema": "rat.shanhaijing.catalog.v2",
        "generated_note": "merged from data/shanhaijing/chapters/*.json",
        "entry_count": len(creatures),
        "theme_scope": theme_scope,
        "kind_counts": dict(sorted(kind_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "entries": entries,
        "creatures": entries,
    }
    GODOT_DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    creatures = load_creatures()
    validate(creatures)
    write_outputs(creatures)
    print(f"OK: {len(creatures)} entries -> {OUT_CATALOG} , {OUT_BY_ID}/ , {GODOT_DATA}")


if __name__ == "__main__":
    main()

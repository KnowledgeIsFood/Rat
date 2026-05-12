# Rat — Godot 工程

- **引擎版本**：Godot 4.6（`project.godot` 中 `config/features` 含 `4.6`）
- **主场景**：`main.tscn` → `main.gd` 读取 `res://data/creatures_catalog.json`，显示全表条数、类目计数及 **`theme_scope`（五藏山经内条目数）**。
- **当前美术占位**：
  - 背景：`game/assets/backgrounds/wilderness_ink_wide.svg`（横版旷野水墨）
  - 异兽：`game/assets/sprites/creatures/baiyuan_16x16.svg`（白猿，16×16）

## 数据管线

仓库根目录运行（先改表 `../data/shanhaijing/creatures_master.csv`）：

```bash
python3 tools/emit_shanhaijing_chapters.py
python3 tools/render_shanhaijing_docs.py
```

会在 `game/data/` 生成最新的 `creatures_catalog.json`（供本工程读取），并在 `docs/shanhaijing/` 生成 Markdown 目录与分条文件。主表说明见 `docs/shanhaijing/表格维护说明.md`；**五经主题范围**见 `docs/shanhaijing/游戏主题-五藏山经.md`。

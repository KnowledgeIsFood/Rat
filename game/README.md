# Rat — Godot 工程

- **引擎版本**：Godot 4.6（`project.godot` 中 `config/features` 含 `4.6`）
- **主场景**：`main.tscn` → `main.gd` 读取 `res://data/creatures_catalog.json` 并显示条目数。

## 数据管线

仓库根目录运行：

```bash
python3 tools/emit_shanhaijing_chapters.py
python3 tools/render_shanhaijing_docs.py
```

会在 `game/data/` 生成最新的 `creatures_catalog.json`（供本工程读取），并在 `docs/shanhaijing/` 生成 Markdown 目录与分条文件。

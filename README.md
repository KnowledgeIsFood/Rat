# Rat

《山海经》世界观的 **成长 · 异变 · 肉鸽** 游戏原型仓库。

## 游戏主题（五本经）

主线经本为 **《山经》五篇——五藏山经**：

**《南山经》《西山经》《北山经》《东山经》《中山经》**

关卡、叙事与博物条目建议以这五篇为纲；`海经` / `大荒经` 等若出现在数据表中，仅作扩展参考（见 `docs/shanhaijing/游戏主题-五藏山经.md`）。

## 技术栈

- **引擎**：Godot **4.6**（工程目录：`game/`）
- **博物资料**：`data/shanhaijing/creatures_master.csv`（含 `kind_zh`：奇禽/异兽/鳞介/草木等）→ `emit` 生成 `chapters/*.json` → `render` 合并为 `game/data/creatures_catalog.json` 与 `docs/shanhaijing/`。

## 快速开始

1. 安装 [Godot 4.6](https://godotengine.org/download/archive/4.6-stable/)，用编辑器打开 `game/project.godot`。
2. 运行主场景 `main.tscn`：界面会显示载入条目总数与 **类目计数**（`kind_counts`）。
3. 若需 **批量占位扩表**（会重写 CSV、追加 `synth_*` / `plant_*` 行）：`python3 tools/expand_shanhaijing_master_csv.py`（勿在 CI/云端每次自动跑，除非你希望保持占位）。
4. 若你修改了 **`data/shanhaijing/creatures_master.csv`**，请在仓库根目录执行：

```bash
python3 tools/emit_shanhaijing_chapters.py
python3 tools/render_shanhaijing_docs.py
```

## 山海经资料入口

- 人类可读总目录：`docs/shanhaijing/CATALOG.md`
- **游戏主题（五藏山经）**：[游戏主题-五藏山经.md](docs/shanhaijing/游戏主题-五藏山经.md)
- 表格列说明：`docs/shanhaijing/表格维护说明.md`
- 视觉风格规范：`docs/art/视觉风格规范.md`

## 许可与来源

经文文本属公有领域；本仓库中的 **整理、推演与游戏化字段** 为项目原创，供开发与协作使用。

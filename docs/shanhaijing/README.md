# 《山海经》资料层（游戏策划向）

本目录与 `data/shanhaijing/` 共同构成 **异兽数据库 v1**：以「典籍归属 → 山川/水体 → 个体条目」组织，每条包含 **文述画像**、**特点与异效**、**生态环境（推演）**、**生物链关系（推演）** 与 **美术转化要点**。

## 快速入口

- **总目录（自动生成）**：[CATALOG.md](CATALOG.md)
- **单条 Markdown（自动生成）**：`creatures/by_id/<id>.md`
- **机读合并表（供 Godot 读取）**：`game/data/creatures_catalog.json`（由脚本从 `data/shanhaijing/chapters/*.json` 合并生成）

## 如何扩充（主表 CSV）

1. 在 **`data/shanhaijing/creatures_master.csv`** 末尾追加一行（或复制上一行改字段）。列含义见 [表格维护说明.md](表格维护说明.md)。
2. 运行：
   - `python3 tools/emit_shanhaijing_chapters.py`
   - `python3 tools/render_shanhaijing_docs.py`
3. 用 Godot 4.6 打开 `game/project.godot`，主场景会显示当前载入条目数。

## 重要说明（非校勘稿）

- 文本为 **通行本大意 + 游戏化推演**，不等同于学术逐字校勘。
- 古《山海图》早佚，**画像**以「文言形体描写 → 美术可控要素」的方式记录；可对照历代绘本（如明清刻本）再创作。
- 同名异物（如不同篇的「肥遗」）在条目中以 **不同 id** 区分。

更多背景见 [00_综述与体量说明.md](00_综述与体量说明.md)、[分类与索引说明.md](分类与索引说明.md)、[生态环境与食物链总论.md](生态环境与食物链总论.md)。

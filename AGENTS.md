# AGENTS.md

## Cursor Cloud specific instructions

### 产品

《山海经》题材 **成长 · 异变 · 肉鸽** 游戏（代号 Rat）。当前以 **Godot 4.6** 工程 `game/` 为主，异兽数据以 **`data/shanhaijing/creatures_master.csv`** 为主表维护；`tools/emit_shanhaijing_chapters.py` 读取 CSV 写出 `data/shanhaijing/chapters/*.json`，`tools/render_shanhaijing_docs.py` 再合并为 `game/data/creatures_catalog.json` 并生成 `docs/shanhaijing/CATALOG.md` 与 `creatures/by_id/*.md`。

### Godot

- 打开 `game/project.godot`。
- 若云端未预装 Godot 二进制，无法在 VM 内无头运行编辑器；以本机 Godot 4.6 打开为准。
- `main.gd` 仅在缺少 `creatures_catalog.json` 时给出运行脚本的提示文案。

### 数据工作流（不要手改生成物）

- **不要**手改 `docs/shanhaijing/CATALOG.md` 或 `docs/shanhaijing/creatures/by_id/*.md` 或 `game/data/creatures_catalog.json`：会被脚本覆盖。
- 扩充异兽：编辑 **`data/shanhaijing/creatures_master.csv`**（见 `docs/shanhaijing/表格维护说明.md`），然后依次运行 `emit` 与 `render` 脚本。

### 与标准文档的关系

人类可读的背景与方法论见 `docs/shanhaijing/README.md` 及同目录下综述、分类、生态总论；此处不重复。

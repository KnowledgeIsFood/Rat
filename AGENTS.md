# AGENTS.md

## Cursor Cloud specific instructions

### 产品

《山海经》题材 **成长 · 异变 · 肉鸽** 游戏（代号 Rat）。**主线经本**为 **五藏山经**五篇：《南山经》《西山经》《北山经》《东山经》《中山经》（见 `docs/shanhaijing/游戏主题-五藏山经.md`）。`海经` / `大荒经` 等条目若存在，视为扩展资料，不纳入主题主轴。

当前以 **Godot 4.6** 工程 `game/` 为主，博物数据以 **`data/shanhaijing/creatures_master.csv`** 为主表（列 **`kind_zh`**：奇禽/异兽/鳞介/草木等）；`tools/emit_shanhaijing_chapters.py` 读取 CSV 写出 `data/shanhaijing/chapters/*.json`（含 `plants_*` 草木分组），`tools/render_shanhaijing_docs.py` 再合并为 `game/data/creatures_catalog.json`（`schema` v2，含 `kind_counts`、`theme_scope` 与 `entries`）并生成 `docs/shanhaijing/CATALOG.md` 与 `creatures/by_id/*.md`。

### Godot

- 打开 `game/project.godot`。
- 若云端未预装 Godot 二进制，无法在 VM 内无头运行编辑器；以本机 Godot 4.6 打开为准。
- `main.gd` 读取 `entries`（或回退 `creatures`）与 `kind_counts`，展示载入条数与类目计数。

### 数据工作流（不要手改生成物）

- **不要**手改 `docs/shanhaijing/CATALOG.md` 或 `docs/shanhaijing/creatures/by_id/*.md` 或 `game/data/creatures_catalog.json`：会被脚本覆盖。
- 扩充条目：编辑 **`data/shanhaijing/creatures_master.csv`**（见 `docs/shanhaijing/表格维护说明.md`），然后依次运行 `emit` 与 `render`。
- **批量占位扩表**（会重写 CSV）：`python3 tools/expand_shanhaijing_master_csv.py` — 仅在需要大量 `synth_*` / `plant_*` 占位时运行；**不要**放进云端每次自动执行的 update 脚本，以免覆盖人工删改。

### 与标准文档的关系

人类可读的背景与方法论见 `docs/shanhaijing/README.md` 及同目录下综述、分类、生态总论；此处不重复。

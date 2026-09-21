# AGENTS.md

## Cursor Cloud specific instructions

### 后续操作必须以 3AGameFactory 为准

Rat 的游戏生成、资产、玩法、UI、导入、启动与验收 **以 [3AGameFactory](https://github.com/OpenDCAI/GameFactory-3A) 文档和公共 API 为权威**。产品世界观仍是五藏山经，但不要再按“直接改 Godot 工程即可”的方式跳过框架工作流。

1. 若 `third_party/GameFactory-3A/agent_skills/setting_overview.md` 不存在，先运行 `git submodule update --init --recursive third_party/GameFactory-3A` 或 `bash tools/bootstrap_gamefactory.sh`。
2. **先读** `third_party/GameFactory-3A/agent_skills/setting_overview.md`。这是框架入口；其中的 `<REPO_PATH>` 等于本仓库的 `third_party/GameFactory-3A`。
3. 再读 Rat 任务包：`docs/gamefactory/task_packet.json`、`docs/gamefactory/general_requirement.txt`、`docs/gamefactory/README.md`。
4. 固定选择：**引擎 `godot`，版本 4.6（官方标签 `4.6-stable`），工程 `game/`，`game_id=gameR_wucang_shanjing_godot`**。不要改用 UE5 / Unity / three.js，也不要传不存在的 `4.6.0`。
5. 宿主机只使用 `from engine_adapters.godot import GodotClient`（`PYTHONPATH` 指向 `third_party/GameFactory-3A`）。不要手写导入/启动/导出旁路。
6. 禁止对已有 `game/` 执行 `create-project`。需要运行时插件时用 `install-framework`。
7. 生成物路径只用 `<REPO_PATH>/pipeline/common/paths.py`。不要手改上游子模块来修游戏。
8. 付费云端资产生成必须先征得用户同意。编译成功不等于可玩；要按 setting_overview 做白盒、资产 QA、实机游玩与录像。

本机可执行文件与插件安装：

```bash
bash tools/bootstrap_gamefactory.sh --with-godot --install-framework
```

云端若未预装 Godot，不要假装引擎已验证；用 `python3 tools/gamefactory_env.py adapter-info` 记录缺口，Godot 操作留到有官方二进制之后。

### 产品

《山海经》题材 **成长 · 异变 · 肉鸽** 游戏（代号 Rat）。**主线经本**为 **五藏山经**五篇：《南山经》《西山经》《北山经》《东山经》《中山经》（见 `docs/shanhaijing/游戏主题-五藏山经.md`）。`海经` / `大荒经` 等条目若存在，视为扩展资料，不纳入主题主轴。

当前以 **Godot 4.6** 工程 `game/` 为主，博物数据以 **`data/shanhaijing/creatures_master.csv`** 为主表（列 **`kind_zh`**：奇禽/异兽/鳞介/草木等）；`tools/emit_shanhaijing_chapters.py` 读取 CSV 写出 `data/shanhaijing/chapters/*.json`（含 `plants_*` 草木分组），`tools/render_shanhaijing_docs.py` 再合并为 `game/data/creatures_catalog.json`（`schema` v2，含 `kind_counts`、`theme_scope` 与 `entries`）并生成 `docs/shanhaijing/CATALOG.md` 与 `creatures/by_id/*.md`。

### Godot

- 打开 `game/project.godot`。
- 引擎发现、安装与校验走 3AGameFactory：`third_party/GameFactory-3A/scripts/engine_install/godot/install.sh --version 4.6 --json`。
- 若云端未预装 Godot 二进制，无法在 VM 内无头运行编辑器；以本机 Godot 4.6 打开为准。
- `main.gd` 读取 `entries`（或回退 `creatures`）与 `kind_counts`，展示载入条数与类目计数。
- 参考实现只读：`third_party/GameFactory-3A/engine_adapters/godot/`，不要拷贝 examples 进 `game/` 当运行时依赖。

### 数据工作流（不要手改生成物）

- **不要**手改 `docs/shanhaijing/CATALOG.md` 或 `docs/shanhaijing/creatures/by_id/*.md` 或 `game/data/creatures_catalog.json`：会被脚本覆盖。
- 扩充条目：编辑 **`data/shanhaijing/creatures_master.csv`**（见 `docs/shanhaijing/表格维护说明.md`），然后依次运行 `emit` 与 `render`。
- **批量占位扩表**（会重写 CSV）：`python3 tools/expand_shanhaijing_master_csv.py` — 仅在需要大量 `synth_*` / `plant_*` 占位时运行；**不要**放进云端每次自动执行的 update 脚本，以免覆盖人工删改。

### 与标准文档的关系

人类可读的背景与方法论见 `docs/shanhaijing/README.md` 及同目录下综述、分类、生态总论；框架操作说明见 `docs/gamefactory/README.md`。此处不重复。

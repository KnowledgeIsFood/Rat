# 3AGameFactory 在 Rat 中的用法

本仓库用 [OpenDCAI/GameFactory-3A](https://github.com/OpenDCAI/GameFactory-3A) 作为后续游戏生成与引擎操作的权威框架。上游文档优先于本文；本文只记录 **Rat 如何接到该框架**。

## 安装

仓库根目录：

```bash
git submodule update --init --recursive third_party/GameFactory-3A
bash tools/bootstrap_gamefactory.sh
```

需要本机 Godot 时：

```bash
bash tools/bootstrap_gamefactory.sh --with-godot
```

需要把 `A3GamePlayable` 装进现有 `game/` 工程时（会改 `game/project.godot` 并写入 `game/addons/a3game_playable/`）：

```bash
bash tools/bootstrap_gamefactory.sh --with-godot --install-framework
```

bootstrap 会：

1. 检出 `third_party/GameFactory-3A`（即框架文档里的 `<REPO_PATH>`）。
2. 可选安装官方 Godot **4.6.0-stable** 到仓库本地 `.tools/`（不提交）。
3. 导出 `A3GAME_GODOT_PROJECT` 指向 `game/`，`PYTHONPATH` 指向框架根目录。
4. 可选通过公共 API `python3 -m engine_adapters.godot install-framework` 安装运行时插件。

不要对已有的 `game/` 执行 `create-project`。那会按空工程模板覆盖 Rat。

## Agent 必须遵守的顺序

后续任何玩法、UI、场景、资产、导入、启动工作都按上游入口走：

1. 读 [`third_party/GameFactory-3A/agent_skills/setting_overview.md`](../../third_party/GameFactory-3A/agent_skills/setting_overview.md)
2. 读本目录 [`task_packet.json`](task_packet.json) 与 [`general_requirement.txt`](general_requirement.txt)
3. 设计阶段读 `agent_skills/game_design/SKILL.md`
4. 白盒：简单几何打通玩家闭环，保留稳定 asset ID
5. 资产：`agent_skills/asset_qa/` 中对应 Skill，QA 通过后再替换占位
6. 玩法 / UI：先 `engine_context/engine_overview.md`，再 mechanic / UI Skill，最后只读 `godot_api.md`
7. 宿主机操作只走 `from engine_adapters.godot import GodotClient`
8. 构建、启动、实际游玩并留下录像证据；编译成功不等于可玩

Rat 的固定选择：

| 项 | 值 |
|---|---|
| 引擎标识 | `godot` |
| Godot 版本 | `4.6.0` |
| `game_id` | `gameR_wucang_shanjing_godot` |
| 工程 | `game/` |
| 公共客户端 | `GodotClient` |
| 运行时插件 | `A3GamePlayable`（`res://addons/a3game_playable/`） |

上游 Godot 安装器默认钉在 `4.5.1`；Rat 明确请求 `4.6.0`，与现有 `game/project.godot` 的 4.6 feature 对齐。框架文档里的 Godot 基线仍以 `godot_api.md` 为准，4.6 上的差异视为未验证行为，需在本机复核。

## 路径约定

框架文档中的 `<REPO_PATH>` **不是** Rat 仓库根，而是：

```text
<REPO_PATH> = <Rat 仓库根>/third_party/GameFactory-3A
```

在该目录执行框架脚本。生成物落在 `<REPO_PATH>/test_data/outputs/<game_id>/<run_id>/...`，用 `pipeline/common/paths.py`，不要手写路径。

博物表、经文文档、Godot 工程仍在 Rat 仓库：

- 主表：`data/shanhaijing/creatures_master.csv`
- 渲染：`tools/emit_shanhaijing_chapters.py` → `tools/render_shanhaijing_docs.py`
- 运行时目录：`game/data/creatures_catalog.json`

## 常用命令

```bash
eval "$(python3 tools/gamefactory_env.py export-env)"
python3 tools/gamefactory_env.py adapter-info
python3 -m engine_adapters.godot --project "$A3GAME_GODOT_PROJECT" info
python3 -m engine_adapters.godot --project "$A3GAME_GODOT_PROJECT" validate-project --no-engine
```

有已验证的 Godot 可执行文件后，去掉 `--no-engine`，再用 `import-asset`、`install-framework`、`launch-game`、`playtest`。

## 禁止事项

- 不要手改 `third_party/GameFactory-3A` 来“修游戏”；游戏代码写在 `game/`。
- 不要混用 UE5 / Unity / three.js API。
- 不要把 `engine_adapters/godot/examples/` 拷进 `game/` 当运行时依赖。
- 不要在未获用户同意时调用付费云端资产 API。
- 不要手改会被脚本覆盖的 `docs/shanhaijing/CATALOG.md`、`docs/shanhaijing/creatures/by_id/*.md`、`game/data/creatures_catalog.json`。

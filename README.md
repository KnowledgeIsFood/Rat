# Rat

《山海经》世界观的 **成长 · 异变 · 肉鸽** 游戏原型仓库。

## 技术栈

- **引擎**：Godot **4.6**（工程目录：`game/`）
- **异兽资料**：`data/shanhaijing/chapters/*.json` → 脚本合并为 `game/data/creatures_catalog.json`，并生成 Markdown 目录 `docs/shanhaijing/`。

## 快速开始

1. 安装 [Godot 4.6](https://godotengine.org/download/archive/4.6-stable/)，用编辑器打开 `game/project.godot`。
2. 运行主场景 `main.tscn`：界面会显示已从 `creatures_catalog.json` 载入的异兽条目数。
3. 若你修改了 `tools/emit_shanhaijing_chapters.py` 或相关数据逻辑，请在仓库根目录执行：

```bash
python3 tools/emit_shanhaijing_chapters.py
python3 tools/render_shanhaijing_docs.py
```

## 山海经资料入口

- 人类可读总目录：`docs/shanhaijing/CATALOG.md`
- 背景说明：`docs/shanhaijing/README.md`、`docs/shanhaijing/00_综述与体量说明.md`
- 生态/食物链设计总论：`docs/shanhaijing/生态环境与食物链总论.md`

## 许可与来源

经文文本属公有领域；本仓库中的 **整理、推演与游戏化字段** 为项目原创，供开发与协作使用。

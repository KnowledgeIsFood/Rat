# third_party

本目录只检出外部框架，不要把 Rat 游戏代码写进来。

| 路径 | 来源 | 用途 |
|---|---|---|
| `GameFactory-3A/` | https://github.com/OpenDCAI/GameFactory-3A | 后续游戏生成 Skill、Pipeline 与 Godot 适配器。`<REPO_PATH>` 就是这里。 |

更新：

```bash
git submodule update --init --recursive third_party/GameFactory-3A
git -C third_party/GameFactory-3A fetch origin
git -C third_party/GameFactory-3A checkout main
```

不要在子模块里改游戏或提交 Rat 需求文件；Rat 绑定文档在 `docs/gamefactory/`。

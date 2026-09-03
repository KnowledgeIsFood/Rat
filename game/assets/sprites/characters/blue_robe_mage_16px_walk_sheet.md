# 蓝袍法师 Sprite Sheet 切割说明

- **文件**：`game/assets/sprites/characters/blue_robe_mage_16px_walk_sheet.png`
- **画布**：48 × 64 像素（宽 3 帧 × 高 4 方向）
- **单帧**：16 × 16 像素，格与格之间 **0 像素空隙**
- **格式**：PNG-32（8-bit RGBA），背景 **全透明**（不是洋红 #FF00FF 色键）
- **像素风格**：无抗锯齿；每个通道只有不透明 255 或全透明 0
- **边距**：每一格最外圈 1 像素为透明，角色（含法杖）落在内侧 14 × 14 区域内
- **缩放**：游戏里必须用 **nearest-neighbor**（Godot：`TextureFilter.NEAREST`），禁止线性过滤

再生（不要手改 PNG）：

```bash
python3 tools/build_blue_robe_mage_sheet.py
```

## 布局

```
        x=0          x=16         x=32
         16px         16px         16px
y=0    [step_a]     [idle]      [step_b]     向下（正面）
y=16   [step_a]     [idle]      [step_b]     向左
y=32   [step_a]     [idle]      [step_b]     向右
y=48   [step_a]     [idle]      [step_b]     向上（背面）
```

列含义：

| 列 | 名称 | 说明 |
| --- | --- | --- |
| 0 | `step_a` | 行走 A（画面左侧脚迈出 / 侧视前脚迈出） |
| 1 | `idle` | 站立（也可作走步接触帧） |
| 2 | `step_b` | 行走 B（画面右侧脚迈出 / 侧视后脚迈出） |

推荐走步循环（4 拍）：`step_a → idle → step_b → idle`。

## 每一格像素坐标 `(x, y, w, h)`

坐标系原点在图像左上角，x 向右、y 向下。

| 方向 | 帧 | 名称 | x | y | w | h |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| down | 0 | `down_step_a` | 0 | 0 | 16 | 16 |
| down | 1 | `down_idle` | 16 | 0 | 16 | 16 |
| down | 2 | `down_step_b` | 32 | 0 | 16 | 16 |
| left | 0 | `left_step_a` | 0 | 16 | 16 | 16 |
| left | 1 | `left_idle` | 16 | 16 | 16 | 16 |
| left | 2 | `left_step_b` | 32 | 16 | 16 | 16 |
| right | 0 | `right_step_a` | 0 | 32 | 16 | 16 |
| right | 1 | `right_idle` | 16 | 32 | 16 | 16 |
| right | 2 | `right_step_b` | 32 | 32 | 16 | 16 |
| up | 0 | `up_step_a` | 0 | 48 | 16 | 16 |
| up | 1 | `up_idle` | 16 | 48 | 16 | 16 |
| up | 2 | `up_step_b` | 32 | 48 | 16 | 16 |

通用公式（方向行 `dir`：down=0, left=1, right=2, up=3；帧列 `frame`：0..2）：

```text
x = frame * 16
y = dir * 16
w = 16
h = 16
```

## 复制用 JSON

```json
{
  "path": "res://assets/sprites/characters/blue_robe_mage_16px_walk_sheet.png",
  "cell": 16,
  "columns": ["step_a", "idle", "step_b"],
  "rows": ["down", "left", "right", "up"],
  "frames": {
    "down_step_a":  {"x": 0,  "y": 0,  "w": 16, "h": 16},
    "down_idle":    {"x": 16, "y": 0,  "w": 16, "h": 16},
    "down_step_b":  {"x": 32, "y": 0,  "w": 16, "h": 16},
    "left_step_a":  {"x": 0,  "y": 16, "w": 16, "h": 16},
    "left_idle":    {"x": 16, "y": 16, "w": 16, "h": 16},
    "left_step_b":  {"x": 32, "y": 16, "w": 16, "h": 16},
    "right_step_a": {"x": 0,  "y": 32, "w": 16, "h": 16},
    "right_idle":   {"x": 16, "y": 32, "w": 16, "h": 16},
    "right_step_b": {"x": 32, "y": 32, "w": 16, "h": 16},
    "up_step_a":    {"x": 0,  "y": 48, "w": 16, "h": 16},
    "up_idle":      {"x": 16, "y": 48, "w": 16, "h": 16},
    "up_step_b":    {"x": 32, "y": 48, "w": 16, "h": 16}
  }
}
```

## Godot 4.6 引用示例

```gdscript
const SHEET := "res://assets/sprites/characters/blue_robe_mage_16px_walk_sheet.png"
const FRAME := 16

enum Dir { DOWN, LEFT, RIGHT, UP }

func frame_rect(dir: Dir, frame: int) -> Rect2i:
    return Rect2i(frame * FRAME, int(dir) * FRAME, FRAME, FRAME)
```

导入该 PNG 时：Filter = **Nearest**，Mipmaps 关闭，不要启用 Filter 或 HDR。

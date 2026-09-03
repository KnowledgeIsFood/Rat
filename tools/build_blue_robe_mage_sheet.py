#!/usr/bin/env python3
"""Build the 16×16 four-direction walk sheet for the blue-robe mage.

Canvas: 48×64 (3 walk frames × 4 directions), PNG-32, nearest-neighbor pixels only.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.pixel_png import write_rgba_png  # noqa: E402

OUT_PNG = ROOT / "game/assets/sprites/characters/blue_robe_mage_16px_walk_sheet.png"
CELL = 16
COLS = 3
ROWS = 4

# GBA-like RGB555 palette (channels in steps of 8). Alpha is always 0 or 255.
PALETTE: dict[str, tuple[int, int, int, int]] = {
    ".": (0, 0, 0, 0),
    "k": (24, 16, 32, 255),  # outline
    "h": (144, 72, 32, 255),  # hair
    "H": (88, 48, 24, 255),  # hair dark
    "L": (192, 112, 56, 255),  # hair light
    "s": (240, 184, 136, 255),  # skin
    "S": (200, 128, 88, 255),  # skin shadow
    "e": (40, 24, 16, 255),  # eye
    "r": (56, 104, 208, 255),  # robe
    "R": (32, 64, 144, 255),  # robe dark
    "b": (88, 144, 232, 255),  # robe light
    "n": (24, 40, 96, 255),  # robe navy
    "y": (208, 160, 48, 255),  # gold clasp / ferrule
    "t": (168, 104, 48, 255),  # staff wood
    "T": (104, 64, 32, 255),  # staff dark
    "p": (208, 144, 80, 255),  # staff light
    "o": (64, 216, 224, 255),  # gem
    "O": (24, 120, 160, 255),  # gem dark
    "u": (224, 248, 248, 255),  # gem highlight
    "f": (72, 48, 32, 255),  # shoe
    "F": (120, 80, 56, 255),  # shoe light
}

TRANSPARENT = PALETTE["."]
ROW_NAMES = ("down", "left", "right", "up")
COL_NAMES = ("step_a", "idle", "step_b")


def px(*parts: tuple[int, str]) -> str:
    """Place color runs onto a 16-wide transparent row."""
    line = ["."] * CELL
    for x, run in parts:
        for i, ch in enumerate(run):
            j = x + i
            if not 0 <= j < CELL:
                raise ValueError(f"pixel x={j} out of range in {run!r} at {x}")
            if ch not in PALETTE:
                raise ValueError(f"unknown color {ch!r}")
            line[j] = ch
    return "".join(line)


def empty() -> str:
    return "." * CELL


# --- down (front): staff in the right hand, gold clasp at the collar ---
_DOWN_HEAD = [
    empty(),
    px((4, "kkkkkk"), (12, "uO")),
    px((3, "kLLLLLLk"), (12, "Oo")),
    px((3, "kLsssLHk"), (12, "tT")),
    px((3, "ksessesk"), (12, "t")),
    px((3, "kssSSssk"), (12, "t")),
    px((4, "kssssk"), (11, "y"), (12, "t")),
]

_DOWN_SHOULDERS = [
    px((3, "kbbbbbbk"), (12, "t")),
    px((2, "kbrrrrrrbk"), (12, "t")),
]
_DOWN_LOWER = [
    px((2, "kRrrrrrrRk"), (12, "t")),
    px((2, "kRnrrrrnRk"), (12, "t")),
]


def _down(step: str) -> list[str]:
    # Right hand stays on the staff (x=11). Left hand swings with the stride.
    if step == "idle":
        hands = px((2, "krrsrrrrss"), (12, "t"))
        hem = px((3, "kRrrrrRk"), (12, "t"))
        ankles = px((4, "kf"), (8, "fk"), (12, "t"))
        shoes = px((4, "FF"), (8, "FF"))
    elif step == "step_a":  # viewer's left foot forward
        hands = px((2, "krsrrrrrss"), (12, "t"))
        hem = px((2, "kRrrrRk"), (12, "t"))
        ankles = px((3, "kf"), (8, "fk"), (12, "t"))
        shoes = px((3, "FF"), (8, "F"))
    else:  # step_b: viewer's right foot forward
        hands = px((2, "krrrsrrrss"), (12, "t"))
        hem = px((4, "kRrrrRk"), (12, "t"))
        ankles = px((5, "kf"), (9, "fk"), (12, "t"))
        shoes = px((5, "F"), (9, "FF"))
    return _DOWN_HEAD + _DOWN_SHOULDERS + [hands] + _DOWN_LOWER + [hem, ankles, shoes, empty()]


# --- left: staff planted in front, hair mass at the back of the head ---
_LEFT_HEAD = [
    empty(),
    px((2, "uO"), (6, "kkkkkk")),
    px((2, "Oo"), (5, "kLLLLHk")),
    px((2, "tT"), (5, "ksssHHk")),
    px((2, "t"), (5, "ksesHHk")),
    px((2, "t"), (6, "kssSkk")),
    px((2, "t"), (6, "kbbbbk")),
]

_LEFT_TORSO = [
    px((2, "t"), (5, "kbrrrbk")),
    px((2, "ty"), (4, "s"), (5, "krrrrk")),  # ferrule, hand, then robe
    px((2, "t"), (5, "krrrrRk")),
    px((2, "t"), (6, "krrrRk")),
    px((2, "t"), (6, "knrnk")),
]


def _left(step: str) -> list[str]:
    if step == "idle":
        hem = px((2, "t"), (7, "krrk"))
        ankles = px((7, "fk"), (10, "f"))
        shoes = px((6, "FF"), (9, "FF"))
    elif step == "step_a":  # leading foot west
        hem = px((2, "t"), (6, "krrk"))
        ankles = px((5, "fk"), (9, "f"))
        shoes = px((4, "FF"), (9, "F"))
    else:  # trailing foot east
        hem = px((2, "t"), (8, "krrk"))
        ankles = px((8, "fk"), (11, "f"))
        shoes = px((7, "F"), (10, "FF"))
    return _LEFT_HEAD + _LEFT_TORSO + [hem, ankles, shoes, empty()]


# --- up (back): no face, hair volume, staff stays in the right hand ---
_UP_HEAD = [
    empty(),
    px((4, "kkkkkk"), (12, "uO")),
    px((3, "kHLLhhHk"), (12, "Oo")),
    px((3, "kHHHHHHHk"), (12, "tT")),
    px((3, "kHHHHHHHk"), (12, "t")),
    px((3, "kHHhhHHk"), (12, "t")),
    px((4, "kkkkkk"), (12, "t")),
]


def _up(step: str) -> list[str]:
    torso = [
        px((3, "kbbbbbbk"), (12, "t")),
        px((2, "kbrrrrrrbk"), (12, "t")),
        px((2, "krrrrrrrrk"), (12, "t")),
        px((2, "kRrrrrrrRk"), (12, "t")),
        px((2, "kRnnrrnnRk"), (12, "t")),
    ]
    if step == "idle":
        hem = px((3, "kRrrrrRk"), (12, "t"))
        ankles = px((4, "kf"), (8, "fk"), (12, "t"))
        shoes = px((4, "FF"), (8, "FF"))
    elif step == "step_a":
        hem = px((2, "kRrrrRk"), (12, "t"))
        ankles = px((3, "kf"), (8, "fk"), (12, "t"))
        shoes = px((3, "FF"), (8, "F"))
    else:
        hem = px((4, "kRrrrRk"), (12, "t"))
        ankles = px((5, "kf"), (9, "fk"), (12, "t"))
        shoes = px((5, "F"), (9, "FF"))
    return _UP_HEAD + torso + [hem, ankles, shoes, empty()]


def mirror_frame(lines: list[str]) -> list[str]:
    return [line[::-1] for line in lines]


def frame_lines(direction: str, column: str) -> list[str]:
    if direction == "down":
        return _down(column)
    if direction == "left":
        return _left(column)
    if direction == "right":
        return mirror_frame(_left(column))
    if direction == "up":
        return _up(column)
    raise KeyError(direction)


def parse_frame(lines: list[str]) -> list[list[tuple[int, int, int, int]]]:
    if len(lines) != CELL:
        raise ValueError(f"frame must have {CELL} rows, got {len(lines)}")
    pixels: list[list[tuple[int, int, int, int]]] = []
    for y, line in enumerate(lines):
        if len(line) != CELL:
            raise ValueError(f"row {y} length {len(line)} != {CELL}: {line!r}")
        pixels.append([PALETTE[ch] for ch in line])
    return pixels


def build_sheet() -> list[list[tuple[int, int, int, int]]]:
    sheet = [[TRANSPARENT for _ in range(CELL * COLS)] for _ in range(CELL * ROWS)]
    for row_i, direction in enumerate(ROW_NAMES):
        for col_i, column in enumerate(COL_NAMES):
            frame = parse_frame(frame_lines(direction, column))
            ox, oy = col_i * CELL, row_i * CELL
            for y in range(CELL):
                for x in range(CELL):
                    sheet[oy + y][ox + x] = frame[y][x]
    return sheet


def cell_border_ok(frame: list[list[tuple[int, int, int, int]]]) -> bool:
    last = CELL - 1
    for i in range(CELL):
        if frame[0][i][3] != 0 or frame[last][i][3] != 0:
            return False
        if frame[i][0][3] != 0 or frame[i][last][3] != 0:
            return False
    return True


def assert_sheet_rules(sheet: list[list[tuple[int, int, int, int]]]) -> None:
    height, width = len(sheet), len(sheet[0])
    if (width, height) != (CELL * COLS, CELL * ROWS):
        raise ValueError(f"sheet size {width}x{height}")
    for row_i, direction in enumerate(ROW_NAMES):
        for col_i, column in enumerate(COL_NAMES):
            ox, oy = col_i * CELL, row_i * CELL
            frame = [row[ox : ox + CELL] for row in sheet[oy : oy + CELL]]
            if not cell_border_ok(frame):
                raise ValueError(f"{direction}/{column} touches the 16px cell border")
            alphas = {px[3] for row in frame for px in row}
            if alphas - {0, 255}:
                raise ValueError(f"{direction}/{column} has intermediate alpha")


def main() -> None:
    sheet = build_sheet()
    assert_sheet_rules(sheet)
    write_rgba_png(OUT_PNG, CELL * COLS, CELL * ROWS, sheet)
    print(f"wrote {OUT_PNG} ({CELL * COLS}x{CELL * ROWS})")


if __name__ == "__main__":
    main()

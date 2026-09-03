from __future__ import annotations

import unittest
from pathlib import Path

from tools.build_blue_robe_mage_sheet import (
    CELL,
    COLS,
    OUT_PNG,
    PALETTE,
    ROWS,
    ROW_NAMES,
    assert_sheet_rules,
    build_sheet,
    frame_lines,
)
from tools.pixel_png import read_rgba_png


class BlueRobeMageSheetTest(unittest.TestCase):
    def test_committed_png_matches_builder_and_grid_rules(self) -> None:
        self.assertTrue(OUT_PNG.is_file(), f"missing {OUT_PNG}")
        width, height, pixels = read_rgba_png(OUT_PNG)
        self.assertEqual((width, height), (CELL * COLS, CELL * ROWS))

        generated = build_sheet()
        assert_sheet_rules(generated)
        self.assertEqual(pixels, generated)

        palette = set(PALETTE.values())
        used = {px for row in pixels for px in row}
        self.assertTrue(used <= palette)
        self.assertEqual({a for _, _, _, a in used}, {0, 255})

        last = CELL - 1
        for row_i, direction in enumerate(ROW_NAMES):
            for col_i in range(COLS):
                ox, oy = col_i * CELL, row_i * CELL
                opaque = 0
                for y in range(CELL):
                    for x in range(CELL):
                        px = pixels[oy + y][ox + x]
                        if y in (0, last) or x in (0, last):
                            self.assertEqual(px[3], 0, f"{direction} col{col_i} border")
                        if px[3] == 255:
                            opaque += 1
                self.assertGreater(opaque, 20, f"{direction} col{col_i} looks empty")

    def test_each_frame_is_16_by_16_ascii(self) -> None:
        for direction in ROW_NAMES:
            for column in ("step_a", "idle", "step_b"):
                lines = frame_lines(direction, column)
                self.assertEqual(len(lines), CELL)
                self.assertTrue(all(len(line) == CELL for line in lines))


if __name__ == "__main__":
    unittest.main()

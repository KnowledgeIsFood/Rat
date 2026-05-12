# 异兽数据目录

- **`creatures_master.csv`**：唯一建议手编的主表（UTF-8 BOM，可用 Excel 打开）。含 **奇禽 / 异兽 / 鳞介 / 草木** 等，见列 **`kind_zh`** 与 `docs/shanhaijing/表格维护说明.md`。
- **`chapters/*.json`**：由 `python3 tools/emit_shanhaijing_chapters.py` 从 CSV 生成，勿手改。

详见 `docs/shanhaijing/表格维护说明.md`。

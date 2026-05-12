extends Node

const CATALOG_PATH := "res://data/creatures_catalog.json"

@onready var count_label: Label = $UILayer/RootControl/VBox/CountLabel


func _ready() -> void:
	if not FileAccess.file_exists(CATALOG_PATH):
		count_label.text = "未找到 %s — 请先在仓库根目录运行：python3 tools/render_shanhaijing_docs.py" % CATALOG_PATH
		return
	var text := FileAccess.get_file_as_string(CATALOG_PATH)
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		count_label.text = "catalog JSON 解析失败"
		return
	var entries: Array = parsed.get("entries", parsed.get("creatures", []))
	var kc: Variant = parsed.get("kind_counts", {})
	var ts: Variant = parsed.get("theme_scope", {})
	var theme_line := ""
	if typeof(ts) == TYPE_DICTIONARY and (ts as Dictionary).has("entry_count_in_theme"):
		var d: Dictionary = ts as Dictionary
		theme_line = "五经内：%s / 全表：%s" % [str(d.get("entry_count_in_theme", "?")), str(d.get("entry_count_total", "?"))]
	var kind_line := ""
	if typeof(kc) == TYPE_DICTIONARY:
		var bits: Array = []
		for k in (kc as Dictionary).keys():
			bits.append("%s:%s" % [str(k), str((kc as Dictionary)[k])])
		bits.sort()
		for i in range(bits.size()):
			if i > 0:
				kind_line += "；"
			kind_line += str(bits[i])
	count_label.text = "载入条目：%s\n类目：%s\n%s" % [
		str(entries.size()),
		kind_line if kind_line != "" else "—",
		theme_line if theme_line != "" else "",
	]

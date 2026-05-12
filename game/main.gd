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
	var creatures: Array = parsed.get("creatures", [])
	count_label.text = "载入异兽条目数：%d（%s）" % [
		creatures.size(),
		str(parsed.get("generated_note", "")),
	]

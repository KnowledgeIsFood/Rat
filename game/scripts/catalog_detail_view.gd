extends RefCounted


func build_detail(entries: Array) -> String:
	if entries.is_empty():
		return "暂无条目详情"

	var first: Variant = entries[0]
	if typeof(first) != TYPE_DICTIONARY:
		return "首条条目格式异常"

	var creature: Dictionary = first as Dictionary
	return "%s（%s）\n%s · %s · %s\n%s\n美术：%s" % [
		str(creature.get("name_zh", "未命名")),
		str(creature.get("id", "?")),
		str(creature.get("kind_zh", "?")),
		str(creature.get("jing_zh", "?")),
		str(creature.get("mountain_zh", "?")),
		str(creature.get("literature_appearance_zh", "")),
		str(creature.get("artistic_portrait_note_zh", "")),
	]

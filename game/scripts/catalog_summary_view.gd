extends RefCounted


func build_summary(catalog: Dictionary, entries: Array) -> String:
	var kind_line := _format_kind_counts(catalog.get("kind_counts", {}))
	var theme_line := _format_theme_scope(catalog.get("theme_scope", {}))
	return "载入条目：%s\n类目：%s\n%s" % [
		str(entries.size()),
		kind_line if kind_line != "" else "—",
		theme_line if theme_line != "" else "",
	]


func _format_kind_counts(kind_counts: Variant) -> String:
	if typeof(kind_counts) != TYPE_DICTIONARY:
		return ""

	var bits: Array = []
	for k in (kind_counts as Dictionary).keys():
		bits.append("%s:%s" % [str(k), str((kind_counts as Dictionary)[k])])
	bits.sort()
	return "；".join(bits)


func _format_theme_scope(theme_scope: Variant) -> String:
	if typeof(theme_scope) != TYPE_DICTIONARY:
		return ""

	var scope: Dictionary = theme_scope as Dictionary
	if not scope.has("entry_count_in_theme"):
		return ""

	return "五经内：%s / 全表：%s" % [
		str(scope.get("entry_count_in_theme", "?")),
		str(scope.get("entry_count_total", "?")),
	]

extends RefCounted

const EXPECTED_SCHEMA := "rat.shanhaijing.catalog.v2"


func load_catalog(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {
			"ok": false,
			"error": "未找到 %s — 请先在仓库根目录运行：python3 tools/render_shanhaijing_docs.py" % path,
		}

	var text := FileAccess.get_file_as_string(path)
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		return {"ok": false, "error": "catalog JSON 解析失败"}

	var catalog: Dictionary = parsed as Dictionary
	var schema := str(catalog.get("schema", ""))
	if schema != EXPECTED_SCHEMA:
		return {"ok": false, "error": "catalog schema 不匹配：%s" % schema}

	var entries: Variant = catalog.get("entries", catalog.get("creatures", []))
	if typeof(entries) != TYPE_ARRAY:
		return {"ok": false, "error": "catalog entries 字段格式异常"}

	return {
		"ok": true,
		"catalog": catalog,
		"entries": entries,
	}

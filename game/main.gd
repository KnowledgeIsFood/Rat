extends Node

const CATALOG_PATH := "res://data/creatures_catalog.json"
const CreatureCatalogLoader := preload("res://scripts/creature_catalog_loader.gd")
const CatalogSummaryView := preload("res://scripts/catalog_summary_view.gd")
const CatalogDetailView := preload("res://scripts/catalog_detail_view.gd")

@onready var count_label: Label = $UILayer/RootControl/VBox/CountLabel
@onready var detail_label: Label = $UILayer/RootControl/VBox/DetailLabel


func _ready() -> void:
	var loader := CreatureCatalogLoader.new()
	var result: Dictionary = loader.load_catalog(CATALOG_PATH)
	if not bool(result.get("ok", false)):
		count_label.text = str(result.get("error", "catalog 载入失败"))
		detail_label.text = ""
		return

	var catalog: Dictionary = result["catalog"] as Dictionary
	var entries: Array = result["entries"] as Array
	count_label.text = CatalogSummaryView.new().build_summary(catalog, entries)
	detail_label.text = CatalogDetailView.new().build_detail(entries)

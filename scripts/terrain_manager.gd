extends Node2D

class_name TerrainManager

@export var speed: float = 200
@export var terrain_width: int = 1152
@onready var terrain_manager: Node = $"."
var last_terrain_used = null

enum TerrainType {Start, Terrain1, Terrain2, Terrain3, Terrain4, Terrain5}

var terrain_scenes := {
	TerrainType.Start: preload("res://scenes/terrains/Start.tscn"),
	TerrainType.Terrain1: preload("res://scenes/terrains/Terrain1.tscn"),
	TerrainType.Terrain2: preload("res://scenes/terrains/Terrain2.tscn"),
	TerrainType.Terrain3: preload("res://scenes/terrains/Terrain3.tscn"),
	TerrainType.Terrain4: preload("res://scenes/terrains/Terrain4.tscn"),
	TerrainType.Terrain5: preload("res://scenes/terrains/Terrain5.tscn")
}

var current_terrain_index := 0
var start_terrain_loaded := false

func _ready() -> void:
	randomize() #for randi to generate random result each run
	initialize_terrain() # generate the first two terrains

func _physics_process(delta: float) -> void:     
	scroll_terrain(delta)

func initialize_terrain() -> void:
	load_terrain(0, 0)
	load_terrain(terrain_width, 0)

func scroll_terrain(delta: float) -> void:
	for area in terrain_manager.get_children():
		area.position.x -= speed * delta
		if area.position.x < -terrain_width:
			load_terrain(area.position.x + terrain_width * 2 - 10, 0)
			area.queue_free()


func load_terrain(x, y):
	if not start_terrain_loaded:
		var scene = terrain_scenes[TerrainType.Start].instantiate()
		scene.position = Vector2(x, y)
		terrain_manager.add_child(scene)
		start_terrain_loaded = true
		last_terrain_used = null  # No previous terrain yet
	else:
		var terrain_types = [TerrainType.Terrain1, TerrainType.Terrain2, TerrainType.Terrain3, TerrainType.Terrain4, TerrainType.Terrain5 ]
		
		# Remove the last used terrain from available options
		if last_terrain_used != null:
			terrain_types.erase(last_terrain_used)
		
		# Randomly select from remaining terrains
		var terrain_type = terrain_types[randi() % terrain_types.size()]
		
		# Store this terrain as the last used
		last_terrain_used = terrain_type
		
		# Instantiate the selected terrain
		var scene = terrain_scenes[terrain_type].instantiate()
		scene.position = Vector2(x, y)
		terrain_manager.add_child(scene)

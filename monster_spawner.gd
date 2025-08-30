extends Node2D

class_name MonsterSpawner

@export var terrain_manager: TerrainManager
@onready var spawn_marker: Marker2D = $Marker2D
var monster_count = 0
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func create_monster():
	var monster: Monster = preload("res://scenes/monsters/recyclable_monster.tscn").instantiate()

	add_child(monster)
	monster.position = spawn_marker.position   
	monster.terrain_manager = terrain_manager

	anim.play("idle")


func _ready() -> void:
	create_monster()

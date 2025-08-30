extends Node2D

class_name Terrain

@onready var trash_spawns: Node2D = $TrashSpawns
var max_markers: int = 0
@export var trash_bin_spawn: Marker2D
@export var monster_spawn: Marker2D

func _ready() -> void:
	max_markers = trash_spawns.get_child_count()

	if Game.trash_bin_countdown == 0:
		spawn_trash_bin()
		Game.reset_trash_bin_countdown()
	else:
		spawn_trashes()
		Game.decrease_trash_bin_countdown()
	spawn_monster_spawner()
	
func spawn_trashes():
	if max_markers == 0:
		return
	var chosen_spawners = range(max_markers)
	chosen_spawners.shuffle()
	chosen_spawners = chosen_spawners.slice(0, randi_range(1, max_markers - 2))
	print(name, " ", chosen_spawners)
	for i in chosen_spawners:
		var trash: Trash = preload("res://scenes/trash.tscn").instantiate()

		var randtype = randi_range(0, Utils.TrashType.size())
		trash.type = randtype as Utils.TrashType
		trash_spawns.get_children()[i].add_child(trash)

func spawn_trash_bin():
	if max_markers == 0:
		return
	if not trash_bin_spawn:
		printerr("No trash bin spawn set")
	var trash_bin: TrashBin = preload("res://scenes/TrashBin.tscn").instantiate()

	var randtype = randi_range(0, Utils.TrashType.size())
	trash_bin.type = randtype as Utils.TrashType


	trash_bin_spawn.add_child(trash_bin)

func spawn_monster_spawner():
	if not monster_spawn:
		printerr("No monster spawn set")
		return
	var spawner: MonsterSpawner = preload("res://scenes/monster_spawner.tscn").instantiate()
	spawner.terrain_manager = get_parent() as TerrainManager
	monster_spawn.add_child(spawner)

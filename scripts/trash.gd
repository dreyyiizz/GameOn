extends Node2D

class_name Trash

@export var type: Utils.TrashType = Utils.TrashType.Recyclable
@onready var trash_label: Label = $Label
@onready var trash_texture: Sprite2D = $Area/Sprite2D
var trash_item_resource: TrashResource
var float_amplitude := 5.0 # pixels
var float_speed := 0.7 # oscillations per second (slower)
var float_time := 0.0
var base_position := Vector2.ZERO

func _ready() -> void:
	base_position = position
	load_trash()

func _process(delta):
	float_time += delta
	position.y = base_position.y + sin(float_time * float_speed * TAU) * float_amplitude

func remove():
	queue_free()

func load_trash() -> void:
	trash_item_resource = Utils.get_random_trash_item()
	var texture_path = trash_item_resource.get_trash_texture_path()

	type = trash_item_resource.trash_type
	
	var texture = load(texture_path) 
	trash_texture.texture = texture
	trash_label.text = "%s: %s" % [Utils.get_enum_name(Utils.TrashType, type), trash_item_resource.trash_name]

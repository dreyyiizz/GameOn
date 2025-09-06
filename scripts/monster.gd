extends Node2D

class_name Monster

@export var type: Utils.TrashType
@onready var player_collision_area: CollisionObject2D = get_node_or_null("PlayerCollisionArea")
@export var anim : AnimatedSprite2D

func _ready() -> void:
	await anim.animation_finished
	anim.play("idle")
	
	#if has_node("Asset"):
		#var asset := $Asset
		#
		#if asset is Sprite2D:
			#var enum_name := Utils.get_enum_name(Utils.TrashType, type)
			#var texture_path := "res://scenes/monsters/%s.tscn" % enum_name
			#if ResourceLoader.exists(texture_path):
				#(asset as Sprite2D).texture = load(texture_path + ".tscn")

				

	# React to player type changes like TrashBin
	if Game.changed_trash_type.is_connected(change_player_collision) == false:
		Game.changed_trash_type.connect(change_player_collision)

	# Hook collision: if PlayerCollisionArea is an Area2D, listen for overlaps

func change_player_collision(trash_type: Utils.TrashType) -> void:
	if player_collision_area == null:
		return
	# Enable collision layer 4 only when monster type differs from player's current type
	if player_collision_area.has_method("set_collision_layer_value"):
		player_collision_area.set_collision_layer_value(4, type != trash_type)
	

extends RigidBody2D
class_name Monster

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D


func _ready() -> void:
	add_to_group("Monster")

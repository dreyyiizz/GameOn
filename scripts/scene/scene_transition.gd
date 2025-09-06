extends CanvasLayer


@onready var scene_trans: AnimationPlayer = $SceneAnimation
var last_position
@onready var player_anim = $PlayerAnim

func _ready() -> void:
	player_anim.hide()
	$Start/StaticBody2D/CollisionShape2D.disabled = true
	
func change_scene(target: String) -> void:
	player_anim.show()
	scene_trans.play("fade_in")
	await scene_trans.animation_finished
	SceneHandler.last_background_scroll_offset = $Parallax/Background.scroll_offset
	SceneHandler.last_midground_scroll_offset = $Parallax/Midground.scroll_offset
	SceneHandler.last_foreground_scroll_offset = $Parallax/Foreground.scroll_offset
	get_tree().change_scene_to_file(target)
	scene_trans.play("fade_out")

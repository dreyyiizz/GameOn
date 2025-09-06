extends Node2D

func _ready() -> void:
	$Background/Background.scroll_offset = SceneHandler.last_background_scroll_offset
	$Background/Midground.scroll_offset = SceneHandler.last_midground_scroll_offset
	$Background/Foreground.scroll_offset = SceneHandler.last_foreground_scroll_offset

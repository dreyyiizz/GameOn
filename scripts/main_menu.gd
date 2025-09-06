extends Control

@onready var game_title = $ParallaxBackground/Misc/GameTitle
@onready var buttons_player = $Buttons/ButtonsPlayer
@onready var props_play = $PropsPlayer
@onready var cam_pos = $Camera2D
@onready var player = $ParallaxBackground/Player
@onready var start_button = $Buttons/StartButton
@onready var tutorial_button = $Buttons/TutorialButton
@onready var exit_button = $Buttons/ExitButton


func _ready():
	is_intro_scene()
	cam_pos.make_current()
	
func _on_start_button_pressed() -> void:
	start_game()

func _on_exit_button_pressed() -> void:
	buttons_player.play("exit_press")
	await buttons_player.animation_finished
	quit_game()

func is_intro_scene():
	if SceneHandler.last_scene_path == "res://scenes/intro.tscn":
		props_play.play("cam_in")
		await props_play.animation_finished
		game_title.play("text_pop")
		props_play.play('hover_button')
		await game_title.animation_finished
		game_title.play("default")
	else:
		props_play.play('hover_button')
		cam_pos.position = Vector2(-3, 0)

func start_game():
	tutorial_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	exit_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	start_button.mouse_filter = Control.MOUSE_FILTER_IGNORE
	SceneHandler.last_scene_path = get_tree().current_scene.scene_file_path
	Game.reset_stats()
	player.hide()
	props_play.play("fade_out")
	SceneTransition.change_scene("res://scenes/Main.tscn")
	
	
func quit_game():
	get_tree().quit()

func _on_tutorial_button_pressed() -> void:
	buttons_player.play("tutorial_press")
	await buttons_player.animation_finished

func _on_tutorial_button_mouse_entered() -> void:
	$Buttons/TutorialButton/TutorialLabel.add_theme_color_override("font_color", Color.html("f07a00"))
		
func _on_tutorial_button_mouse_exited() -> void:
	$Buttons/TutorialButton/TutorialLabel.add_theme_color_override("font_color", Color.html("da6800"))

func _on_exit_button_mouse_entered() -> void:
	$Buttons/ExitButton/ExitLabel.add_theme_color_override("font_color", Color.html("f07a00"))

func _on_exit_button_mouse_exited() -> void:
	$Buttons/ExitButton/ExitLabel.add_theme_color_override("font_color", Color.html("da6800"))

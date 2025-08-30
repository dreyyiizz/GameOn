extends TextureProgressBar

class_name EnergyBar


func _ready() -> void:
	max_value = Game.MAX_ENERGY
	Game.energy_changed.connect(change_energy_value)
	change_energy_value(Game.energy)

	
	
func change_energy_value(energy: int):
	zero_energy(energy)
	value = energy

func zero_energy(energy: int):
	if energy == 0:
		Game.update_game_state.emit(Utils.GameStateType.Pause)
		Game.update_ui_state.emit( Utils.UIStateType.GameOver, Utils.GameOverReason.OutOfEnergy)

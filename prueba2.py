from pynput import keyboard as kb

def pulsa(tecla):
	print('Se ha pulsado la tecla ' + str(tecla))
	if str(tecla) == "Key.esc":
		print("SWSWW")
		return
		print("SWSWW2w")



with kb.Listener(pulsa) as escuchador:
	escuchador.join()
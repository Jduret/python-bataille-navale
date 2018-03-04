#classe qui permet de simuler un event comme lors d'un clic sur la grille
#elle permetr d'utiliser les même méthode d'attaque en graphique par clic et en automatique en aléatoire
class AutomaticEvent:
	x = None
	y = None

	def __init__(self, x, y) :
		self.x = x
		self.y = y

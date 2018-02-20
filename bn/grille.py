from bn.settings import *
#
# Classe de gestion des grilles
# pour une bataille navale par exemple on a besoin de 2 grilles : joueur et PC
#
class Grille:
	def __init__(self):
		#Les cases qui composent une grille 10*10
		self.cases = [[0]*Settings.tailleGrille]*Settings.tailleGrille
		self.bateaux = []

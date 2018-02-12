from jdev4u.settings import *
#
# Classe de gestion des grilles
# pour une bataille navale par exemple on a besoin de 2 grilles
#
class Grille:
	def __init__(self):
		self.emplacements = {}
		self.bateaux = {}
	def hasBateau(self, case):
		return case in self.emplacements
	def getBateau(self, case):
		if self.hasBateau(case):
			return self.bateaux[self.emplacements[case]] 
		else :
			return None

#
# Classe de gestion des bateau
#
class Bateau:
	def __init__(self, nom, taille):
		self.nom = nom
		self.taille = taille
		self.emplacement = []
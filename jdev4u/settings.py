import os

#Un petit  objet d'utilitaire
class Settings:
	__location__ = os.getcwd()
	window = None
	title = 'Bataille Navale'
	defaultHumainName = 'Joueur 1'
	#Devraient etre dans la classe Grille
	#nombre de cases de largeur de la grille
	tailleGrille = 10
	#taille en px d'une case
	tailleCase = 40
	#épaisseur du trait
	epaisseurTrait = 3
	#Taille du rond de placement bateau + placement touché (obligatoirement inférieur à tailleCase)
	tailleRond = tailleCase - 5
	epaisseurMarques = 5
	couleurFondGrille = 'lightseagreen'
import os

#Un petit  objet d'utilitaires
class Settings:
	__location__ = os.getcwd()
	title = 'Bataille Navale'
	defaultHumainName = 'Joueur'
	#Devraient etre dans la classe Grille
	#nombre de cases de largeur de la grille
	tailleGrille = 10
	#taille en px d'une case
	tailleCase = 30
	#épaisseur du trait
	epaisseurTrait = 3
	#Taille du rond de placement bateau + placement touché (obligatoirement inférieur à tailleCase)
	tailleRond = tailleCase - 5
	epaisseurMarques = 5
	couleurFondGrille = 'lightseagreen'
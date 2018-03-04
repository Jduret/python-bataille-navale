# Sous licence Apache-2.0

"""Classe de gestion des bateaux permettant de créer et bouger les bateaux"""

##----- Importation des Modules -----##
from bn.settings import *
#
# Classe de gestion des bateaux
#
class Bateau:
	nom = None
	taille = None
	isGraphic = True

	jeu = None
	elementGraphique = None
	pointAncrage = None
	ancrage = []
	sens = None
	
#initialisation de l'ensemble des variables nécessaires
	def __init__(self, nom, taille):
		self.nom = nom
		self.taille = int(taille)
		self.pointAncrage = None
		self.sens = 'horizontal'
		self.elementGraphique = None
		
# Fonction donnant les coordonnées de la 2eme extrémité du bateau
	def calculDimensions(self, sens):
		(c, l) = self.pointAncrage
		largeur = Settings.tailleCase*(c - 1)+Settings.tailleRond
		hauteur = Settings.tailleCase*(l - 1)+Settings.tailleRond

		if(sens == 'horizontal'):
			#taille - 1 car on a déjà mis en place une taille de 1 carreau juste au dessus
			return [largeur + ((self.taille - 1)*Settings.tailleCase), hauteur]
		else :
			#taille - 1 car on a déjà mis en place une taille de 1 carreau juste au dessus
			return [largeur,hauteur + ((self.taille - 1)*Settings.tailleCase)]

#permet de connaître l'ensemble des cases occupées par le bateau
	def listeCasesBateau(self, pointAncrage):
		(c, l) = pointAncrage
		ancrage = []
		for i in range(self.taille):
			ancrage.append(Settings.pointToCase([c, l]))

			if('horizontal' == self.sens):
				c = c + 1
			else :
				l = l + 1

		return ancrage

#avec le clic gauche:crée un bateau s'il n'existe pas, le change de place s'il existe	
	def placerAncrage(self, grille, pointAncrage):
		self.pointAncrage = pointAncrage
		if(grille.isGraphic):
			if	(None != self.elementGraphique):
				self.removeGraphique(grille)
			self.createGraphique(grille.grilleGraphique)
			self.bindMove(grille)
		self.ancrage = self.listeCasesBateau(pointAncrage)

#créé le graphisme du bateau
	def createGraphique(self, grille):
		(colonne, ligne) = self.pointAncrage
		(largeur, hauteur) = self.calculDimensions(self.sens)
		self.elementGraphique = grille.create_oval(
			Settings.tailleCase*(colonne-1)+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond,
			Settings.tailleCase*(ligne-1)+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond,
			largeur,
			hauteur,
			width = Settings.epaisseurMarques,
			outline = 'chocolate',
			fill='chocolate',
			tags = self.nom
		)

#le clic droit va permettre de changer de sens un bateau	
	def moveGraphique(self, event, grille):

		(colonne, ligne) = self.pointAncrage
		(largeur, hauteur) = self.calculDimensions(self.sens)

		grille.coords(self.elementGraphique,
			Settings.tailleCase*(colonne-1)+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond,
			Settings.tailleCase*(ligne-1)+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond,
			largeur,
			hauteur,
		)

#permet de déplacer un bateau de la grille
	def removeGraphique(self, grille):
		self.unbindMove(grille)
		grille.grilleGraphique.delete(self.elementGraphique)

#ajoute la gestion du clic sur le bateau
	def bindMove(self, grille):
		grille.grilleGraphique.tag_bind(self.nom, '<Button-3>',lambda event, grille=grille, bateau=self: grille.retournerBateau(event, bateau))

#retire la gestion du clic sur le bateau
	def unbindMove(self, grille):
		grille.grilleGraphique.tag_unbind(self.nom, '<Button-3>')

#retire une case attaquéede la liste des cases du bateau
	def attaque(self, case):
		if(case in self.ancrage):
			self.ancrage.remove(case)

#vérifie si le bateau est coulé
	def estCoule(self):
		return (len(self.ancrage) == 0)
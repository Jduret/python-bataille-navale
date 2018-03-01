from jdev4u.settings import *
#
# Classe de gestion des bateau
#
class Bateau:
	nom = None
	taille = None
	isGraphic = True

	jeu = None
	elementGraphique = None
	ancrage = []
	sens = None

	def __init__(self, nom, taille):
		self.nom = nom
		self.taille = int(taille)
		self.pointAncrage = None
		self.sens = 'horizontal'
		self.elementGraphique = None

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

	def listeCasesBateau(self, pointAncrage):
		(c, l) = pointAncrage
		ancrage = []
		for i in range(self.taille):
			ancrage.append(str(c) + str(l))

			if('horizontal' == self.sens):
				c = c + 1
			else :
				l = l + 1

		return ancrage

	def placerAncrage(self, grille, pointAncrage):
		self.pointAncrage = pointAncrage
		if(grille.isGraphic):
			if	(None != self.elementGraphique):
				self.removeGraphique(grille)
			self.createGraphique(grille.grilleGraphique)
			self.bindMove(grille)
		self.ancrage = self.listeCasesBateau(pointAncrage)

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

	def moveGraphique(self, event, grille):

		(colonne, ligne) = self.pointAncrage
		(largeur, hauteur) = self.calculDimensions(self.sens)

		grille.coords(self.elementGraphique,
			Settings.tailleCase*(colonne-1)+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond,
			Settings.tailleCase*(ligne-1)+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond,
			largeur,
			hauteur,
		)

	def removeGraphique(self, grille):
		self.unbindMove(grille)
		grille.grilleGraphique.delete(self.elementGraphique)

	def bindMove(self, grille):
		grille.grilleGraphique.tag_bind(self.nom, '<Button-3>',lambda event, grille=grille, bateau=self: grille.retournerBateau(event, bateau))

	def unbindMove(self, grille):
		grille.grilleGraphique.tag_unbind(self.nom, '<Button-3>')

	def attaque(self, case):
		if(case in self.ancrage):
			self.ancrage.remove(case)
	def estCoule(self):
		return (len(self.ancrage) == 0)





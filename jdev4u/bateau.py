from jdev4u.settings import *
#
# Classe de gestion des bateau
#
class Bateau:
	nom = None
	taille = None
	
	jeu = None	
	elementGraphique = None
	ancrage = []

	def __init__(self, nom, taille, Jeu):
		self.nom = nom
		self.taille = int(taille)
		self.pointAncrage = None
		self.sens = 'horizontal'		
		self.elementGraphique = None
		self.jeu = Jeu
	
	def calculDimensions(self, sens):
		(l, c) = self.pointAncrage
		largeur = Settings.tailleCase*c+Settings.tailleRond
		hauteur = Settings.tailleCase*l+Settings.tailleRond
		
		if(sens == 'horizontal'):
			#taille - 1 car on a déjà mis en place une taille de 1 carreau juste au dessus
			return [largeur + ((self.taille - 1)*Settings.tailleCase), hauteur]
		else :
			#taille - 1 car on a déjà mis en place une taille de 1 carreau juste au dessus
			return [largeur,hauteur + ((self.taille - 1)*Settings.tailleCase)]
	
	def updateCasesJeu(self, pointAncrage):
		(l, c) = pointAncrage
		l = l + 1
		c = c + 1
		self.ancrage = []
		self.ancrage.append(str(l) + str(c))
		for i in range(self.taille - 1):
			if('horizontal' == self.sens):
				l = l + 1
			else :
				c = c + 1
			
			self.ancrage.append(str(l) + str(c))
		
	
	def placerAncrage(self, grille, pointAncrage):
		self.pointAncrage = pointAncrage
		if	(None != self.elementGraphique):
			self.removeGraphique(grille)
		self.createGraphique(grille)
		self.bindMove(grille)
		self.updateCasesJeu(pointAncrage)
		
	def createGraphique(self, grille):
		(ligne, colonne) = self.pointAncrage
		(largeur, hauteur) = self.calculDimensions(self.sens)
		self.elementGraphique = grille.create_oval(
			Settings.tailleCase*colonne+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
			Settings.tailleCase*ligne+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond, 
			largeur, 
			hauteur, 
			width = Settings.epaisseurMarques, 
			outline = 'chocolate', 
			fill='chocolate',
			tags = self.nom
		)
	
	def moveGraphique(self, event, grille):
		if('horizontal' == self.sens):
			self.sens = 'vertical'
		else:
			self.sens = 'horizontal'
			
		(ligne, colonne) = self.pointAncrage
		(largeur, hauteur) = self.calculDimensions(self.sens)
		
		grille.coords(self.elementGraphique, 
			Settings.tailleCase*colonne+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
			Settings.tailleCase*ligne+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond, 
			largeur, 
			hauteur, 
		)
		
	def removeGraphique(self, grille):
		self.unbindMove(grille)
		grille.delete(self.elementGraphique)
		
	def bindMove(self, grille):
		grille.tag_bind(self.nom, '<Button-3>',lambda event, element=grille: self.moveGraphique(event, element))
		
	def unbindMove(self, grille):
		grille.tag_unbind(self.nom, '<Button-3>')
		
	
		
	

from jdev4u.settings import *
#
# Classe de gestion des bateau
#
class Bateau:
	nom = None
	taille = None
	
	elementGraphique = None

	def __init__(self, nom, taille, Jeu):
		self.nom = nom
		self.taille = taille
		self.pointAncrage = None
		self.sens = 'horizontal'
	
	def calculDimensions(self, sens):
		(c, l) = self.pointAncrage
		largeur = Settings.tailleCase*c+Settings.tailleRond
		hauteur = Settings.tailleCase*l+Settings.tailleRond
		
		if(sens == 'horizontal'):
			return [largeur + (self.taille*Settings.tailleCase), hauteur]
		else :
			return [largeur,hauteur + (self.taille*Settings.tailleCase)]
	
	def placerAncrage(self, grille, pointAncrage):
		self.pointAncrage = pointAncrage
		if	(None != self.elementGraphique):
			self.removeGraphique(grille)
		self.createGraphique(grille)
		self.bindMove(grille)
		
	def createGraphique(self, grille):
		(colonne, ligne) = self.pointAncrage
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
			
		(colonne, ligne) = self.pointAncrage
		(largeur, hauteur) = self.calculDimensions(self.sens)
		
		grille.coords(self.elementGraphique, 
			Settings.tailleCase*colonne+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
			Settings.tailleCase*ligne+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond, 
			largeur, 
			hauteur, 
		)
		
	def removeGraphique(self, grille):
		grille.delete(self.elementGraphique)
		
	def bindMove(self, grille):
		grille.tag_bind(self.nom, '<Button-3>',lambda event, element=grille: self.moveGraphique(event, element))
		
	def unbindMove(self):
		grille.tag_unbind(self.nom, '<Button-3>')
		
	
		
	

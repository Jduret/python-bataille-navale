from bn.settings import *
#
# Classe de gestion des bateaux
#
class Bateau:
	"""Classe permettant de créer l'objet bateau"""

#initialisation de l'ensemble des variables nécessaires	
	def __init__(self, nom, taille, Jeu):
		self.nom = nom
		self.taille = int(taille)
		self.pointAncrage = None
		self.sens = 'horizontal'		
		self.elementGraphique = None
		self.jeu = Jeu

# Fonction donnant les coordonnées de la 2eme extrémité du bateau
	def calculDimensions(self, sens):
		(c, l) = self.pointAncrage
		largeur = Settings.tailleCase*c+Settings.tailleRond
		hauteur = Settings.tailleCase*l+Settings.tailleRond
		
		if(sens == 'horizontal'):
			#taille - 1 car on a déjà mis en place une taille de 1 carreau juste au dessus
			return [largeur + ((self.taille - 1)*Settings.tailleCase), hauteur]
		else :
			#taille - 1 car on a déjà mis en place une taille de 1 carreau juste au dessus
			return [largeur,hauteur + ((self.taille - 1)*Settings.tailleCase)]

#avec le clic gauche:crée un bateau s'il n'existe pas, le change de place s'il existe	
	def placerAncrage(self, grille, pointAncrage):
		self.pointAncrage = pointAncrage
		if	self.elementGraphique!=None:
			self.removeGraphique(grille)
		self.createGraphique(grille)
		self.bindMove(grille)

#créé le graphisme du bateau
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

#le clic droit va permettre de changer de sens un bateau	
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
		
#permet de déplacer un bateau de la grille		
	def removeGraphique(self, grille):
		self.unbindMove(grille)
		grille.delete(self.elementGraphique)

#ajoute la gestion du clic sur le bateau		
	def bindMove(self, grille):
		grille.tag_bind(self.nom, '<Button-3>',lambda event, element=grille: self.moveGraphique(event, element))

#retire la gestion du clic sur le bateau		
	def unbindMove(self, grille):
		grille.tag_unbind(self.nom, '<Button-3>')
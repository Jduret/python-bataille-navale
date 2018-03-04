# Sous licence Apache-2.0

from bn.settings import *
from tkinter import *

#
# Classe de gestion des grilles
# pour une bataille navale par exemple on a besoin de 2 grilles
#
class Grille:
	bateaux = {}
	emplacements = {}
	emplacementsAttaque = []

	grilleGraphique = None
	isGraphic = True
	figuresAttaque = []

#initialisation des variables 
	def __init__(self, joueurType):
		self.emplacements = {}
		self.bateaux = {}

#permet de vérifier si une case contient un bateau
	def hasBateau(self, case):
		return case in self.emplacements

# permet de connaître où sont situés les bateaux dans la grille
	def getBateau(self, case):
		if self.hasBateau(case):
			return self.bateaux[self.emplacements[case]]
		else :
			return None
		

	def placerBateau(self, bateau, pointAncrage):
		if(False == self.isIn(bateau, pointAncrage) or True == self.seCroise(bateau, pointAncrage)):
			return False
		if(bateau.nom in self.bateaux.keys()):
			for emplacement in dict(self.emplacements):
				if(bateau.nom == self.emplacements[emplacement]):
					del self.emplacements[emplacement]
		bateau.placerAncrage(self, pointAncrage)
		self.bateaux[bateau.nom] = bateau
		for case in bateau.ancrage:
			self.emplacements[case] = bateau.nom
		return True

	def retournerBateau(self, event, bateau):
		currentSens = bateau.sens
		newSens = 'horizontal' if('vertical' == currentSens) else 'vertical'
		pointAncrage = Settings.caseToPoint(bateau.ancrage[0])
		#Si l'on veut modifier aussi le point d'ancrage lors d'une rotation
		#pointAncrage = Settings.eventToPoint(event)
		bateau.sens = newSens
		if(False == self.placerBateau(bateau, pointAncrage)):
			bateau.sens = currentSens
			return False
		return True

	def isIn(self, bateau, pointAncrage):
		(c, l) = pointAncrage
		return (
			c > 0 and l > 0 and
			(('horizontal' == bateau.sens and c - 1 + bateau.taille <= Settings.tailleGrille)
			or ('vertical' == bateau.sens and l - 1 + bateau.taille <= Settings.tailleGrille))
		)
	def seCroise(self, bateau, pointAncrage):
		for case in bateau.listeCasesBateau(pointAncrage):
			if(case in self.emplacements.keys() and bateau.nom != self.emplacements[case]):
				return True
		return False

	def removeBateau(self, bateau):
		for emplacement in dict(self.emplacements):
			if(bateau.nom == self.emplacements[emplacement]):
				del self.emplacements[emplacement]
		bateau.removeGraphique(self)
		del self.bateaux[bateau.nom]

	def toucheCoule(self, pointAttaque):
		case = Settings.pointToCase(pointAttaque)
		#si on a deja attaqué, on ne réattaque pas
		if(case in self.emplacementsAttaque):
			return False, None
		self.emplacementsAttaque.append(case)
		result = 'aleau'

		bateau = self.getBateau(case)
		if(None != bateau):
			result = 'touche'
			bateau.attaque(case)
			if(bateau.estCoule()):
				result = 'coule'
				self.removeBateau(bateau)
				if(len(self.bateaux) == 0):
					result = 'win'
		return result, bateau

	def addGrille(self, placement):
		self.grilleGraphique = self.createGrille();
		self.grilleGraphique.grid(row = placement['row'], column = placement['column'], columnspan = 1, padx = 5, pady = 5)
		return


	def createGrille(self):
		largeur = Settings.tailleCase * Settings.tailleGrille + Settings.epaisseurTrait
		grille = Canvas(Settings.window, bg=Settings.couleurFondGrille, width=largeur, height=largeur)
		for i in range(Settings.tailleGrille +1):
			grille.create_line(
				0,
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2),
				largeur,
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2),
				width=Settings.epaisseurTrait)

			grille.create_line(
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2),
				0,
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2),
				largeur,
				width=Settings.epaisseurTrait)
		return grille

	def bindClic(self, action, params = []):
		self.clicAction = action
		self.clicActionParams = params
		self.grilleGraphique.bind('<Button-1>', self.clicActionHandler)
		return
	def clicActionHandler(self, event):
		return self.clicAction(event, *self.clicActionParams)

	def unbindClic(self):
		self.grilleGraphique.unbind('<Button-1>')

	def placerAleau(self, pointAttaque):
		grille = self.grilleGraphique
		(c, l) = pointAttaque
		#pour la partie graphique, le point d'attaque doit débuter par le point 0, 0
		c -= 1
		l -= 1
		self.figuresAttaque.append(grille.create_line(
			((Settings.tailleCase)*c) + Settings.epaisseurTrait,
			((Settings.tailleCase)*l)+ Settings.epaisseurTrait,
			((Settings.tailleCase)*(c+1)) + Settings.epaisseurTrait,
			((Settings.tailleCase)*(l+1))+ Settings.epaisseurTrait,
			width = Settings.epaisseurMarques, fill = 'white'))
		self.figuresAttaque.append(grille.create_line(
			((Settings.tailleCase)*(c+1)) + Settings.epaisseurTrait,
			((Settings.tailleCase)*l)+ Settings.epaisseurTrait,
			((Settings.tailleCase)*c) + Settings.epaisseurTrait,
			((Settings.tailleCase)*(l+1))+ Settings.epaisseurTrait,
			width = Settings.epaisseurMarques, fill = 'white'))

	def placerTouche(self, pointAttaque):
		grille = self.grilleGraphique
		(c, l) = pointAttaque
		#pour la partie graphique, le point d'attaque doit débuter par le point 0, 0
		c -= 1
		l -= 1
		self.figuresAttaque.append(grille.create_oval(
			Settings.tailleCase*(c+1) + (2*Settings.epaisseurTrait) - Settings.tailleRond,
			Settings.tailleCase*(l+1) + (2*Settings.epaisseurTrait) - Settings.tailleRond,
			Settings.tailleCase*c+Settings.tailleRond,
			Settings.tailleCase*l+Settings.tailleRond,
			width = Settings.epaisseurMarques, outline = 'red'))

	def placerCoule(self, bateau):
		grille = self.grilleGraphique
		ancrage = bateau.listeCasesBateau(bateau.pointAncrage)
		(c1, l1) = Settings.caseToPoint(ancrage[0])
		(c2, l2) = Settings.caseToPoint(ancrage[-1])
		if(bateau.sens == 'horizontal'):
			self.figuresAttaque.append(grille.create_line(
				(Settings.tailleCase*(c1 - 1)) + (Settings.epaisseurTrait),
				(Settings.tailleCase*(l1 - 0.5))+ (Settings.epaisseurTrait),
				(Settings.tailleCase*(c2)) + (Settings.epaisseurTrait),
				(Settings.tailleCase*(l2 - 0.5))+ (Settings.epaisseurTrait),
			width = Settings.epaisseurMarques, fill = 'red'
			))
		else :
			self.figuresAttaque.append(grille.create_line(
				(Settings.tailleCase*(c1 - 0.5)) + (Settings.epaisseurTrait),
				(Settings.tailleCase*(l1 - 1))+ (Settings.epaisseurTrait),
				(Settings.tailleCase*(c2 - 0.5)) + (Settings.epaisseurTrait),
				(Settings.tailleCase*(l2))+ (Settings.epaisseurTrait),
			width = Settings.epaisseurMarques, fill = 'red'
			))

	def viderGrille(self):
		for figure in self.figuresAttaque:
			self.grilleGraphique.delete(figure)
		for bateau in self.bateaux.values():
			bateau.removeGraphique(self)
			bateau.pointAncrage = None
		self.figuresAttaque = []
		self.bateaux = {}
		self.emplacementsAttaque = []
		self.emplacements = {}

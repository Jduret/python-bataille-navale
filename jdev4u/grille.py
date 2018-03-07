from jdev4u.globals import *
from tkinter import *

#
# Classe de gestion des grilles
# pour une bataille navale par exemple on a besoin de 2 grilles
#
class Grille:
	bateaux = {}
	emplacements = {}
	emplacementsAttaque = {}
	casesRestantes = []

	grilleGraphique = None
	isGraphic = True
	figuresAttaque = []

	def __init__(self, joueurType):
		self.emplacements = {}
		self.bateaux = {}
		self.casesRestantes = Globals.listAllCases()

	def hasBateau(self, case):
		return case in self.emplacements

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
		pointAncrage = Globals.caseToPoint(bateau.ancrage[0])
		#Si l'on veut modifier aussi le point d'ancrage lors d'une rotation
		#pointAncrage = Globals.eventToPoint(event)
		bateau.sens = newSens
		if(False == self.placerBateau(bateau, pointAncrage)):
			bateau.sens = currentSens
			return False
		return True

	def isIn(self, bateau, pointAncrage):
		(c, l) = pointAncrage
		return (
			c > 0 and l > 0 and
			(('horizontal' == bateau.sens and c - 1 + bateau.taille <= Globals.tailleGrille)
			or ('vertical' == bateau.sens and l - 1 + bateau.taille <= Globals.tailleGrille))
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
		case = Globals.pointToCase(pointAttaque)
		#si on a deja attaqué, on ne réattaque pas
		if(case in self.emplacementsAttaque.keys()):
			return False, None
		result = 'aleau'

		bateau = self.getBateau(case)
		if(None != bateau):
			result = 'touche'
			bateau.attaque(case)
			if(bateau.estCoule()):
				result = 'coule'
				self.updateEmplacementsAttaque(bateau.ancrage, result)
				self.removeBateau(bateau)
				if(len(self.bateaux) == 0):
					result = 'win'
		self.updateEmplacementsAttaque([case],result)
		return result, bateau

	def addGrille(self, placement):
		self.grilleGraphique = self.createGrille();
		self.grilleGraphique.grid(row = placement['row'], column = placement['column'], columnspan = 1, padx = 5, pady = 5)
		return

	def getCasesAttaqueParStatus(self, searchStatus):
		cases = []
		for case, status in self.emplacementsAttaque.items():
		    if status == searchStatus:
		    	cases.append(case)
		return cases


	def updateEmplacementsAttaque(self, cases, result) :
		for case in cases :
			self.emplacementsAttaque[case] = result
			if(case in self.casesRestantes):
				del self.casesRestantes[self.casesRestantes.index(case)]

	def createGrille(self):
		largeur = Globals.tailleCase * Globals.tailleGrille + Globals.epaisseurTrait
		grille = Canvas(Globals.window, bg=Globals.couleurFondGrille, width=largeur, height=largeur)
		for i in range(Globals.tailleGrille +1):
			grille.create_line(
				0,
				Globals.tailleCase*i+(Globals.epaisseurTrait / 2),
				largeur,
				Globals.tailleCase*i+(Globals.epaisseurTrait / 2),
				width=Globals.epaisseurTrait)

			grille.create_line(
				Globals.tailleCase*i+(Globals.epaisseurTrait / 2),
				0,
				Globals.tailleCase*i+(Globals.epaisseurTrait / 2),
				largeur,
				width=Globals.epaisseurTrait)
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
			((Globals.tailleCase)*c) + Globals.epaisseurTrait,
			((Globals.tailleCase)*l)+ Globals.epaisseurTrait,
			((Globals.tailleCase)*(c+1)) + Globals.epaisseurTrait,
			((Globals.tailleCase)*(l+1))+ Globals.epaisseurTrait,
			width = Globals.epaisseurMarques, fill = 'white'))
		self.figuresAttaque.append(grille.create_line(
			((Globals.tailleCase)*(c+1)) + Globals.epaisseurTrait,
			((Globals.tailleCase)*l)+ Globals.epaisseurTrait,
			((Globals.tailleCase)*c) + Globals.epaisseurTrait,
			((Globals.tailleCase)*(l+1))+ Globals.epaisseurTrait,
			width = Globals.epaisseurMarques, fill = 'white'))

	def placerTouche(self, pointAttaque):
		grille = self.grilleGraphique
		(c, l) = pointAttaque
		#pour la partie graphique, le point d'attaque doit débuter par le point 0, 0
		c -= 1
		l -= 1
		self.figuresAttaque.append(grille.create_oval(
			Globals.tailleCase*(c+1) + (2*Globals.epaisseurTrait) - Globals.tailleRond,
			Globals.tailleCase*(l+1) + (2*Globals.epaisseurTrait) - Globals.tailleRond,
			Globals.tailleCase*c+Globals.tailleRond,
			Globals.tailleCase*l+Globals.tailleRond,
			width = Globals.epaisseurMarques, outline = 'red'))

	def placerCoule(self, bateau):
		grille = self.grilleGraphique
		ancrage = bateau.listeCasesBateau(bateau.pointAncrage)
		(c1, l1) = Globals.caseToPoint(ancrage[0])
		(c2, l2) = Globals.caseToPoint(ancrage[-1])
		if(bateau.sens == 'horizontal'):
			self.figuresAttaque.append(grille.create_line(
				(Globals.tailleCase*(c1 - 1)) + (Globals.epaisseurTrait),
				(Globals.tailleCase*(l1 - 0.5))+ (Globals.epaisseurTrait),
				(Globals.tailleCase*(c2)) + (Globals.epaisseurTrait),
				(Globals.tailleCase*(l2 - 0.5))+ (Globals.epaisseurTrait),
			width = Globals.epaisseurMarques, fill = 'red'
			))
		else :
			self.figuresAttaque.append(grille.create_line(
				(Globals.tailleCase*(c1 - 0.5)) + (Globals.epaisseurTrait),
				(Globals.tailleCase*(l1 - 1))+ (Globals.epaisseurTrait),
				(Globals.tailleCase*(c2 - 0.5)) + (Globals.epaisseurTrait),
				(Globals.tailleCase*(l2))+ (Globals.epaisseurTrait),
			width = Globals.epaisseurMarques, fill = 'red'
			))

	def viderGrille(self):
		for figure in self.figuresAttaque:
			self.grilleGraphique.delete(figure)
		for bateau in self.bateaux.values():
			bateau.removeGraphique(self)
			bateau.pointAncrage = None
		self.figuresAttaque = []
		self.bateaux = {}
		self.emplacementsAttaque = {}
		self.emplacements = {}
		self.casesRestantes = Globals.listAllCases()

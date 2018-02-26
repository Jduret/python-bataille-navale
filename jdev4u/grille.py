from jdev4u.settings import *
#
# Classe de gestion des grilles
# pour une bataille navale par exemple on a besoin de 2 grilles
#
class Grille:
	bateaux = {}
	emplacements = {}
	emplacementsAttaque = {}

	grilleGraphique = None
	grilleType = ''
	figuresAttaque = []

	def __init__(self, joueurType):
		self.emplacements = {}
		self.bateaux = {}

	def hasBateau(self, case):
		return case in self.emplacements

	def getBateau(self, case):
		if self.hasBateau(case):
			return self.bateaux[self.emplacements[case]]
		else :
			return None

	def addGrille(self, placement):
		self.gilleGraphique = self.createGrille();
		self.grilleGraphique.grid(row = placement.row, column = placement.column, columnspan = 1, padx = 5, pady = 5)
		return


	def createGrille(self):
		largeur = Settings.tailleCase*Settings.tailleGrille + Settings.epaisseurTrait
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

	def selectionnerBateau(self, bateauName):
		return

	def placerBateau(self, bateau, event):
		return

	def bindClic(self, action):
		self.grilleGraphique.bind('<Button-1>', action)
		return

	def unbindClic(self):
		self.gilleGraphique.unbind('<Button-1>')

	def placerAleau(self, event):
		grille = self.grilleGraphique
		abscisse = event.x
		ordonnee = event.y

		l = (ordonnee-Settings.epaisseurTrait)//Settings.tailleCase
		c = (abscisse-Settings.epaisseurTrait)//Settings.tailleCase

		self.figuresAttaque['attaque'].append(grille.create_line(
			((Settings.tailleCase)*c) + Settings.epaisseurTrait,
			((Settings.tailleCase)*l)+ Settings.epaisseurTrait,
			((Settings.tailleCase)*(c+1)) + Settings.epaisseurTrait,
			((Settings.tailleCase)*(l+1))+ Settings.epaisseurTrait,
			width = Settings.epaisseurMarques, fill = 'white'))
		self.figuresAttaque['attaque'].append(grille.create_line(
			((Settings.tailleCase)*(c+1)) + Settings.epaisseurTrait,
			((Settings.tailleCase)*l)+ Settings.epaisseurTrait,
			((Settings.tailleCase)*c) + Settings.epaisseurTrait,
			((Settings.tailleCase)*(l+1))+ Settings.epaisseurTrait,
			width = Settings.epaisseurMarques, fill = 'white'))

	def placerTouche(self, event):
		grille = self.grilleGraphique

		abscisse = event.x
		ordonnee = event.y

		l = (ordonnee-Settings.epaisseurTrait)//Settings.tailleCase
		c = (abscisse-Settings.epaisseurTrait)//Settings.tailleCase
		self.figuresAttaque['attaque'].append(grille.create_oval(
			Settings.tailleCase*c+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond,
			Settings.tailleCase*l+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond,
			Settings.tailleCase*c+Settings.tailleRond,
			Settings.tailleCase*l+Settings.tailleRond,
			width = Settings.epaisseurMarques, outline = 'red'))

	def viderGrille(self):
		for figure in self.figuresAttaque:
			self.grilleGraphique.delete(figure)
		for bateau in self.bateaux:
			bateau.removeGraphique(self.grilleGraphique)
			bateau.pointAncrage = None
		self.figuresAttaque = {
			'attaque' : [],
			'bateau' : []
		}

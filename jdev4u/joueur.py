from jdev4u.grille import *
from tkinter import *
from tkinter import StringVar
from random import *
import copy

class Joueur:
	TYPE = 'undefined'
	JOUEUR_PC = 'pc'
	JOUEUR_HUMAIN = 'humain'

	name = None
	grille = None
	isAutomatic = False

	def Factory(self, type):
		if type in Joueur.__subclasses__():
			return eval(type+ '()')
		raise TypeError('Le type de joueur "' + type + '" est inconnu.')

	def __init__(self, name = ''):
		self.name = StringVar()
		self.name.set(name if name != '' else  self.__class__.__name__)
		self.grille = Grille(self.TYPE)

	def createGrille(self):
		raise NotImplementedError('Chaque type de joueur DOIT définir la méthode "createGraphique" permettant de générer le graphique de la grille')

	def getAdversaire(self, joueurs):
		return joueurs[self.JOUEUR_PC] if (self.TYPE == self.JOUEUR_HUMAIN) else joueurs[self.JOUEUR_HUMAIN]

	def attaque(self, pointAttaque):
		return self.grille.toucheCoule(pointAttaque)

	def recommencer(self):
		self.grille.viderGrille()



class JoueurPc(Joueur):
	TYPE = 'pc'
	isAutomatic = True

	def __init__(self, name = ''):
		Joueur.__init__(self, name)
		self.grille.isGraphic = False

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 0})
		return false

	def placementBateauAleatoire(self, bateaux):
		sens = ['horizontal', 'vertical']
		for bateau in bateaux.values():
			bateau = copy.deepcopy(bateau)
			bateauPlace = False
			#on cherche un emplacement libre
			while(False == bateauPlace) :
				cMax = lMax = Settings.tailleGrille
				bateau.sens = sens[randint(0,1)]
				if(bateau.sens == 'horizontal'):
					cMax -= bateau.taille
				else :
					lMax -= bateau.taille
				pointAncrage = [randint(1, cMax), randint(1, lMax)]
				if(self.grille.isIn(bateau, pointAncrage) and False == self.grille.seCroise(bateau, pointAncrage)):
					bateauPlace = True

			self.grille.placerBateau(bateau, pointAncrage)
		return

	def attaqueAleatoire(self):
		pointAttaque = [randint(1, Settings.tailleGrille), randint(1, Settings.tailleGrille)]
		return Settings.pointToEvent(pointAttaque)

class JoueurHumain(Joueur):
	TYPE = 'humain'
	isAutomatic = False

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 2})
		return false

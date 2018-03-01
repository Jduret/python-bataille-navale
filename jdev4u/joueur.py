from jdev4u.grille import *
from tkinter import *
from tkinter import StringVar

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



class JoueurPc(Joueur):
	TYPE = 'pc'
	isAutomatic = True

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 0})
		return false
	
	def placementBateauAleatoire(self):
		return
		
	def attaqueAleatoire(self, adversaire):
		pointAttaque = [2, 2]
		return adversaire.attaque(pointAttaque)

class JoueurHumain(Joueur):
	TYPE = 'humain'

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 2})
		return false

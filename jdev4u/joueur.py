from jdev4u.grille import *


class Joueur:
	TYPE = 'undefined'
	JOUEUR_PC = 'pc'
	JOUEUR_HUMAIN = 'humain'

	name = None
	grille = None

	def Factory(self, type):
		if type in Joueur.__subclasses__():
			return eval(type+ '()')
		raise TypeError('Le type de joueur "' + type + '" est inconnu.')

	def __init__(self, name = ''):
		self.name = name if name != '' else  self.__class__.__name__
		self.grille = Grille(self.TYPE)

	def createGrille(self):
		raise NotImplementedError('Chaque type de joueur DOIT définir la méthode "createGraphique" permettant de générer le graphique de la grille')


class JoueurPc(Joueur):
	TYPE = 'pc'

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 0})
		return false

class JoueurHumain(Joueur):
	TYPE = 'humain'

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 2})
		return false

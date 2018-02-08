from jdev4u.grille import *


class Joueur:
	TYPE = 'undefined'
	JOUEUR_PC = 'pc'
	JOUEUR_HUMAIN = 'humain'

	def Factory(self, type):
		if type in Joueur.__subclasses__():
			return eval(type+ '()')
		raise TypeError('Le type de joueur "' + type + '" est inconnu.')

	def __init__(self, name = ''):
		self.name = name if name != '' else  self.__class__.__name__
		self.grille = Grille()
		
	def choisirCase(self, limitation = None):
		raise NotImplementedError('Chaque type de joueur DOIT définir la méthode "choisirCase"')
	
	#Cette méthode va appeler la méthode choisir case autant de fois que nécessaire pour placer les bateaux
	def placerBateaux(self):
		return false
		
	def toucheCoule(self, point):
		return false

class JoueurPc(Joueur):
	TYPE = 'pc'
	
	def choisirCase(self, limitation = None):
		return false

class JoueurHumain(Joueur):
	TYPE = 'humain'
	
	def choisirCase(self, limitation = None):
		return false

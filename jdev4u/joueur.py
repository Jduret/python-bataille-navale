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
	stats = {
		'lastAttaque' : None,
		'lastResult' : None,
		'lastTouche' : None
	}

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
		result, bateau = self.grille.toucheCoule(pointAttaque)

		self.stats['lastAttaque'] = pointAttaque
		self.stats['lastResult'] = result
		if(result == 'touche'):
			self.stats['lastTouche'] = pointAttaque
		elif(result == 'coule'):
			self.stats['lastTouche'] = None

		return result, bateau

	def recommencer(self):
		self.grille.viderGrille()
		self.stats = {
			'lastAttaque' : None,
			'lastResult' : None,
			'lastTouche' : None
		}



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
		#si on a touché un bateau, on tourne autour pour le trouver
		if(Settings.hardLevel == True and self.stats['lastTouche']!= None) :
			findPoint = False
			for point in Settings.getAroundPoints( self.stats['lastTouche']):
				#on a un point et un sens pour le bateau
				if('touche' == self.grille.emplacementsAttaque[Settings.pointToCase(point)]):
					pointAttaque = self.findNextPoint([ self.stats['lastTouche'], point])
					findPoint = (False != pointAttaque)
				if(False == findPoint and False == (Settings.pointToCase(point) in self.grille.emplacementsAttaque.keys())):
					pointAttaque = point
					findPoint = True
		return Settings.pointToEvent(pointAttaque)

	def findNextPoint(points):
		(c1, l1) = points[0]
		(c2, l2) = points[1]
		sens = None
		if(c1 == c2):
			sens = 'vertical'
		elif(l1 == l2):
			sens = 'horizontal'
		#si les 2 points ne sont alignés ni horizontalement ni verticalement
		#on ne peut calculer de points d'attaque
		else :
			return False

		if(sens == 'horizontal'):
			l = l1
			c = c2 + 1 if (c2 > c1) else c1 + 1
			if(c > Settings.tailleGrille or Settings.pointToCase([c, l]) in self.grille.emplacementsAttaque.keys()):
				c = c2 -1 if (c2 < c1) else c1 -1
		else :
			c = c1
			l = l2 + 1 if (l2 > l1) else l1 + 1
			if(l > Settings.tailleGrille or Settings.pointToCase([c, l]) in self.grille.emplacementsAttaque.keys()):
				l = l2 -1 if (l2 < l1) else l1 -1
		return [c, l]



class JoueurHumain(Joueur):
	TYPE = 'humain'
	isAutomatic = False

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 2})
		return false

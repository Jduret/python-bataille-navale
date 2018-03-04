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
		return  self.grille.toucheCoule(pointAttaque)

	def updateStats(self, result, pointAttaque):
		self.stats['lastAttaque'] = pointAttaque
		self.stats['lastResult'] = result
		if(result == 'touche'):
			self.stats['lastTouche'] = pointAttaque
		#c'est bon on a coulé le bateau, on repasse en recherche à taton
		elif(result == 'coule'):
			self.stats['lastTouche'] = None

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
				cMax = lMax = Globals.tailleGrille
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

	def getPointAttaqueAleatoire(self, adversaire):
		pointAttaque = [randint(1, Globals.tailleGrille), randint(1, Globals.tailleGrille)]

		#creation d'une liste de point possible pour l'attaque
		# le dernier point sera toujours celui issue de la plus grande intelligence
		pointAttaquePossible = [pointAttaque]

		#si on a touché un bateau, on tourne autour pour le trouver
		if(Globals.hardLevel > 0 and self.stats['lastTouche']!= None) :
			for point in Globals.getAroundPoints( self.stats['lastTouche']):
				if(False == (Globals.pointToCase(point) in adversaire.grille.emplacementsAttaque.keys())):
					pointAttaquePossible.append(point)
				if(Globals.hardLevel > 1) :
					#on a un point et un sens pour le bateau
					if('touche' == self.grille.emplacementsAttaque[Globals.pointToCase(point)]):
						pointAttaqueTrouve = self.findNextPoint([ self.stats['lastTouche'], point])
						pointAttaquePossible.append(pointAttaqueTrouve)
						if (False != pointAttaqueTrouve) :
							break
		return Globals.pointToEvent(pointAttaquePossible[-1])

	def findNextPoint(semf, points):
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
			if(c > Globals.tailleGrille or Globals.pointToCase([c, l]) in self.grille.emplacementsAttaque.keys()):
				c = c2 -1 if (c2 < c1) else c1 -1
		else :
			c = c1
			l = l2 + 1 if (l2 > l1) else l1 + 1
			if(l > Globals.tailleGrille or Globals.pointToCase([c, l]) in self.grille.emplacementsAttaque.keys()):
				l = l2 -1 if (l2 < l1) else l1 -1
		return [c, l]



class JoueurHumain(Joueur):
	TYPE = 'humain'
	isAutomatic = False

	def createGrille(self):
		self.grille.addGrille({'row' : 1, 'column' : 2})
		return false

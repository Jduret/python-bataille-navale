import os
import re
from jdev4u.automaticEvent import *

#Un petit  objet d'utilitaire
class Globals:
	__location__ = os.getcwd()
	window = None
	title = 'Bataille Navale'
	defaultHumainName = 'Joueur 1'
	#Devraient etre dans la classe Grille
	#nombre de cases de largeur de la grille
	tailleGrille = 10
	#taille en px d'une case
	tailleCase = 40
	#épaisseur du trait
	epaisseurTrait = 3
	#Taille du rond de placement bateau + placement touché (obligatoirement inférieur à tailleCase)
	tailleRond = tailleCase - 5
	epaisseurMarques = 5
	couleurFondGrille = 'lightseagreen'

	grillePlacement = {
		'humain' : {'column' : 2, 'row' : 1},
		'pc' : {'column' : 0, 'row' : 1}
	}
	#ce paramètre permet de gérer le placement au centre de la fenêtre.
	#En cas de souci de fenêtre qui n'apparait pas, essayer de désactiver ce paramètre
	enableWindowUpdate = False

	columnList = None
	hardLevel = False

	def	eventToPoint(event):
		abscisse = event.x
		ordonnee = event.y
		l = (ordonnee-Globals.epaisseurTrait)//Globals.tailleCase
		c = (abscisse-Globals.epaisseurTrait)//Globals.tailleCase
		#la première case est la 0, 0
		#transformation en 1, 1
		return [c + 1, l + 1]

	def pointToEvent(point):
		(c, l) = point
		x = ((c - 1) * Globals.tailleCase) + Globals.epaisseurTrait
		y = ((l - 1) * Globals.tailleCase) + Globals.epaisseurTrait
		return AutomaticEvent(x, y)

	def pointToCase(point):
		(c, l) = point
		return Globals.columnToChar(c) + str(l)

	def caseToPoint(case):
		match = re.match(r"([a-z]+)([0-9]+)", case, re.I)

		(columnChar, line) = match.groups()
		return [Globals.charToColumn(columnChar), int(line)]


	def array_merge( first_array , second_array ):
		if isinstance( first_array , list ) and isinstance( second_array , list ):
			return first_array + second_array
		elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
			return dict( list( first_array.items() ) + list( second_array.items() ) )
		elif isinstance( first_array , set ) and isinstance( second_array , set ):
			return first_array.union( second_array )
		return False

	def getColumnList():
		if(None == Globals.columnList):
			Globals.columnList = Globals.sizeToColumnList(Globals.tailleGrille)
		return Globals.columnList

	def sizeToColumnList(size):
		alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
		charlist = []
		prefix = []
		for x in range(0, size):
			if(x > 0 and 0 == (x % len(alphabet)) ):
				if(0 == len(prefix) or prefix[-1] == alphabet[-1]) :
					if(0 < len(prefix)) :
						prefix[-1] = alphabet[0]
					prefix.append(alphabet[0])
				else :
					prefix[-1] = alphabet[alphabet.index(prefix[-1]) + 1]
			charlist.append(''.join(prefix) + alphabet[(x % len(alphabet))])
		return charlist


	def columnToChar(column) :
		alphabet = Globals.getColumnList()
		return alphabet[column-1]

	def charToColumn(char) :
		alphabet = Globals.getColumnList()
		return alphabet.index(char) + 1

	def getAroundPoints(point):
		(c, l) = point
		listPoints = []
		for pt in [
			[c+1, l],
			[c-1, l],
			[c, l+1],
			[c, l-1]
		] :
			(colonne, ligne) = pt
			if(colonne <= Globals.tailleGrille
				and ligne <= Globals.tailleGrille):
				listPoints.append(pt)
		return listPoints


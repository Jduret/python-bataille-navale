from ..jdev4u.globals import *
from ..jdev4u.plateau import *
from ..jdev4u.jeu import *
import sys
#on va simuler un plan d'attaque pour vérifier le fonctionnement de l'attaque aléatoire intelligente

def attaqueAleatoire(stats, emplacementsAttaque):
	pointAttaque = [randint(1, Globals.tailleGrille), randint(1, Globals.tailleGrille)]

	#si on a touché un bateau, on tourne autour pour le trouver
	if(Globals.hardLevel == True and stats['lastTouche']!= None) :
		points = Globals.getAroundPoints( stats['lastTouche'])
		print(points)
		for point in points:
			if(not (Globals.pointToCase(point) in emplacementsAttaque.keys())):
				pointAttaque = point
			else :
				case = Globals.pointToCase(point)
				print(case)
				#on a un point et un sens pour le bateau
				if('touche' == emplacementsAttaque[case]):
					print([stats['lastTouche'], point])
					pointAttaque = 'findNextPoint'
					if (False != pointAttaque) :
						break

	return pointAttaque

def findNextPoint(points, emplacementsAttaque):
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
			if(c > Globals.tailleGrille or Globals.pointToCase([c, l]) in emplacementsAttaque.keys()):
				c = c2 -1 if (c2 < c1) else c1 -1
		else :
			c = c1
			l = l2 + 1 if (l2 > l1) else l1 + 1
			if(l > Globals.tailleGrille or Globals.pointToCase([c, l]) in emplacementsAttaque.keys()):
				l = l2 -1 if (l2 < l1) else l1 -1
		return [c, l]

#print(attaqueAleatoire({'lastTouche' : [2, 2]}, {}))
#print(attaqueAleatoire({'lastTouche' : [2, 2]}, {'B1' : 'aleau'}))
print(attaqueAleatoire({'lastTouche' : [2, 2]}, {'B3' : 'touche'}))
print(findNextPoint([[2, 2], [2, 3]],  {'B3' : 'touche'}))
print(findNextPoint([[2, 2], [2, 3]],  {'B3' : 'touche', 'B4' : 'aleau'}))


sys.exit(0)

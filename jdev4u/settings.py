import os

#Un petit  objet d'utilitaire pourrait êtr renommé en Utils ou Globals
class Settings:
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
	
	@staticmethod
	def	eventToPoint(event):
		abscisse = event.x
		ordonnee = event.y
		l = (ordonnee-Settings.epaisseurTrait)//Settings.tailleCase
		c = (abscisse-Settings.epaisseurTrait)//Settings.tailleCase
		return [c, l]
		
	def array_merge( first_array , second_array ):
		if isinstance( first_array , list ) and isinstance( second_array , list ):
			return first_array + second_array
		elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
			return dict( list( first_array.items() ) + list( second_array.items() ) )
		elif isinstance( first_array , set ) and isinstance( second_array , set ):
			return first_array.union( second_array )
		return False
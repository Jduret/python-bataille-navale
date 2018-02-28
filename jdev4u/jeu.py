from jdev4u.joueur import *
from jdev4u.bateau import *
from jdev4u.plateau import *
import copy

#
# Class de gestion du jeu
# contient les méthodes propre au jeu
# recommencer
# placerBateaux ...
#
class Jeu:
	joueurs = {Joueur.JOUEUR_PC : None, Joueur.JOUEUR_HUMAIN : None}
	_bateauxDisponibles = None
	currentJoueur = None
	currentBateau = None

	def __init__(self):
		# Drapeau permettant de connaitre le joueur suivant
		# l'humain commence le jeu
		self.currentJoueur = Joueur.JOUEUR_HUMAIN;
		self.currentBateau = None
		#Le jeu bataille navale est fait de 2 joueurs
		#le PC
		self.joueurs[Joueur.JOUEUR_PC] = JoueurPc()
		#l'humain
		self.joueurs[Joueur.JOUEUR_HUMAIN] = JoueurHumain()

	#	Méthode permettant de réinitialiser une partie
	def recommencer(self):
		for joueurType in self.joueurs:
			self.joueurs[joueurType].grille.viderGrille()

	def getBateaux(self, refresh = False):
		if self._bateauxDisponibles == None or refresh == True :
			self._bateauxDisponibles = self._readConfigFile()
		return self._bateauxDisponibles

	def getBateau(self, name):
		return self.getBateaux()[name]

	def _readConfigFile(self, fichierPath = 'include/bateaux.txt'):
		result = {}
		file = open(os.path.join(Settings.__location__, fichierPath), 'r')
		for ligne in file:
			name, size = ligne.split(';')
			result[name] = Bateau(name, size)
		return result

	#cette méthode permet à l'utilisateur de placer ses bateaux
	def selectionBateau(self, bateauName, joueurType):
		#au premier appel on met en place la gestion du clique sur la grille permettant le placement des bateaux
		if(None == self.currentBateau):
			self.joueurs[joueurType].grille.bindClic(self.placerBateau, [joueurType])

		#cloner le bateau ICI
		self.currentBateau = copy.deepcopy(self.getBateau(bateauName)) if (False == (bateauName in self.joueurs[joueurType].grille.bateaux.keys())) else self.joueurs[joueurType].grille.bateaux[bateauName]		
	
	#Positionne le bateau sur la grille si possible
	def placerBateau(self, event, joueurType):
		pointAncrage = Settings.eventToPoint(event)
		#On place le bateau dans la grille, et on l'affiche ou le déplace sur la grille graphique
		self.joueurs[joueurType].grille.placerBateau(self.currentBateau, pointAncrage)
		
	def tousLesBateauxSontPlaces(self, joueurType):
		return (len(self.getBateaux()) == len(self.joueurs[joueurType].grille.bateaux))

	#Permet de retourner le joueur actuel
	def joueurSuivant(self):
		joueur = self.joueurSuivant
		self.joueurSuivant = Joueur.JOUEUR_HUMAIN if self.joueurSuivant == Joueur.JOUEUR_PC  else Joueur.JOUEUR_PC

	#Return touche | aleau
	def attaquer(self, event):
		result = self.currentJoueur.adversaire.attaque(Plateau.eventToPoint(event))
		if result == 'touche':
			self.currentJoueur.placerTouche(self.elements['grillePc'], event)
		elif result == 'aleau':
			self.currentJoueur.placerAleau(self.elements['grillePc'], event)


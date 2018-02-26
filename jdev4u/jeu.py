from jdev4u.joueur import *
from jdev4u.bateau import *
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

	def __init__(self):
		# Drapeau permettant de connaitre le joueur suivant
		# l'humain commence le jeu
		self.currentJoueur = Joueur.JOUEUR_HUMAIN;
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

	#Positionne le bateau sur la grille si possible
	#a faire
	def placerBateau(self, joueurType, pointAncrage):
		#cloner le bateau ICI
		self.joueurs[joueurType].grille.placerBateau(copy.deepcopy(self.currentBateau), pointAncrage)

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


from jdev4u.joueur import *
from jdev4u.bateau import *
#
# Class de gestion du jeu
# contient les méthodes propre au jeu
# recommencer
# placerBateaux ...
#
class Jeu:
	joueurs = {Joueur.JOUEUR_PC : None, Joueur.JOUEUR_HUMAIN : None}
	_bateauxDisponibles = None
	currentBateau = None
	
	def __init__(self, window = None):
		# Drapeau permettant de connaitre le joueur suivant
		# l'humain commence le jeu
		self._joueurSuivant = Joueur.JOUEUR_HUMAIN;
		#Le jeu bataille navale est fait de 2 joueurs
		#le PC
		self.joueurs[Joueur.JOUEUR_PC] = JoueurPc()
		#l'humain
		self.joueurs[Joueur.JOUEUR_HUMAIN] = JoueurHumain()
		
		self.currentBateauName = None
				
	#	Méthode permettant de réinitialiser une partie
	def recommencer(self):
		self.__init__()
		
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
			result[name] = Bateau(name, size, self)
		return result
		
	def positionnerBateaux(self, emplacements, bateau, joueur = None):
		self.joueurs[joueur].placerBateau(bateau, emplacements)
	
	#Permet de retourner le joueur actuel
	def joueurSuivant(self):
		joueur = self.joueurSuivant
		self.joueurSuivant = Joueur.JOUEUR_HUMAIN if self.joueurSuivant == Joueur.JOUEUR_PC  else Joueur.JOUEUR_PC
	
	#Return touche | aleau
	def attaquer(self, plateau, pointAttaque):
		(ligne, colonne) = pointAttaque
		ligne = ligne + 1
		colonne = colonne + 1
		plateau.message('attaque : ' + ';'.join([str(ligne), str(colonne)]))
		bateaux = self.getBateaux()
		attaque =  str(colonne) + str(ligne)
		for bateauName in bateaux:
			if attaque in bateaux[bateauName].ancrage :
				return 'touche'
			
		return 'aleau'
		
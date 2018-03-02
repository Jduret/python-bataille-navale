from jdev4u.joueur import *
from jdev4u.bateau import *
from jdev4u.plateau import *
import copy
from tkinter import StringVar

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
	plateau = None
	nbTours = 0
	nbToursStatus = None

	def __init__(self):
		# Drapeau permettant de connaitre le joueur suivant
		# l'humain commence le jeu
		self.currentJoueur = Joueur.JOUEUR_HUMAIN;
		self.currentBateau = None
		self.nbToursStatus = StringVar()
		#Le jeu bataille navale est fait de 2 joueurs
		#le PC
		self.joueurs[Joueur.JOUEUR_PC] = JoueurPc()
		if(self.joueurs[Joueur.JOUEUR_PC].isAutomatic):
			self.joueurs[Joueur.JOUEUR_PC].placementBateauAleatoire(self.getBateaux())
		#l'humain
		self.joueurs[Joueur.JOUEUR_HUMAIN] = JoueurHumain()
		if(self.joueurs[Joueur.JOUEUR_HUMAIN].isAutomatic):
			self.joueurs[Joueur.JOUEUR_HUMAIN].placementBateauAleatoire(self.getBateaux())

	#	Méthode permettant de réinitialiser une partie
	def recommencer(self):
		for joueurType in self.joueurs:
			self.joueurs[joueurType].recommencer()
			if(self.joueurs[joueurType].isAutomatic) :
				self.joueurs[joueurType].placementBateauAleatoire(self.getBateaux())
		self.currentBateau = None
		self.nbTours = 0
		self.nbToursStatus.set('En attente...');
		self.plateau.status.set('Placez vos bateaux')

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
		self.currentJoueur = Joueur.JOUEUR_HUMAIN if self.currentJoueur == Joueur.JOUEUR_PC  else Joueur.JOUEUR_PC
		if(self.joueurs[self.currentJoueur].isAutomatic):
			loop = True
			while(loop):
				loop = (False == self.attaquer(self.joueurs[self.currentJoueur].attaqueAleatoire()))

	#Return touche | coule | aleau
	def attaquer(self, event):
		pointAttaque = Settings.eventToPoint(event)
		result, bateau = self.joueurs[self.currentJoueur].getAdversaire(self.joueurs).attaque(pointAttaque)
		if(False == result) :
			return False
		#cas spécial à l'eau
		if(result == 'aleau'):
			self.joueurs[self.currentJoueur].getAdversaire(self.joueurs).grille.placerAleau(pointAttaque)
		#dans tous les autres cas que à l'eau, on place une touche
		else :#if(result=='touche' or result=='coule' or result=='win'):
			self.joueurs[self.currentJoueur].getAdversaire(self.joueurs).grille.placerTouche(pointAttaque)
		#cas spécial de la victoire
		if(result == 'win'):
			self.joueurs[Joueur.JOUEUR_PC].grille.unbindClic()
			if(None != self.plateau):
				self.plateau.winner(self.joueurs[self.currentJoueur])
		#cas spécial du coulé
		if(result == 'coule'):
			self.joueurs[self.currentJoueur].getAdversaire(self.joueurs).grille.placerCoule(bateau)
			self.nbToursStatus.set('Bateau ' + bateau.nom + ' ' + result + '.')
			self.plateau.status.set(
				self.joueurs[Joueur.JOUEUR_PC].name.get() + ' ' + str(len(self.joueurs[Joueur.JOUEUR_HUMAIN].grille.bateaux)) + '/' + str(len(self.getBateaux()))
				+ ' ' + self.joueurs[Joueur.JOUEUR_HUMAIN].name.get() + ' ' + str(len(self.joueurs[Joueur.JOUEUR_PC].grille.bateaux)) + '/' + str(len(self.getBateaux()))
			)
		if(self.currentJoueur == Joueur.JOUEUR_HUMAIN):
			self.nbTours += 1
			resultStatus = {
				'touche' : 'touché',
				'coule' : 'coulé',
				'aleau' : 'à l\'eau',
				'win' : 'gagné!!'
			}
			self.nbToursStatus.set('Attaque ' + str(self.nbTours) + ' ' + Settings.pointToCase(pointAttaque) + ' ' + resultStatus[result])
		#certaines regles permettent à un attaquant de rejouer en cas de succès
		#pour mettre en place cette règle, il suffit de déplacer joueurSuivant dans le case 'aleau'
		#et de faire en sorte que attaquer retourne False
		self.joueurSuivant()

		return result


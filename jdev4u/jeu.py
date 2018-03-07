import copy
import pickle
from tkinter import StringVar

from jdev4u.joueur import *
from jdev4u.bateau import *
from jdev4u.plateau import *

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
	nomFichierScore = 'scores.db'
	scores = None
	score = None

	def __init__(self):
		# Drapeau permettant de connaitre le joueur suivant
		# l'humain commence le jeu
		self.currentJoueur = Joueur.JOUEUR_HUMAIN;
		self.currentBateau = None
		self.nbToursStatus = StringVar()
		self.score = StringVar()

		#Le jeu bataille navale est fait de 2 joueurs
		#le PC
		self.joueurs[Joueur.JOUEUR_PC] = JoueurPc()
		if(self.joueurs[Joueur.JOUEUR_PC].isAutomatic):
			self.joueurs[Joueur.JOUEUR_PC].placementBateauAleatoire(self.getBateaux())
		#l'humain
		self.joueurs[Joueur.JOUEUR_HUMAIN] = JoueurHumain()
		if(self.joueurs[Joueur.JOUEUR_HUMAIN].isAutomatic):
			self.joueurs[Joueur.JOUEUR_HUMAIN].placementBateauAleatoire(self.getBateaux())
		#ajout de la gestion des scores
		self.recupererScores()
		self.updateAffichageScore()

	#	Méthode permettant de réinitialiser une partie
	def recommencer(self):
		for joueurType in self.joueurs:
			self.joueurs[joueurType].recommencer()
			if(self.joueurs[joueurType].isAutomatic) :
				self.joueurs[joueurType].placementBateauAleatoire(self.getBateaux())
		self.currentBateau = None
		self.nbTours = 0
		self.nbToursStatus.set('En attente...');

	def buildPath (self, fichierPath):
		return os.path.join(Globals.__location__, fichierPath)
	# fonctions permettant d'enregistrer les scores des joueurs.
	# Créé un fichier pour le joueur s'il n'existe pas, ajoute 1 point s'il a gagné au score précédent
	def enregistrerScores(self):
		fichier_scores=open(self.buildPath(self.nomFichierScore),"wb")
		mon_pickler=pickle.Pickler(fichier_scores)
		mon_pickler.dump(self.scores)
		fichier_scores.close()

	def recupererScores(self):
		"""
		Permet de récuperer la liste des scores
		retourne Vrai si la liste à été chargée, Faux sinon
		"""
		self.scores={}
		if os.path.exists(self.buildPath(self.nomFichierScore)):
			fichier_scores=open(self.buildPath(self.nomFichierScore),"rb")
			mon_depickler=pickle.Unpickler(fichier_scores)
			self.scores=mon_depickler.load()
			fichier_scores.close()
			return True
		return False

	def updateAffichageScore(self):
		self.score.set( 'Scores : '
			+ self.joueurs[Joueur.JOUEUR_PC].name.get() + ' ' + str(self.getScore(self.joueurs[Joueur.JOUEUR_PC].name.get()))
			+ ' ' + self.joueurs[Joueur.JOUEUR_HUMAIN].name.get() + ' ' + str(self.getScore(self.joueurs[Joueur.JOUEUR_HUMAIN].name.get()))
		)

	def getScore(self, nomJoueur):
		return self.scores[nomJoueur] if nomJoueur in self.scores.keys() else 0

	def ajouterScore(self, nomJoueur):
		"""
		Gestion des scores : ajoute un point au gagnant reférencé par son nom
		"""
		if nomJoueur not in self.scores.keys():
		    self.scores[nomJoueur]=0
		self.scores[nomJoueur] += 1
		self.enregistrerScores()
		self.updateAffichageScore()


	def getBateaux(self, refresh = False):
		if self._bateauxDisponibles == None or refresh == True :
			self._bateauxDisponibles = self._readConfigFile()
		return self._bateauxDisponibles

	def getBateau(self, name):
		return self.getBateaux()[name]

	def _readConfigFile(self, fichierPath = 'include/bateaux.txt'):
		result = {}
		file = open(self.buildPath(fichierPath), 'r')
		for ligne in file:
			name, size, color = ligne.rstrip("\r\n").split(';')
			result[name] = Bateau(name, size, color)
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
		pointAncrage = Globals.eventToPoint(event)
		#On place le bateau dans la grille, et on l'affiche ou le déplace sur la grille graphique
		self.joueurs[joueurType].grille.placerBateau(self.currentBateau, pointAncrage)

	def tousLesBateauxSontPlaces(self, joueurType):
		return (len(self.getBateaux()) == len(self.joueurs[joueurType].grille.bateaux))

	#Permet de retourner le joueur actuel
	def joueurSuivant(self):
		self.currentJoueur = Joueur.JOUEUR_HUMAIN if self.currentJoueur == Joueur.JOUEUR_PC  else Joueur.JOUEUR_PC
		if(self.joueurs[self.currentJoueur].isAutomatic):
			self.attaquer(self.joueurs[self.currentJoueur].getPointAttaqueAleatoire(self.joueurs[self.currentJoueur].getAdversaire(self.joueurs)))

	#Return touche | coule | aleau
	def attaquer(self, event):
		pointAttaque = Globals.eventToPoint(event)
		(result, bateau) = self.joueurs[self.currentJoueur].getAdversaire(self.joueurs).attaque(pointAttaque)
		#result est FAUX dans 2 situations
		#la case attaqué est hors grille
		#la case attaqué à déjà été attaqué
		if(False == result) :
			if (self.currentJoueur == Joueur.JOUEUR_PC ) :
				self.joueurSuivant()
			return False
		#on informe le joueur du résultat de son attaque
		self.joueurs[self.currentJoueur].updateStats(result, pointAttaque)
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
			self.ajouterScore(self.joueurs[self.currentJoueur].name.get())
		#cas spécial du coulé
		if(result == 'coule'):
			self.joueurs[self.currentJoueur].getAdversaire(self.joueurs).grille.placerCoule(bateau)
			self.nbToursStatus.set('Bravo, bateau ' + bateau.nom + 'coulé.')

		if(self.currentJoueur == Joueur.JOUEUR_HUMAIN):
			self.nbTours += 1
			resultStatus = {
				'touche' : 'touché',
				'coule' : 'coulé',
				'aleau' : 'à l\'eau',
				'win' : 'gagné!!'
			}
			self.nbToursStatus.set('Attaque ' + str(self.nbTours) + ' ' + Globals.pointToCase(pointAttaque) + ' ' + resultStatus[result])
		#certaines regles permettent à un attaquant de rejouer en cas de succès
		#pour mettre en place cette règle, il suffit de déplacer joueurSuivant dans le case 'aleau'
		#et de faire en sorte que attaquer retourne False
		self.joueurSuivant()

		return result


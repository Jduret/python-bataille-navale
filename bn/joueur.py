from bn.grille import *
import os
import pickle


class Joueur:
	TYPE = 'undefined'
	JOUEUR_PC = 'pc'
	JOUEUR_HUMAIN = 'humain'

	def Factory(self, type):
		if type in Joueur.__subclasses__():
			return eval(type+ '()')
		raise TypeError('Le type de joueur "' + type + '" est inconnu.')

	def __init__(self, name = ''):
		self.name = name if name != '' else  self.__class__.__name__
		self.grille = Grille()
		
	def choisirCase(self, limitation = None):
		raise NotImplementedError('Chaque type de joueur DOIT définir la méthode "choisirCase"')
	

	def enregistrer_scores(self,scores):
		fichier_scores=open(nom_fichier_scores,"wb")
		mon_pickler=pickle.Pickler(fichier_scores)
		mon_pickler.dump(scores)
		fichier_scores.close()

	# fonctions gérant les éléments saisis par l'utilisateur
	def recup_nom_utilisateur(self):
		nom_utilisateur=plateau.askName.answer()
		nom_utilisateur=nom_utilisateur.capitalize()
		if not nom_utilisateur.isalnum() or len(nom_utilisateur)<3:
			print("ce nom est invalide")
			return recup_nom_utilisateur()
		else:
			return nom_utilisateur

	def recup_scores():
		if os.path.exists(nom_fichier_scores):
			fichier_scores=open(nom_fichier_scores,"rb")
			mon_depickler=pickle.Unpickler(fichier_scores)
			scores=mon_depickler.load()
			fichier_scores.close()
		else:
			scores={}
		return scores

	
	#Cette méthode va appeler la méthode choisir case autant de fois que nécessaire pour placer les bateaux
	def placerBateaux(self):
		return false
		
	def toucheCoule(self, point):
		return false

class JoueurPc(Joueur):
	TYPE = 'pc'
	
	def choisirCase(self, limitation = None):
		return false

class JoueurHumain(Joueur):
	TYPE = 'humain'
	
	def choisirCase(self, limitation = None):
		return false


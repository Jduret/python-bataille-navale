##----- Importation des Modules -----##
from __future__ import generators
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import StringVar

import os
#Attention, on importe pas tous car os conteint AUSSI une méthode open
#from os import *
from math import *
from sys import *
from jdev4u.globals import *
from jdev4u.bateau import *
from jdev4u.joueur import *

class Plateau:
	#instance de Jeu
	jeu = None
	bateauText = None

	#Dans ce tableau on va placer tous les éléments graphique nécessaire à l'interface
	elements = {}

	def __init__(self, batailleNavale):
		#cas d'une dépendance croisée. A limiter au strict nécessaire
		batailleNavale.plateau = self
		self.jeu = batailleNavale
		self.bateauText = StringVar()
		self.bateauText.set('')

		self.elements['messageStatus'] = Label(Globals.window, anchor= W, textvariable=self.jeu.score)
		#le columnspan ici permet de faire en sorte que le texte se place sur toute la largeur de la fenêtre
		self.elements['messageStatus'].grid(row = 0, column = 0, padx=3, pady=3, columnspan=3, sticky = W+E)

		self.elements['messageAttaque'] = Label(Globals.window, textvariable=self.jeu.nbToursStatus)
		self.elements['messageAttaque'].grid(row = 0, column = 2, padx=3, pady=3, sticky = W+E)

		##----- Zones de texte -----##
		self.elements['messagePc'] = Label(Globals.window, text='Joueur PC')
		self.elements['messagePc'].grid(row = 2, column = 0, padx=3, pady=3, sticky = W+E)

		self.elements['messageHumain'] = Label(Globals.window, textvariable=self.jeu.joueurs[Joueur.JOUEUR_HUMAIN].name)
		self.elements['messageHumain'].grid(row = 2, column = 2, padx=3, pady=3, sticky = W+E)

		#Boutons
		self.elements['boutonQuitter'] = Button(Globals.window, text='Quitter', command = Globals.window.destroy)
		self.elements['boutonQuitter'].grid(row = 4, column = 2, padx = 3, pady = 3,sticky=S+W+E)

		self.elements['boutonRecommencer'] = Button(Globals.window, text='Nouvelle partie', command=self.recommencer)
		self.elements['boutonRecommencer'].grid(row = 4, column = 0, padx = 3, pady = 3, sticky = S+W+E)

		def askName():
			self.jeu.joueurs[Joueur.JOUEUR_HUMAIN].name.set(simpledialog.askstring('Nouveau nom', Globals.window))
			self.jeu.updateAffichageScore()

		self.elements['boutonChangeNom'] = Button(Globals.window, text='Changer nom', command=askName)
		self.elements['boutonChangeNom'].grid(row = 4, column = 1, padx = 3, pady = 3, sticky = S+W+E)

		self.elements['BateauTitle'] = Label(Globals.window, text='Placement bateau :')
		self.elements['BateauTitle'].place(relx=0.5, rely=0.1, anchor= CENTER, relwidth=0.4)
		self.elements['CurrentBateau'] = Label(Globals.window, textvariable=self.bateauText)
		self.elements['CurrentBateau'].place(in_=self.elements['BateauTitle'], relx=0.5, rely=1.2,  bordermode='outside', anchor= CENTER)

		self.createBateauxButtons()

		#ajout des grilles
		for joueurType in self.jeu.joueurs:
			self.jeu.joueurs[joueurType].grille.addGrille(Globals.grillePlacement[joueurType])

		self.recommencer()

	def updatePosition(self):
		#Cette ligne permet de désactiver le replacement automatique de la fenêtre
		if(Globals.enableWindowUpdate):
			return;

		#Taille actuelle de la fenêtre
		h = Globals.window.winfo_height()
		w = Globals.window.winfo_width()

		#Si la fenêtre n'est pas encore dessiné, on reporte
		#si la hauteur est inférieur à 50, alors on considère qu'elle n'est pas déssinée
		if(h < 50):
			Globals.window.after(50, self.updatePosition)
			return
		# Taille actuelle de l'écran
		ws = Globals.window.winfo_screenwidth() # largeur de l'écran
		hs = Globals.window.winfo_screenheight() # hauteur de l'écran

		# calcul des coordonnées du point en haut à gauche de la fenêtre
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)

		# set the dimensions of the screen
		# and where it is placed
		Globals.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def createBateauxButtons(self):
		#on initialise à None pour pouvoir gérer le placement des boutons relativement au bouton précédent (option "_in" de la méthode "place")
		#et évidemment, le premier bouton n'a pas de précédent, et donc il sera placé relativement à la fenêtre (absence de l'option "_in")
		lastShip = None
		if('boutonBateau' in self.elements.keys()):
			for bouton in self.elements['boutonBateau'].values():
				bouton.destroy();
		self.elements['boutonBateau'] = {}

		for bateau in self.jeu.getBateaux():
			self.elements['boutonBateau'][bateau] = Button(Globals.window, text=bateau, command=lambda  currentBateau = bateau:
				self.placerBateau(bateauName = currentBateau, joueurType = Joueur.JOUEUR_HUMAIN)
			)

			if(None == lastShip):
				self.elements['boutonBateau'][bateau].place(relx=0.5, rely=0.2, anchor= CENTER, relwidth=0.4)
			else :
				self.elements['boutonBateau'][bateau].place(in_=self.elements['boutonBateau'][lastShip], relx=0.5, anchor= CENTER, rely=1.5, relwidth=1, bordermode='outside')
			lastShip = bateau
		#On ajoute un bouton de validation du placement des bateaux
		self.elements['boutonBateau']['validerPlacement'] = Button(Globals.window, text='Valider', command=lambda :
			self.validerPlacement(Joueur.JOUEUR_HUMAIN)
		)
		self.elements['boutonBateau']['validerPlacement'].place(in_=self.elements['boutonBateau'][lastShip], relx=0.5, anchor = CENTER, rely = 2.5, relwidth=1, bordermode='outside')

	def placerBateau(self, bateauName, joueurType) :
		self.bateauText.set(bateauName)
		self.jeu.selectionBateau(bateauName, joueurType)

	def validerPlacement(self, joueurType):
		if(False == self.jeu.tousLesBateauxSontPlaces(joueurType)):
			self.message('Tous les bateaux ne sont pas encore placés')
			return
		#On désactive les boutons
		if('boutonBateau' in self.elements.keys()):
			for bouton in self.elements['boutonBateau'].values():
				bouton.configure(state = DISABLED);

		self.jeu.joueurs[joueurType].grille.unbindClic()
		for bateau in self.jeu.joueurs[joueurType].grille.bateaux.values():
			bateau.unbindMove(self.jeu.joueurs[joueurType].grille)
		self.jeu.joueurs[joueurType].getAdversaire(self.jeu.joueurs).grille.bindClic(self.jeu.attaquer)

	def recommencer(self):
		self.elements['messageHumain'].configure(text=Globals.defaultHumainName)
		self.jeu.recommencer()
		if('boutonBateau' in self.elements.keys()):
			for bouton in self.elements['boutonBateau'].values():
				bouton.configure(state = NORMAL);

	def unbindAll(self):
		for joueur in self.jeu.joueurs.values():
			joueur.grille.unbindClic()

	def message(self, text):
		messagebox.showinfo(Globals.title, text)

	def winner(self, joueur):
		self.unbindAll()
		if(joueur.TYPE == Joueur.JOUEUR_HUMAIN):
			self.message('Bravo ' + joueur.name.get() + ' tu as gagné!')
		else :
			self.message('Dommage! PERDU...')




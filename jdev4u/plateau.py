##----- Importation des Modules -----##
from __future__ import generators
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import StringVar

import os
#Attention, on importe pas tous car os conteint AUSSI une méthode open
#from os import *
from copy import *
from random import *
from math import *
from sys import *
from jdev4u.settings import *
from jdev4u.bateau import *
from jdev4u.joueur import *

class Plateau:
	#instance de Jeu
	jeu = None
	bateauText = None

	#Dans ce tableau on va placer tous les éléments graphique nécessaire à l'interface
	elements = {}

	def __init__(self, batailleNavale):
		self.jeu = batailleNavale
		self.bateauText = StringVar()
		self.bateauText.set('')

		self.elements['messageStatus'] = Label(Settings.window, text='Placez vos bateaux ici le message peut prendre de la place c\'est pas grave il dispose de toute une ligne pour lui tout seul')
		#le columnspan ici permet de faire en sorte que le texte se place sur toute la largeur de la fenêtre
		self.elements['messageStatus'].grid(row = 0, column = 0, padx=3, pady=3, columnspan=3, sticky = W+E)

		##----- Zones de texte -----##
		self.elements['messagePc'] = Label(Settings.window, text='Joueur PC')
		self.elements['messagePc'].grid(row = 2, column = 0, padx=3, pady=3, sticky = W+E)

		self.elements['messageHumain'] = Label(Settings.window, textvariable=self.jeu.joueurs[Joueur.JOUEUR_HUMAIN].name)
		self.elements['messageHumain'].grid(row = 2, column = 2, padx=3, pady=3, sticky = W+E)

		#Boutons
		self.elements['boutonQuitter'] = Button(Settings.window, text='Quitter', command = Settings.window.destroy)
		self.elements['boutonQuitter'].grid(row = 4, column = 2, padx = 3, pady = 3,sticky=S+W+E)

		self.elements['boutonRecommencer'] = Button(Settings.window, text='Nouvelle partie', command=self.recommencer)
		self.elements['boutonRecommencer'].grid(row = 4, column = 0, padx = 3, pady = 3, sticky = S+W+E)

		def askName():
			self.jeu.joueurs[Joueur.JOUEUR_HUMAIN].name.set(simpledialog.askstring('Nouveau nom', Settings.window))
			#self.elements['messageHumain'].configure(text=answer)

		self.elements['boutonChangeNom'] = Button(Settings.window, text='Changer nom', command=askName)
		self.elements['boutonChangeNom'].grid(row = 4, column = 1, padx = 3, pady = 3, sticky = S+W+E)

		self.elements['BateauTitle'] = Label(Settings.window, text='Placement bateau :')
		self.elements['BateauTitle'].place(relx=0.5, rely=0.1, anchor= CENTER, relwidth=0.4)
		self.elements['CurrentBateau'] = Label(Settings.window, textvariable=self.bateauText)
		self.elements['CurrentBateau'].place(in_=self.elements['BateauTitle'], relx=0.5, rely=1.2,  bordermode='outside', anchor= CENTER)

		self.createBateauxButtons()
		
		#ajout des grilles
		for joueurType in self.jeu.joueurs:
			self.jeu.joueurs[joueurType].grille.addGrille(Settings.grillePlacement[joueurType])

		self.recommencer()

	def updatePosition(self):
		#Cette ligne permet de désactiver le replacement automatique de la fenêtre
		if(Settings.enableWindowUpdate):
			return;
		
		#Taille actuelle de la fenêtre
		h = Settings.window.winfo_height()
		w = Settings.window.winfo_width()

		#Si la fenêtre n'est pas encore dessiné, on reporte
		#si la hauteur est inférieur à 50, alors on considère qu'elle n'est pas déssinée
		if(h < 50):
			Settings.window.after(50, self.updatePosition)
			return
		# Taille actuelle de l'écran
		ws = Settings.window.winfo_screenwidth() # largeur de l'écran
		hs = Settings.window.winfo_screenheight() # hauteur de l'écran

		# calcul des coordonnées du point en haut à gauche de la fenêtre
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)

		# set the dimensions of the screen
		# and where it is placed
		Settings.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def createBateauxButtons(self):
		#on initialise à None pour pouvoir gérer le placement des boutons relativement au bouton précédent (option "_in" de la méthode "place")
		#et évidemment, le premier bouton n'a pas de précédent, et donc il sera placé relativement à la fenêtre (absence de l'option "_in")
		lastShip = None
		if('boutonBateau' in self.elements.keys()):
			for bouton in self.elements['boutonBateau'].values():
				bouton.destroy();
		self.elements['boutonBateau'] = {}
				
		for bateau in self.jeu.getBateaux():
			self.elements['boutonBateau'][bateau] = Button(Settings.window, text=bateau, command=lambda  currentBateau = bateau:
				self.placerBateau(bateauName = currentBateau, joueurType = Joueur.JOUEUR_HUMAIN)
			)
			
			if(None == lastShip):
				self.elements['boutonBateau'][bateau].place(relx=0.5, rely=0.2, anchor= CENTER, relwidth=0.4)
			else :
				self.elements['boutonBateau'][bateau].place(in_=self.elements['boutonBateau'][lastShip], relx=0.5, anchor= CENTER, rely=1.5, relwidth=1, bordermode='outside')
			lastShip = bateau
		#On ajoute un bouton de validation du placement des bateaux
		self.elements['boutonBateau']['validerPlacement'] = Button(Settings.window, text='Valider', command=lambda : 
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
		
		self.jeu.joueurs[joueurType].grille.unbindClic()
		for bateau in self.jeu.joueurs[joueurType].grille.bateaux.values():
			bateau.unbindMove(self.jeu.joueurs[joueurType].grille)
		self.jeu.joueurs[joueurType].getAdversaire(self.jeu.joueurs).grille.bindClic(self.jeu.attaquer)
			

	def recommencer(self):
		self.elements['messageHumain'].configure(text=Settings.defaultHumainName)
		self.jeu.recommencer()
		if('boutonBateau' in self.elements.keys()):
			for bouton in self.elements['boutonBateau'].values():
				bouton.configure(state = NORMAL);

	def message(self, text):
		messagebox.showinfo(Settings.title, text)

	def winner(self, joueur):
		self.unbindAll()
		self.message('Bravo ' + joueur.name + ' tu as gagné!')




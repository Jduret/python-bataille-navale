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

		self.elements['messageStatus'] = Label(Settings.window, text='Placez vos bateaux')
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

		self.recommencer()

	def updatePosition(self):
		return;
		#Current size
		h = Settings.window.winfo_height()
		w = Settings.window.winfo_width()

		#Si la fenêtre n'est pas encore dessiné, on reporte
		if(h < 50):
			Settings.window.after(50, self.updatePosition)
			return
		# get screen width and height
		ws = Settings.window.winfo_screenwidth() # width of the screen
		hs = Settings.window.winfo_screenheight() # height of the screen

		# calculate x and y coordinates for the Tk root window
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)

		# set the dimensions of the screen
		# and where it is placed
		Settings.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def	eventToPoint(self, event):
		abscisse = event.x
		ordonnee = event.y
		l = (ordonnee-Settings.epaisseurTrait)//Settings.tailleCase
		c = (abscisse-Settings.epaisseurTrait)//Settings.tailleCase
		return [c, l]

	def createBateauxButtons(self):
		lastShip = None
		for bateau in self.jeu.getBateaux():
			if(None == lastShip):
				self.elements['boutonBateau_' + bateau] = Button(Settings.window, text=bateau, command=lambda currentBateau = bateau: self.selectionBateau(bateauName = currentBateau))
				self.elements['boutonBateau_' + bateau].place(relx=0.5, rely=0.2, anchor= CENTER, relwidth=0.4)
			else :
				self.elements['boutonBateau_' + bateau] = Button(Settings.window, text=bateau, command=lambda  currentBateau = bateau: self.selectionBateau(bateauName = currentBateau))
				self.elements['boutonBateau_' + bateau].place(in_=self.elements['boutonBateau_' + lastShip], relx=0.5, anchor= CENTER, rely=1.5, relwidth=1, bordermode='outside')
			lastShip = bateau

	def recommencer(self):
		self.elements['messageHumain'].configure(text=Settings.defaultHumainName)
		self.jeu.recommencer()

		#juste pour test, sera retiré par la suite
		#il faut appeler ces méthodes au bon moment
		#self.bindPlacementBateaux()
		#self.bindAttaque()

	def message(self, text):
		messagebox.showinfo(Settings.title, text)

	def winner(self, joueur):
		self.unbindAll()
		self.message('Bravo ' + joueur.name + ' tu as gagné!')




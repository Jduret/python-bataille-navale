##----- Importation des Modules -----##
from __future__ import generators
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import string
import os
#Attention, on importe pas tous car os conteint AUSSI une méthode open
#from os import *
from copy import *
from random import *
from math import *
from sys import *
from jdev4u.settings import *


class Plateau:
	#instance de Tk
	window = None
	#instance de Jeu	
	jeu = None
	bateauText = None
	
	#Dans ce tableau on va placer tous les éléments graphique nécessaire à l'interface
	elements = {}
	
	def __init__(self, window, batailleNavale):
		self.window = window
		self.jeu = batailleNavale
		self.bateauText = StringVar()
		self.bateauText.set('')
		
		self.elements['figuresGrilleHumain'] = []
		self.elements['figuresGrillePc'] = []
		
		##----- Zones de texte -----##
		self.elements['messagePc'] = Label(self.window, text='Joueur PC')
		self.elements['messagePc'].grid(row = 2, column = 0, padx=3, pady=3, sticky = W+E)

		self.elements['messageHumain'] = Label(self.window, text=Settings.defaultHumainName)
		self.elements['messageHumain'].grid(row = 2, column = 2, padx=3, pady=3, sticky = W+E)
		
		#Boutons
		self.elements['boutonQuitter'] =  Button(self.window, text='Quitter', command = self.window.destroy)
		self.elements['boutonQuitter'].grid(row = 4, column = 2, padx = 3, pady = 3,sticky=S+W+E)
		
		self.elements['boutonRecommencer'] = Button(self.window, text='Nouvelle partie', command=self.recommencer)
		self.elements['boutonRecommencer'].grid(row = 4, column = 0, padx = 3, pady = 3, sticky = S+W+E)
		
		def askName():
			answer = simpledialog.askstring('Nouveau nom', self.window)
			self.elements['messageHumain'].configure(text=answer)
			
		self.elements['boutonChangeNom'] = Button(self.window, text='Changer nom', command=askName)
		self.elements['boutonChangeNom'].grid(row = 4, column = 1, padx = 3, pady = 3, sticky = S+W+E)
		
		def test(self, bateauName):
			self.bateauText.set(bateauName)
			c=l=2
			largeur = Settings.tailleCase*c+Settings.tailleRond
			hauteur = Settings.tailleCase*l+Settings.tailleRond
			tailleBateau = 5
			
			if( 'bateauxGrilleHumain' in self.elements and len(self.elements['bateauxGrilleHumain']) > 0) : #mouvement du bateau
				#self.elements['grilleHumain'].delete(self.elements['bateauxGrilleHumain'][len(self.elements['bateauxGrilleHumain'])-1])
				hauteur = hauteur + (tailleBateau*Settings.tailleCase)
				
				self.elements['grilleHumain'].coords(self.elements['bateauxGrilleHumain'][len(self.elements['bateauxGrilleHumain'])-1], 
					Settings.tailleCase*c+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
					Settings.tailleCase*l+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond, 
					largeur, 
					hauteur, 
				)
			else :#creation du bateau
				self.elements['bateauxGrilleHumain'] = []
				largeur = largeur + (tailleBateau*Settings.tailleCase)
				
				self.elements['bateauxGrilleHumain'].append(self.elements['grilleHumain'].create_oval(
					Settings.tailleCase*c+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
					Settings.tailleCase*l+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond, 
					largeur, 
					hauteur, 
					width = Settings.epaisseurMarques, outline = 'chocolate', fill='chocolate')
				)
				
		self.elements['TextTest'] = Label(self.window, text='Placement bateau :')
		self.elements['TextTest'].place(relx=0.5, rely=0.1, anchor= CENTER, relwidth=0.4)
		self.elements['TextTest2'] = Label(self.window, textvariable=self.bateauText)
		self.elements['TextTest2'].place(in_=self.elements['TextTest'], relx=0.5, rely=1,  bordermode='outside')
		
		
		self.elements['boutonTest'] = Button(self.window, text='test', command=lambda: test(self, bateauName = 'test0'))
		self.elements['boutonTest'].place(relx=0.5, rely=0.2, anchor= CENTER, relwidth=0.4)
		
		self.elements['boutonTest2'] = Button(self.window, text='test2', command=test)
		self.elements['boutonTest2'].place(in_=self.elements['boutonTest'], relx=0.5, anchor= CENTER, rely=1.5, relwidth=1, bordermode='outside')

		self.elements['boutonTest3'] = Button(self.window, text='test3', command=test)
		self.elements['boutonTest3'].place(in_=self.elements['boutonTest2'], relx=0.5, anchor= CENTER, rely=1.5, relwidth=1, bordermode='outside')

		self.elements['boutonTest4'] = Button(self.window, text='test4', command=test)
		self.elements['boutonTest4'].place(in_=self.elements['boutonTest3'], relx=0.5, anchor= CENTER, rely=1.5, relwidth=1, bordermode='outside')

		self.elements['boutonTest5'] = Button(self.window, text='test5', command=test)
		self.elements['boutonTest5'].place(in_=self.elements['boutonTest4'], relx=0.5, anchor= CENTER, rely=1.5, relwidth=1, bordermode='outside')

		#Grilles
		self.elements['grillePc']= self.createGrille()
		self.elements['grillePc'].grid(row = 1, column = 0, columnspan = 1, padx = 5, pady = 5)
		
		self.elements['grilleHumain'] = self.createGrille()
		self.elements['grilleHumain'].grid(row = 1, column = 2, columnspan = 1, padx = 5, pady = 5)
		
		self.recommencer()
		
	def updatePosition(self):
		#Current size
		h = self.window.winfo_height()
		w = self.window.winfo_width()
		
		#Si la fenêtre n'est pas encore dessiné, on reporte
		if(h < 50):
			self.window.after(50, self.updatePosition)
			return
		# get screen width and height
		ws = self.window.winfo_screenwidth() # width of the screen
		hs = self.window.winfo_screenheight() # height of the screen

		# calculate x and y coordinates for the Tk root window
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)

		# set the dimensions of the screen 
		# and where it is placed
		self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
		
	def bindPlacementBateaux(self):
		self.elements['grilleHumain'].bind('<Button-1>',self.placerBateau)

	def unbindAll(self):
		self.unbindAttaque()
		self.unbindPlacement()
		
	def unbindAttaque(self):
		self.elements['grillePc'].unbind('<Button-1>')
	def unbindPlacement(self):
		self.elements['grilleHumain'].unbind('<Button-1>')
	
	def bindAttaque(self):
		self.elements['grillePc'].bind('<Button-1>', self.attaquer)
	
	def attaquer(self, event):
		result = self.jeu.attaquer(self.elements['grillePc'], event)
		if result == 'touche':
			self.placerTouche(self.elements['grillePc'], event)
		elif result == 'aleau':
			self.placerAleau(self.elements['grillePc'], event)
	
	def createGrille(self):
		largeur = Settings.tailleCase*Settings.tailleGrille + Settings.epaisseurTrait
		grille = Canvas(self.window, bg=Settings.couleurFondGrille, width=largeur, height=largeur)
		for i in range(Settings.tailleGrille +1):
			grille.create_line(
				0, 
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2), 
				largeur, 
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2), 
				width=Settings.epaisseurTrait)
				
			grille.create_line(
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2), 
				0, 
				Settings.tailleCase*i+(Settings.epaisseurTrait / 2), 
				largeur, 
				width=Settings.epaisseurTrait)
		return grille
		
	def placerBateau(self, event):
		abscisse = event.x
		ordonnee = event.y
		
		l = (ordonnee-Settings.epaisseurTrait)//Settings.tailleCase
		c = (abscisse-Settings.epaisseurTrait)//Settings.tailleCase 
		lettre = list(string.ascii_uppercase)
		self.message('Placement ' + lettre[c] + str(l+1))
		self.elements['figuresGrilleHumain'].append(self.elements['grilleHumain'].create_oval(
			Settings.tailleCase*c+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
			Settings.tailleCase*l+Settings.tailleCase + (2*Settings.epaisseurTrait)- Settings.tailleRond, 
			Settings.tailleCase*c+Settings.tailleRond, 
			Settings.tailleCase*l+Settings.tailleRond, 
			width = Settings.epaisseurMarques, outline = 'chocolate'))
		#self.jeu.positionnerBateaux(lettre[c]+str(l+1), )
	
	def placerAleau(self, grille, event):
		abscisse = event.x
		ordonnee = event.y
		
		l = (ordonnee-Settings.epaisseurTrait)//Settings.tailleCase
		c = (abscisse-Settings.epaisseurTrait)//Settings.tailleCase 
		
		self.elements['figuresGrillePc'].append(grille.create_line(
			((Settings.tailleCase)*c) + Settings.epaisseurTrait, 
			((Settings.tailleCase)*l)+ Settings.epaisseurTrait,
			((Settings.tailleCase)*(c+1)) + Settings.epaisseurTrait, 
			((Settings.tailleCase)*(l+1))+ Settings.epaisseurTrait,
			width = Settings.epaisseurMarques, fill = 'white'))
		self.elements['figuresGrillePc'].append(grille.create_line(
			((Settings.tailleCase)*(c+1)) + Settings.epaisseurTrait, 
			((Settings.tailleCase)*l)+ Settings.epaisseurTrait,
			((Settings.tailleCase)*c) + Settings.epaisseurTrait, 
			((Settings.tailleCase)*(l+1))+ Settings.epaisseurTrait,
			width = Settings.epaisseurMarques, fill = 'white'))
		
	def placerTouche(self, grille, event):
		abscisse = event.x
		ordonnee = event.y
		
		l = (ordonnee-Settings.epaisseurTrait)//Settings.tailleCase
		c = (abscisse-Settings.epaisseurTrait)//Settings.tailleCase 
		self.elements['figuresGrillePc'].append(grille.create_oval(
			Settings.tailleCase*c+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
			Settings.tailleCase*l+Settings.tailleCase + (2*Settings.epaisseurTrait) - Settings.tailleRond, 
			Settings.tailleCase*c+Settings.tailleRond, 
			Settings.tailleCase*l+Settings.tailleRond, 
			width = Settings.epaisseurMarques, outline = 'red'))
		
	def recommencer(self):
		for figure in self.elements['figuresGrilleHumain']:
			self.elements['grilleHumain'].delete(figure)
		for figure in self.elements['figuresGrillePc']:
			self.elements['grillePc'].delete(figure)
				
		self.elements['messageHumain'].configure(text=Settings.defaultHumainName)
		self.jeu.recommencer()
		
		#juste pour test, sera retiré par la suite
		#il faut appeler ces méthodes au bon moment
		self.bindPlacementBateaux()
		self.bindAttaque()
		
	def message(self, text):
		messagebox.showinfo(Settings.title, text)
		
	def winner(self, joueur):
		self.unbindAll()
		self.message('Bravo ' + joueur.name + ' tu as gagné!')
		
		
		
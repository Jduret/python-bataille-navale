__licence__ = "Apache-2.0"
__author__  = "Jérôme Plotton, Antoine Femenias, Lydie Riche"

##----- Importation des Modules -----##
from tkinter import *
from bn.settings import *
from bn.plateau import *
from bn.jeu import *

#Initalisation du jeu

Settings.window = root = Tk()
root.title(Settings.title)
#on empêche la modification de la taille de fenêtre
root.resizable(0,0)
#on cache les boutons de fermeture reduction et maximisation
root.overrideredirect(1)

graphic = Plateau(Jeu())

#Une fois les graphiques ajoutés à la fenêtre, on la déplace au centre
root.after(50, graphic.updatePosition)

#sous pyzo la boucle d'attente est déjà lancée
root.mainloop()  # Boucle d'attente des evenements

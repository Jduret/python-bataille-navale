##----- Importation des Modules -----##
from tkinter import *
from jdev4u.settings import *
from jdev4u.plateau import *
from jdev4u.jeu import *

#Initalisation du jeu

Settings.window = root = Tk()
root.title(Settings.title)
#on empêche la modification de la taille de fenêtre
root.resizable(0,0)
#on cache les boutons de fermeture reduction et maximisation
root.overrideredirect(1)

graphic = Plateau(Jeu())

#Une fois les graphique ajouté à la fenêtre, on la déplace au centre
root.after(50, graphic.updatePosition)

#sous pyzo la boucle d'attente est déjà lancé
root.mainloop()  # Boucle d'attente des evenements
#pas de exit pour pyzo
#sys.exit(0) 	
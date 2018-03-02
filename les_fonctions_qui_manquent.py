import os
from random import *

grillePC=[[0]*10]*10

#correspond à la méthode Grille.isIn
def est_dans_la_grille(case,grille): # case sous forme de tuple
    if case[0]<len(grille) and case[1]<len(grille):
        return True
    else:
        return False

def placer_bateau(valeur,grille):
    l=randint(0,9)
    c=randint(0,9)
    print ("la case se situe a ",l,c)
    #print ("la grille etait ",grille)
    grille_modifiee=grille.copy()
    taille=valeur
    direction=randint(0,1) #0 pour vers le bas, 1 pour vers la droite
    print ("la case contient la valeur ",grille_modifiee[l][c])
    print("la direction est (0 nord,1 est) ",direction)
    if direction==0:
        while taille>0:
            if grille_modifiee[l][c]==0 and est_dans_la_grille((l,c),grille_modifiee):
                grille_modifiee[l][c]=valeur
                taille-=1
                l=l+1
            else:
                break
                placer_bateau(valeur,grille)
            
    else:
        while taille>0:
            if grille_modifiee[l][c]==0 and est_dans_la_grille((l,c),grille_modifiee):
                grille_modifiee[l][c]=valeur
                taille-=1
                c=c+1
            else:
                break
                placer_bateau(valeur,grille)
            print ("la grille est maintenant ",grille_modifiee)
    return grille_modifiee

def placement_aleatoire(grille):
    fichier=open("C:/Users/Lydie/Desktop/rapport projet/python/include/bateaux.txt",'r')
    bateaux={}
    for ligne in fichier:
        name,size=ligne.split(';')
        bateaux[name]=size
        #print (bateaux)
    for valeur in bateaux.values():
        valeur=int(valeur)
        print ("la taille du bateau est ",valeur)
        placer_bateau(valeur,grille)
        
        
placement_aleatoire(grillePC)
print (grillePC)

grille_test=[
[0,2,0,0,0,0,0,0,0,0],
[0,2,0,0,3,3,3,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,3,0],
[0,0,0,0,0,0,0,0,3,0],
[0,0,0,0,4,4,4,4,3,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,5,5,5,5,5,0,0],
[0,0,0,0,0,0,0,0,0,0]]
print ("la grille de test est ",grille_test)

def attaquerPc(grille,compteur):
    c=2*randint(0,4)
    l=2*randint(0,4)+1
    print ("la case attaquée est en (",l,",",c,")")
    if grille[l][c]==0:
        print ("à l'eau")
        return "à l'eau"
    else:
        if coule(compteur):
            print ("coulé")
            return "coule"
        else:
            print ("touché")
            return "touché"

def coule(compteur):
    
        
attaquerPc(grille_test)
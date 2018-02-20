from joueur import*
import random

scores=recup_scores()
utilisateur=recup_nom_utilisateur()
if utilisateur not in scores.keys():
    scores[utilisateur]=0
if Joueur.toucheCoule(scores):
    scores+=1
else:
    JoueurPc.toucheCoule(scores)+=1 #peut etre faudra-t-il mettre un compteur pour connaitre le nombre de parties jouees avec le meme joueur


def cases_ajacentes(abscisse_case,ordonnee_case):
    cases_adjacentes=[(abscisse_case+1,ordonnee_case),(abscisse_case-1,ordonnee_case),(abscisse_case,ordonnee_case+1),(abscisse_case,ordonnee_case-1)
    
def attaque_pc(case):
    if case==Touche:
        case_a_tester=choice(case) in case_adjacentes
    return case_a_tester

def placerpc(self,fichierPath = 'include/bateaux.txt'):
    l = randint(0,9) # tirage aleatoire de la premiere case du porteavion de quatre cases
    c = randint(0,9) # pour le pc, comme il ne va pas faire le placement de manière visuelle, il ne sert a rien de faire du getBateau
    file = open(os.path.join(Settings.__location__, fichierPath), 'r')
    for ligne in file:
        name, size = ligne.split(';')
    if grille[l][c]==0:
        grille[l][c]=size
        directionBateau=[N,S,E,O]
        dirChoisie=choice(directionBateau)
        for i<size-1: #on choisit une direction et on vérifie que les cases sont vides sinon on relance le choix aléatoire jusqu'a avoir qqch de bon mais il faudra que si ca marche pas au nord je fasse une vérif au su et pareil pour est ouest 
            if dirChoisie=='N':
                if grille[l-i][c]!=0:
                    placerpc((self,fichierPath = 'include/bateaux.txt')
                else:
                    grille[l-i][c]=size
            elif dirChoisie=='S':
                if grille[l+i][c]!=0:
                    placerpc((self,fichierPath = 'include/bateaux.txt')
                else:
                    grille[l+i][c]=size
            elif dirChoisie=='E':
                if grille[l][c+i]!=0
                    placerpc((self,fichierPath = 'include/bateaux.txt')
                else:
                    grille[l][c+i]=size
            else:
                if grille[l][c-i]!=0:
                    placerpc((self,fichierPath = 'include/bateaux.txt')
                else:
                    grille[l][c-i]=size
    return grille,Bateau

def attaquer(self,grille,event):
    abscisse=event.x
    ordonnee=event.y
    if (abscisse,ordonnee) in getBateau:
        return "Touche"
        del getBateau(abscisse,ordonnee)
    else:
        return "A l'eau"

def gagner(self):
    if attaquer (self,grille,event)=='Touche':
        if getBateau=={}:
            return 'ToucheCoule'
        else :
            return 'Touche'

#a rajouter dans la definition des bateaux de l'humain
if calculDimensions not in grille:
    return Error    
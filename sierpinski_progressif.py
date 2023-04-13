#! /usr/bin/env python
# -*- coding:Utf8 -*-

# Détection et positionnement d'un clic de souris dans une fenêtre :

# Suivant que l'on exécute ce script sous Python 3 ou Python 2,
# on utilisera le module Tkinter correspondant :
try:
    from tkinter import *      # module Tkinter pour Python 3
except:
    from Tkinter import *      # module Tkinter pour Python 2
    
from random import randrange
from math import *
from threading import Thread
import time

global compteur_dimension
global couleur_points_depart
global coord_points_depart
global coord_point_courant
global nombre_iterations
global ligne_courante
global en_marche
global indice_iteration
global montemps
global ponderation_eloignement

dimension = 3
compteur_dimension = 0
rayon_point = 2
couleur_points_depart = 'red'
nombre_iterations = 50000 # (50000 suffit mais peut être plus grand si on a le temps de pousser l'expérience et on peut toujours stopper le programme...)
coord_points_depart = []
coord_point_courant = 0,0
indice_iteration = 0
montemps = 0
ponderation_eloignement = 0.5 # coefficient de pondération d'éloignement entre 0 et 1 (normalement vaut 0,5 pour dimension=3, à optimiser pour les autres : pour 5, ~.61, pour 7, ~.69 ?...)
ponderation_rapprochement = 1 - ponderation_eloignement
hauteur_cadre = 850
largeur_cadre = 900
marge_cadre = 30

def sierpinski() :
    global coord_points_depart
    global coord_point_courant
    global ligne_courante
    global en_marche
    global indice_iteration
    global montemps

    montemps=time.time()
    temps_repos = .8 # en secondes
    duree_affichage_lent = 8
    duree_affichage = 200
    en_marche = True
    un_affichage_sur = 100000
    while indice_iteration in range(nombre_iterations) and en_marche :
        extremite = randrange(dimension) # tirage du sommet à considérer
        if indice_iteration<=duree_affichage :   # on n'affiche le processus que sur les premiers points...
            cadre.coords(ligne_courante,coord_points_depart[extremite]+coord_point_courant) # Concaténation de tuples !
            time.sleep(temps_repos) # On affiche ce qui se passe au début...
            if indice_iteration==duree_affichage_lent : # (plus lentement au début...)
                temps_repos = temps_repos / 5
            elif indice_iteration==duree_affichage :
                cadre.delete(ligne_courante)
                
##        elif i%un_affichage_sur==0 : # une fois sur 10 (pour gagner du temps), on "coupe" le thread pour permettre l'affichage...
##            time.sleep(.0000015) # Temps_mort pour laisser l'affichage se faire (1ms n'est pas assez alors je donne 1,5ms)
#### Apparemment ce n'est pas la peine puisqu'ainsi l'affichage se fait bien... (boucle while au lieu de for ????!!!!).......
#### La boucle while a tout de même apparemment l'inconvénient d'être beaucoup plus lente (à cause de la variable globale indice_iteration ?)...
                
        coord_point_courant = coord_points_depart[extremite][0] * ponderation_eloignement + coord_point_courant[0] * ponderation_rapprochement ,\
                              coord_points_depart[extremite][1] * ponderation_eloignement + coord_point_courant[1] * ponderation_rapprochement
        cadre.create_rectangle(coord_point_courant,coord_point_courant,fill='black')
        indice_iteration += 1
    if en_marche :
        chaine = 'terminée en'
    else :
        chaine = 'stoppée à'
    print('Exécution',chaine,(time.time()-montemps),'secondes pour',indice_iteration,'itérations')
       


def pointeur(event) :
    global compteur_dimension
    global couleur_points_depart
    global coord_points_depart
    global coord_point_courant
    global indice_iteration
    
    if compteur_dimension <= dimension :
        x = event.x
        y = event.y
        
        if compteur_dimension == dimension :
            couleur_points_depart = 'blue'
            coord_point_courant = x,y
        else :
            coord_points_depart.append((x,y))
            
        cadre.create_oval(x-rayon_point,y-rayon_point,x+rayon_point,y+rayon_point,fill=couleur_points_depart)
        
        if compteur_dimension == dimension :
            t = Thread(target=sierpinski)
            t.start()
            
        compteur_dimension += 1
    else :
        print('Exécution en cours,',(time.time()-montemps),'secondes écoulées pour',indice_iteration,'itérations')

        

def stopper(event) :
    global en_marche
    global montemps
    
    en_marche = False
    
      
print('Clic-gauche',dimension+1,'fois pour choisir les points sur la fenêtre, les clics-gauche suivants donnent le temps...')      
print('Puis clic-droit pour stopper le programme')
fen = Tk()
cadre = Canvas(fen, width =largeur_cadre, height =hauteur_cadre, bg="light yellow")
ligne_courante = cadre.create_line(0,0,0,0,fill='orange')

# affichage d'une mire
angle_suiv = 0
rayon = 200
delta_angle = 360 / dimension
for i in range(dimension) :
    angle = angle_suiv
    angle_suiv = angle_suiv + delta_angle
    coord_arc = marge_cadre, marge_cadre, min(largeur_cadre,hauteur_cadre)-marge_cadre, min(largeur_cadre,hauteur_cadre)-marge_cadre
    cadre.create_arc(coord_arc,start=angle, extent=angle_suiv,outline='purple',dash=(1,10))
cadre.bind("<Button-1>", pointeur)
cadre.bind("<Button-3>", stopper)
cadre.pack()

fen.mainloop()



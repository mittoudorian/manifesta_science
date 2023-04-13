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

import time
from math import *

global compteur_dimension
global couleur_points_depart
global coord_points_depart
global coord_point_courant
global nombre_iterations
global ligne_courante
global ponderation_eloignement

dimension = 3
compteur_dimension = 0
rayon_point = 2
couleur_points_depart = 'red'
nombre_iterations = 100000
coord_points_depart = []
coord_point_courant = 0,0
ponderation_eloignement = .5 # coefficient de pondération d'éloignement entre 0 et 1 (normalement vaut 0,5 pour dimension=3, à optimiser pour les autres : pour 5, ~.61, pour 7, ~.69 ?...)
ponderation_rapprochement = 1 - ponderation_eloignement
hauteur_cadre = 850
largeur_cadre = 900
marge_cadre = 30

def pointeur(event):
    global compteur_dimension
    global couleur_points_depart
    global coord_points_depart
    global coord_point_courant
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
            sierpinski()
        compteur_dimension += 1
            
def sierpinski() :
    global coord_points_depart
    global coord_point_courant
    global ligne_courante
    for i in range(nombre_iterations):
        extremite = randrange(dimension)
        # couleur différente pour les premiers points
        if i<10 : couleur = 'red'
        else : couleur = 'black'
        # tuple de coordonnées
        coord_point_courant = coord_points_depart[extremite][0] * ponderation_eloignement + coord_point_courant[0] * ponderation_rapprochement ,\
                              coord_points_depart[extremite][1] * ponderation_eloignement + coord_point_courant[1] * ponderation_rapprochement
        cadre.create_rectangle(coord_point_courant,coord_point_courant,outline=couleur)    

fen = Tk()
cadre = Canvas(fen, width =largeur_cadre, height =hauteur_cadre, bg="light yellow")
angle_suiv = 0
delta_angle = 360 / dimension
for i in range(dimension):
    angle = angle_suiv
    angle_suiv = angle_suiv + delta_angle
    coord_arc = marge_cadre, marge_cadre, min(largeur_cadre,hauteur_cadre)-marge_cadre, min(largeur_cadre,hauteur_cadre)-marge_cadre
    cadre.create_arc(coord_arc,start=angle, extent=angle_suiv,outline='purple',dash=(1,10))
cadre.bind("<Button-1>", pointeur)
cadre.pack()
chaine = Label(fen)
chaine.pack()

fen.mainloop()



#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------------------------------------------------------------

"""
Programme : Station météo
Auteur : jmetra
Version : 06a
Date : 10.09.2017

Ce programme affiche sur un display 2x16 caractères les prévisions météorologiques.

Sur la première ligne sont afichés le jour de la semaine et la date ainsi que les
températures minimales et maximales prévues et sur la deuxième lignes est donnée
la prévision météorologique en bref.

Le lieu pour lequel la prévision est faite peut être choisi par l'utilisateur dans une
liste proposée par le programmeur en pressant sur les boutons <GAUCHE et <DROITE>

La prévision est actualisée lors du lancement de l'application, lors de la pression
sur le bouton <SELECT> ou <GAUCHE> ou <DROITE>

Le programme permet également en pressant sur les boutons <HAUT> et <BAS> d'afficher la
prévision météo du jour précédent et respectivement du jour suivant.

Les informations météo sont downloadée depuis le site internet https://www.wunderground.com/
au moyen d'une clé que chaque utilisateur devra obtenir car pour chaque clé, le nombre de prévisions
obtenues gratuitement est limité.
   - la clé doit être introduite dans le code ci-après et assignéeà la variable <sKey>
   - l'URL est fourni par le site Wunderground.com et doit être assigné à la variable <sURL>
"""

#---------------------------------------------------------------------------------------------------------------------------------
# importation des librairies nécessaires
import urllib2
import json
import requests
import time
import Adafruit_CharLCD as LCD
import unicodedata

#---------------------------------------------------------------------------------------------------------------------------------
#initialisations des variables

# info site wunderground qui fournit les prévisions météo pour le monde entier
sKey = "d49b0a2fb656398f" # clé fournie par le site internet de prévision météo https://www.wunderground.com/
sDemand = "forecast" # la demande pourrait aussi être "forecast10day" pour afficher la prévision sur 10 jours
sUrl = "http://api.wunderground.com/api" # url pour la demande

# assignation du display à la variable lcd 
lcd = LCD.Adafruit_CharLCDPlate()

# création des listes pour les différents lieux pour lesquel on veut pouvoir afficher les prévisions météo
lLieux = [
   ["CH", "Sion", "FR"],
   ["IT", "Todi", "IT"],
   ["ES", "la Garriga", "SP"],
   ["GB", "London", "EN"],
   ["Canada", "Montreal", "FR"],
   ["Australia", "Sydney", "EN"],
   ["CA", "San Francisco", "EN"],
   ["Germany", "Berlin", "DL"]]

# Listes des couleurs
lCouleurs = [
   [1.0, 0.0, 0.0, "RED"],
   [0.0, 1.0, 0.0, "GREEN"],
   [0.0, 0.0, 1.0, "BLUE"],
   [1.0, 1.0, 0.0, "YELLOW"],
   [0.0, 1.0, 1.0, "CYAN"],
   [1.0, 0.0, 1.0, "MAGENTA"],
   [1.0, 1.0, 1.0, "WHITE"]]

#buttons 
buttons = (LCD.SELECT, LCD.RIGHT, LCD.DOWN, LCD.UP, LCD.LEFT)

# indexes
iLieuxPays = 0 # index des pays dans la liste lLieux
iLieuxVille = 1 # index de la ville dans la liste lLieux
iLieuxLangue = 2 # index de la langue dans la liste lLieux

iLieuChoisi = 0 # 0=Sion, 1=Todi, ...
iJourChoisi = 1 # 0=aujourd'hui, 1=demain , ...
iCouleurChoisie = 6 #  0=reed , ... 6=white

#---------------------------------------------------------------------------------------------------------------------------------
# fonctions nécessaires au fonctionnement du programme

# fonction qui permet de supprimer les lettres accentuées dans un string
# car le display ne peut pas afficher des lettres accentuées
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
# fonction qui lit et retourne les données du lieu choisi dans la liste <iLieux> en fonction de l'index <iPlace>
def select_place(iPlace):
   return lLieux[iPlace][iLieuxPays], lLieux[iPlace][iLieuxVille], 'lang:' + lLieux[iPlace][iLieuxLangue]

# fonction qui questionne le site wunderground.com et retoune la prévision
def get_forecast (iPlace):

   sCountry, sCity, sLanguage = select_place(iPlace) # assignation des valeurs pays, ville et langue aux variables
   # questionnement du site wunderground,com
   r = requests.get(sUrl + "/" + sKey + "/" + sDemand + "/" + sLanguage + "/q/" + sCountry + "/" + sCity +".json")
   sForecast = r.json()


   # boucle pour parcourir les prévisions jour après jour (4 jours pour forecast)
   
   retForecast = [] # initialisation de la liste des prévision
   for day in sForecast['forecast']['simpleforecast']['forecastday']:

      # création du string date et températures
      str1 = strip_accents(day['date']['weekday'][0:2] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius'])

      # création du string de prévision
      str2 = strip_accents(day['conditions'])

      # si le string contient plus de 16 caractères alors on raccourcit le premier mot en principe mais le dernier en anglais et allemand
      if len(str2) > 16 :
         if sLanguage == "lang:EN" or sLanguage == "lang:DL" :
            str31 = str2.split()
            str3 = str31[len(str31)-1]
            str2 = str2[0:9] + " " + str3[0:4] + "."
         else :
            str3 = str2.split()[0]
            str2 = str3[0:15-len(str2)] + "." + str2[len(str3):]

      # le string final pour l'affichage = str1 + saut de ligne + str2
      strx = str1 + "\n" + str2
      # et on renvoie le string préparé
      retForecast += [strx]

   return retForecast

#---------------------------------------------------------------------------------------------------------------------------------
# PROGRAMME PRINCIPAL

lcd.clear()
lForecast = get_forecast(iLieuChoisi)
lcd.message(lForecast[iJourChoisi])

# impression utile pendant la phase de mise au point du programme
print lLieux[iLieuChoisi][iLieuxVille] + " / " + lLieux[iLieuChoisi][iLieuxLangue]
print lForecast[iJourChoisi]
print "------------------"

# boucle sans fin <CTRL-C> pour quitter le programme
while True:
   
    # boucle sur tous les boutons et contrôle si un est pressé
    for button in buttons:

       # un bouton est-il pressé ?
       if lcd.is_pressed(button): 

          # actualise les données et les affiche
          if button == 0 : # SELECT
             iJourChoisi=1 # 0 = aujourd'hui, 1 = demain , ...
             lForecast = get_forecast(iLieuChoisi)

          # sélectionne le lieu suivant dans la liste iLieux
          elif button == 1: # RIGHT
             iLieuChoisi += 1
             if iLieuChoisi >= len(lLieux) :
                iLieuChoisi = 0
             lForecast = get_forecast(iLieuChoisi)

          # sélectionne le jour suivant   
          elif button == 2: # DOWN
             iJourChoisi -= 1
             if iJourChoisi < 0 :
                iJourChoisi = len(lForecast) - 1
             lForecast = get_forecast(iLieuChoisi)

          # sélectionne le jour précédent   
          elif button == 3: # UP
             iJourChoisi += 1
             if iJourChoisi >= len(lForecast) :
                iJourChoisi = 0
             lForecast = get_forecast(iLieuChoisi)

          # change la couleur de l'affichage   
          elif button == 4: # LEFT
             iCouleurChoisie += 1
             if iCouleurChoisie >= len(lCouleurs) :
                iCouleurChoisie = 0

          # sette la couleur de l'affichage      
          lcd.set_color(lCouleurs[iCouleurChoisie][0],lCouleurs[iCouleurChoisie][1],lCouleurs[iCouleurChoisie][2])
          # efface l'affichage
          lcd.clear()
          # affiche le nom de la ville et la langue sur le display pour 1 seconde
          lcd.message(lLieux[iLieuChoisi][iLieuxVille] + " / " + lLieux[iLieuChoisi][iLieuxLangue])
          time.sleep(1)
          # efface le display
          lcd.clear()
          # affiche la prévision météo
          lcd.message(lForecast[iJourChoisi])

          # impression utile pendant la phase de mise au point du programme
          print lLieux[iLieuChoisi][iLieuxVille] + " / " + lLieux[iLieuChoisi][iLieuxLangue]
          print lForecast[iJourChoisi]
          print "------------------"
          
    time.sleep(0.2)

# Fin du programme
#---------------------------------------------------------------------------------------------------------------------------------

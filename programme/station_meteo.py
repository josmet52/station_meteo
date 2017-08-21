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

Usage des boutons :
   <SELECT> mise à jour des informations selon les données par défaut
   <HAUT> prévision pour le prochain jour 
   <DROITE> sélectionne le prochain lieu dans la liste 
   <BAS> sélectionne la prochaine langue dans la liste
   <GAUCHE> sélectionne la prochaine couleur
   Remarque : toutes les actions reprennent au début lorsque la dernière est atteinte

Les informations météo sont downloadée depuis le site internet https://www.wunderground.com/
au moyen d'une clé que chaque utilisateur doit obtenir car pour chaque clé, le nombre de prévisions
obtenues gratuitement est limité.
   - la clé doit être introduite dans le code ci-après et assignée à la variable <wuKey>
   - l'URL est fourni par le site Wunderground.com et doit être assigné à la variable <wuURL>
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
wuKey = "d49b0a2fb656398f" # clé fournie par le site internet de prévision météo https://www.wunderground.com/
wuDemand = "forecast" # la demande pourrait aussi être "forecast10day" pour afficher la prévision sur 10 jours
wuURL = "http://api.wunderground.com/api" # url pour la demande

# assignation du display à la variable lcdDisplay 
lcdDisplay = LCD.Adafruit_CharLCDPlate()

# création des listes pour les différents lieux pour lesquel on veut pouvoir afficher les prévisions météo
placeList = [
   ["CH", "Sion"],
   ["IT", "Todi"],
   ["ES", "la Garriga"],
   ["GB", "London"],
   ["Canada", "Montreal"],
   ["Australia", "Sydney"],
   ["CA", "San Francisco"],
   ["Germany", "Berlin"]]

# indexes
placesCountryIndex = 0 # index des pays dans la liste placeList (colonne 0)
placesCityIndex = 1 # index de la ville dans la liste placeList (colonne 1)

selectedPlace = 0 # 0=Sion, 1=Todi, ...
selectedDay = 1 # 0=aujourd'hui, 1=demain , ...
selectedColor = 6 #  0=reed , ... 6=white

# Listes des couleurs 0=red, 1=green, 2=blue, 3=yellow, 4=cyan, 5=magenta, 6=white
colorList = [
   [1.0, 0.0, 0.0],
   [0.0, 1.0, 0.0],
   [0.0, 0.0, 1.0],
   [1.0, 1.0, 0.0],
   [0.0, 1.0, 1.0],
   [1.0, 0.0, 1.0],
   [1.0, 1.0, 1.0]]

# Liste des langues
languageList = ["FR", "IT", "SP", "CA", "DL", "EN"]
selectedLanguage = 0  # par défaut en francais

#buttonList 
buttonList = [LCD.SELECT, LCD.RIGHT, LCD.DOWN, LCD.UP, LCD.LEFT]

#---------------------------------------------------------------------------------------------------------------------------------
# fonctions nécessaires au fonctionnement du programme

# fonction qui permet de supprimer les lettres accentuées dans un string
# car le display ne peut pas afficher des lettres accentuées
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
# fonction qui questionne le site wunderground.com et retoune la prévision
def get_forecast (iPlace):

   sLanguage = 'lang:' + languageList[selectedLanguage]
   sCountry = placeList[iPlace][placesCountryIndex] 
   sCity = placeList[iPlace][placesCityIndex]
   # questionnement du site wunderground,com
   r = requests.get(wuURL + "/" + wuKey + "/" + wuDemand + "/" + sLanguage + "/q/" + sCountry + "/" + sCity +".json")
   sForecast = r.json()


   # boucle pour parcourir les prévisions jour après jour (4 jours pour forecast)
   
   retForecast = [] # initialisation de la liste des prévision
   for day in sForecast['forecast']['simpleforecast']['forecastday']:

      # création du string date et températures
      str1 = strip_accents(day['date']['weekday_short'] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius'])

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

lcdDisplay.clear()
lForecast = get_forecast(selectedPlace)
lcdDisplay.message(lForecast[selectedDay])

# impression utile pendant la phase de mise au point du programme
print placeList[selectedPlace][placesCityIndex] + " / " + languageList[selectedLanguage]
print lForecast[selectedDay]
print "------------------"

# boucle sans fin <CTRL-C> pour quitter le programme
while True:
   
    # boucle sur tous les boutons et contrôle si un est pressé
    for button in buttonList:

       # un bouton est-il pressé ?
       if lcdDisplay.is_pressed(button): 

          # actualise les données et les affiche
          if button == 0 : # SELECT
             selectedDay=0 # 0 = aujourd'hui
             selectedLanguage = 0 # 0 = francais
             selectedPlace = 0 # 0 = Sion
             selectedColor = 6 # 0 = white
             lForecast = get_forecast(selectedPlace)

          # sélectionne le lieu suivant dans la liste iLieux
          elif button == 1: # RIGHT
             selectedPlace += 1
             if selectedPlace >= len(placeList) :
                selectedPlace = 0
             lForecast = get_forecast(selectedPlace)

          # sélectionne la langue suivante   
          elif button == 2: # DOWN
             selectedLanguage += 1
             if selectedLanguage >= len(languageList) :
                selectedLanguage = 0
             lForecast = get_forecast(selectedPlace)

          # sélectionne le jour précédent   
          elif button == 3: # UP
             selectedDay += 1
             if selectedDay >= len(lForecast) :
                selectedDay = 0
             lForecast = get_forecast(selectedPlace)

          # change la couleur de l'affichage   
          elif button == 4: # LEFT
             selectedColor += 1
             if selectedColor >= len(colorList) :
                selectedColor = 0

          # sette la couleur de l'affichage      
          lcdDisplay.set_color(colorList[selectedColor][0],colorList[selectedColor][1],colorList[selectedColor][2])
          # efface l'affichage
          lcdDisplay.clear()
          # affiche le nom de la ville et la langue sur le display pour 1 seconde
          lcdDisplay.message(placeList[selectedPlace][placesCityIndex] + " / " + languageList[selectedLanguage])
          time.sleep(1)
          # efface le display
          lcdDisplay.clear()
          # affiche la prévision météo
          lcdDisplay.message(lForecast[selectedDay])

          # impression utile pendant la phase de mise au point du programme
          print placeList[selectedPlace][placesCityIndex] + " / " + languageList[selectedLanguage]
          print lForecast[selectedDay]
          print "------------------"
          
    time.sleep(0.2)

# Fin du programme
#---------------------------------------------------------------------------------------------------------------------------------

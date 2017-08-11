#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

#---------------------------------------
# importation des librairies nécessaires
import urllib2
import json
import requests
import time
import Adafruit_CharLCD as LCD
import unicodedata

#-----------------------------
#initialisations des variables

# assignation du display à la variable lcd et effacement du display
lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()

# création des listes pour les différents lieux pour lesquel on veut pouvoir afficher les prévisions météo
lPays = ["CH", "IT", "ES", "GB"]
lVille = ["Sion", "Todi", "la Garriga", "London"]
lLangue = ["lang:FR", "lang:IT", "lang:SP", "lang:EN"]

# choix du lieu par défaut
iLieuChoisi = 0
iNombreLieux = len(lVille)
iJourChoisi = 1 # 0 = auhourd'hui, 1 = demain , ...

# assignation des valeurs aux variables utilisées par la suite
sPays = lPays[iLieuChoisi]
sVille = lVille[iLieuChoisi]
sLang = lLangue[iLieuChoisi]

# clé fournie par le site internet de prévision météo https://www.wunderground.com/
sKey = "67b3e8dedd282c83"
sDemand = "forecast10day" # la demande pourrait aussi être "forecast10day" pour afficher la prévision sur 10 jours
sUrl = "http://api.wunderground.com/api" # url pour la demande

# fin de l'assignation des variable
#----------------------------------

#------------------------------
# fonctions utiles au programme

# fonction qui permet de supprimer les lettres accentuées dans un string
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# fonction qui lit la prévision
def read_forecast(sRequest):
   r = requests.get(sRequest)
   return r.json() # récuper les datas sous forme JavaScript Object Notation (JSON)
   
# fonction qui retourne les valeur du lieu choisi
def select_place(iPlace):
   return lPays[iPlace], lVille[iPlace], lLangue[iPlace]

# fonction qui retoune la prévision
def get_forecast (iPlace):

   sCountry, sCity, sLanguage = select_place(iPlace)
   sForecast = read_forecast(sUrl + "/" + sKey + "/" + sDemand + "/" + sLanguage + "/q/" + sCountry + "/" + sCity +".json")

   # boucle pour parcourir les prévisions une à une
   iDay = 0
   retForecast = []
   for day in sForecast['forecast']['simpleforecast']['forecastday']:

      # création du string date et températures
      str1 = strip_accents(day['date']['weekday'][0:2] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius'])

      # création du string de prévision
      str2 = strip_accents(day['conditions'])

      # si le string contient plus de 16 caractères alors on raccorci le premier mot 
      if len(str2) > 16 :
         str3 = str2.split()[0]
         str2 = str3[0:15-len(str2)] + "." + str2[len(str3):]

      # le string final pour l'affichage = str1 + saut de ligne + str2
      strx = str1 + "\n" + str2

      retForecast += [strx]
      iDay += 1

   return retForecast

# fin des la définition des fonctions
#------------------------------------


#--------------------
# PROGRAMME PRINCIPAL


lForecast = get_forecast(iLieuChoisi)
lcd.message(lForecast[iJourChoisi])

# Make list of button value, text, and backlight color.
buttons = (LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN,  LCD.RIGHT)

while True:
    # Loop through each button and check if it is pressed.
    for button in buttons:
       
       if lcd.is_pressed(button): 

          if button == 0 : # SELECT
             iJourChoisi=1 # 10 = aujourd'hui, 1 = demain , ...
          
          elif button == 1: # RIGHT
             iLieuChoisi += 1
             if iLieuChoisi >= iNombreLieux :
                iLieuChoisi = 0
             
          elif button == 2: # DOWN
             iJourChoisi -= 1
             if iJourChoisi < 0 :
                iJourChoisi = len(lForecast) - 1
             
          elif button == 3: # UP
             iJourChoisi += 1
             if iJourChoisi >= len(lForecast) :
                iJourChoisi = 0
             
          elif button == 4: # LEFT
             iLieuChoisi -= 1
             if iLieuChoisi < 0 :
                iLieuChoisi = iNombreLieux - 1
                
          lcd.clear()
          lcd.message(lVille[iLieuChoisi])
          time.sleep(1)
          lcd.clear()
          lForecast = get_forecast(iLieuChoisi)
          lcd.message(lForecast[iJourChoisi])

# Fin du programme principal
#---------------------------

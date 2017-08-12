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

# assignation du display à la variable lcd et effacement du display
lcd = LCD.Adafruit_CharLCDPlate()

# création des listes pour les différents lieux pour lesquel on veut pouvoir afficher les prévisions météo
lLieux = [
   ["CH", "Sion", "FR"],
   ["IT", "Todi", "IT"],
   ["ES", "la Garriga", "SP"],
   ["GB", "London", "EN"],
   ["CH", "Bramois", "FR"],
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

iLieuChoisi = 0 # 0 = Sion, 1=  Todi, ...
iJourChoisi = 1 # 0 = auhourd'hui, 1 = demain , ...
iCouleurChoisie = 6 #  = reed , ... 6 = white

# info site wunderground
sKey = "d49b0a2fb656398f" # # clé fournie par le site internet de prévision météo https://www.wunderground.com/
sDemand = "forecast10day" # la demande pourrait aussi être "forecast10day" pour afficher la prévision sur 10 jours
sUrl = "http://api.wunderground.com/api" # url pour la demande

#---------------------------------------------------------------------------------------------------------------------------------
# fonctions utiles au programme

# fonction qui permet de supprimer les lettres accentuées dans un string
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
# fonction qui retourne les valeur du lieu choisi
def select_place(iPlace):
   return lLieux[iPlace][iLieuxPays], lLieux[iPlace][iLieuxVille], 'lang:' + lLieux[iPlace][iLieuxLangue]

# fonction qui retoune la prévision
def get_forecast (iPlace):

   sCountry, sCity, sLanguage = select_place(iPlace)
   r = requests.get(sUrl + "/" + sKey + "/" + sDemand + "/" + sLanguage + "/q/" + sCountry + "/" + sCity +".json")
   sForecast = r.json()


   # boucle pour parcourir les prévisions une à une
   iDay = 0
   retForecast = []
   for day in sForecast['forecast']['simpleforecast']['forecastday']:

      # création du string date et températures
      str1 = strip_accents(day['date']['weekday'][0:2] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius'])

      # création du string de prévision
      str2 = strip_accents(day['conditions'])

      # si le string contient plus de 16 caractères alors on raccourcit le premier mot 
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

      retForecast += [strx]
      iDay += 1

   return retForecast

#---------------------------------------------------------------------------------------------------------------------------------
# PROGRAMME PRINCIPAL

lcd.clear()
lForecast = get_forecast(iLieuChoisi)
lcd.message(lForecast[iJourChoisi])


while True:
    # Loop through each button and check if it is pressed.
    for button in buttons:
       
       if lcd.is_pressed(button): 

          if button == 0 : # SELECT
             iJourChoisi=1 # 0 = aujourd'hui, 1 = demain , ...
             lForecast = get_forecast(iLieuChoisi)
          
          elif button == 1: # RIGHT
             iLieuChoisi += 1
             if iLieuChoisi >= len(lLieux) :
                iLieuChoisi = 0
             lForecast = get_forecast(iLieuChoisi)
             
          elif button == 2: # DOWN
             iJourChoisi -= 1
             if iJourChoisi < 0 :
                iJourChoisi = len(lForecast) - 1
             lForecast = get_forecast(iLieuChoisi)
             
          elif button == 3: # UP
             iJourChoisi += 1
             if iJourChoisi >= len(lForecast) :
                iJourChoisi = 0
             lForecast = get_forecast(iLieuChoisi)
             
          elif button == 4: # LEFT
             iCouleurChoisie += 1
             if iCouleurChoisie >= len(lCouleurs) :
                iCouleurChoisie = 0
                
          lcd.set_color(lCouleurs[iCouleurChoisie][0],lCouleurs[iCouleurChoisie][1],lCouleurs[iCouleurChoisie][2])
          lcd.clear()
          lcd.message(lLieux[iLieuChoisi][iLieuxVille] + " / " + lLieux[iLieuChoisi][iLieuxLangue])
          time.sleep(1)
          lcd.clear()
          lcd.message(lForecast[iJourChoisi])
    time.sleep(0.2)

# Fin du programme
#---------------------------------------------------------------------------------------------------------------------------------

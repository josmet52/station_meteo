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

# importation des librairies nécessaires
import urllib2
import json
import requests
import time
import Adafruit_CharLCD as LCD
import unicodedata

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
             print "SELECT"
             iJourChoisi=1 # 10 = aujourd'hui, 1 = demain , ...
          
          elif button == 1: # RIGHT
             print "RIGHT"
             iLieuChoisi += 1
             if iLieuChoisi >= iNombreLieux :
                iLieuChoisi = 0
             
          elif button == 2: # DOWN
             print "DOWN"
             iJourChoisi -= 1
             if iJourChoisi < 0 :
                iJourChoisi = len(lForecast) - 1
             
          elif button == 3: # UP
             print "UP"
             iJourChoisi += 1
             if iJourChoisi >= len(lForecast) :
                iJourChoisi = 0
             
          elif button == 4: # LEFT
             print "LEFT"
             iLieuChoisi -= 1
             if iLieuChoisi < 0 :
                iLieuChoisi = iNombreLieux - 1
                
          lcd.clear()
          lcd.message(lVille[iLieuChoisi])
          time.sleep(1)
          lcd.clear()
          lForecast = get_forecast(iLieuChoisi)
          lcd.message(lForecast[iJourChoisi])





































### création du string demande
##sRequest = sUrl + "/" + sKey + "/" + sDemand + "/" + sLang + "/q/" + sPays + "/" + sVille +".json" 
##
##j=0 # compteur du nombre de passes pour la phase de test
##
### boucle sans fin du programme
##while True:
##    # interroger le site de prévision météo
##    r = requests.get(sRequest)
##    data = r.json() # récuper les datas sous forme JavaScript Object Notation (JSON)
##    
##    i=0 # initialisation du compteur de jours
##    j += 1 # incrémentation du compteur de passes
##
##    # boucle pour parcourir les prévisions une à une
##    for day in data['forecast']['simpleforecast']['forecastday']:
##
##        # création du string date et températures
##        str1 = day['date']['weekday'][0:2] + " " + str(day['date']['day']) + " -> " + day['low']['celsius'] + "-" + day['high']['celsius']
##
##        # création du string de prévision
##        str2 = strip_accents(day['conditions'])
##
##        # si le string contient plus de 16 caractères alors on raccorci le premier mot 
##        if len(str2) > 16 :
##            str3 = str2.split()[0]
##            str2 = str3[0:15-len(str2)] + "." + str2[len(str3):]
##
##        # le string final pour l'affichage = str1 + saut de ligne + str2
##        strx = str1 + "\n" + str2
##        # on enleve encore tous les accents dans le string car l'affichage ne les supporte pas
##        strx = strip_accents(strx)
##
##        # on imprime le string à l'écran
##        print str1, " -> low = ", day['low']['celsius'], " / high = ", day['high']['celsius'], " -> ", str2
##
##        # on enregistre les températures min et max pour choisir la couleur de l'affichage
##        tempMin = int(day['low']['celsius'])
##        tempMax = int(day['high']['celsius'])
##
##        # si on est en train de traiter "demain" on garde en mémoire les min et max
##        if i == 1 :
##            stry = strx
##            tempMiny = tempMin
##            tempMaxy = tempMax
##
##        # on ajuste la couleur de l'affichage en fonction des temp min et max
##        if tempMin < 0 :
##            lcd.set_color(0,0,1) # temp min < 0 -> color = blue
##        elif tempMax > 30 :
##            lcd.set_color(1,0,0) # temp max > 30 -> color = red
##        else :
##            lcd.set_color(0,1,0) # else color -> color = green
##
##        # on affiche la prévision
##        lcd.message(strx)
##        time.sleep(3)
##        lcd.clear()
##        
##        i += 1
##
##    # Avant de se mettre en pause, on affiche la prévision de demain qui restaera affichée pendant la pause de 20 minutes 
##    if tempMiny < 0 :
##       lcd.set_color(0,0,1) # temp min < 0 -> color = blue
##    elif tempMaxy > 30 :
##       lcd.set_color(1,0,0) # temp max > 30 -> color = red
##    else :
##       lcd.set_color(0,1,0) # else color -> color = green
##         
##    lcd.message(stry)
##
##    # pour le debug en phase initiale
##    print 'passe : ' + str(j) + " -> " + time.strftime('%d.%m.%Y %H:%M',time.localtime())
##    print sPays + " -> " + sVille
##    print stry
##    print '----------------------------------'
##
##    # et on fait une pasuse de 20 minutes, le temps de prendre un café ;-)
##    time.sleep(1200)

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

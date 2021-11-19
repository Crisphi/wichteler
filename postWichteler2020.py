# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 12:04:11 2020

@author: CrisO
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:38:20 2020

@author: CrisO
"""
"""2020 Update: Jetzt mit Blacklists!"""
"""Programm zum Auslosen von Wichtelpartnern"""

import json
from random import randint
tL = [] #Liste Teilnehmer
partner = dict() #Dictionary in der Partner*innen gespeichert werden

#Erstellt die Matches, Gibt Boolean über den Erfolg des Matches zurück
def matchfinder(tL):
    global partner
    pL1 = tL.copy() #Liste-Partner 1 (Schenkender)
    pL2 = tL.copy() #Liste-Partner 2 (Beschenkter)

    for x in range(len (pL1)):
        p1 = pL1.pop(0) #Übergibt Name und entfernt ihn danach aus der Liste
        counter = 0 #Counter für das Matching mit Blacklists
        while True:
            ridx = randint(0,len(pL2)-1) #Random Index
            if p1 != pL2[ridx]: #Stellt sicher, dass man sich nicht selber ziehen kann
                whitelisted = True
                # überprüft die Konformität mit blacklists
                for y in range(len(p1["blacklist"])):
                    if pL2[ridx]["name"] == p1["blacklist"][y]:
                        whitelisted = False
                if whitelisted == True:
                    break
                else:
                    if counter < 5000:
                        counter = counter + 1
                    else:
                        return False
            elif len(pL2) == 1 and p1 == pL2[ridx]:
                return False
        p2 = pL2.pop(ridx) #Übergibt Name und entfernt ihn danach aus der Liste
        partner.update({p1["name"]:p2["name"]}) #speichert das gefundene Match in partner

    #Noch einmal überprüfen ob sich niemand selbst gezogen hat
    for (k,v) in partner.items():
        if k == v:
            return False
    return True

#Automatisches Auslosen der Partner*innen
def automatischPartner(tL):
    counter2 = 0 #Counter für die Versuche Matches zu finden
    print("Suche Matches unter Berücksichtigung der Blacklists\n...")
    while counter2 < 100:
        result = matchfinder(tL)
        if result == True:
            ergebnissespeichern()
            break
        else:
            print("...")
            counter2 = counter2+1
    if counter2 >= 100:
        print("Es wurde keine Lösung mit den aktuellen Blacklists gefunden!")
        print("Auslosung abgebrochen! Versuche es erneut oder verändere die Blacklists")

#Erstellt File matches.json mit den ausgelosten Partner*innen, die vom mailer.py genutzt wird um die Mails zu versenden
def ergebnissespeichern():
    global partner
    j = json.dumps(partner)
    f = open("matches.json", "w+")
    f.write(j)
    f.close()
    print("------------------------------------------")
    print("Alle Teilnehmer*innen haben jetzt eine*n Partner*in!\nDie Dateien sind Abgespeichert.\nViel Spaß beim Wichteln!")

#Automatisch Teilnehmer*innen hinzufügen
def automatischhinzufuegen():
    p = open("participants.json", "r")
    participants = json.load(p)
    p.close()

    for (k, v) in participants.items():
        entree = {"name": k, "blacklist": v["blacklist"]}
        tL.append(entree)


#-----------------------------------------------------------------------------------
automatischhinzufuegen()
print("Teilnehmer*innen: ")
for x in tL:
    print(x["name"])
print("------------------------------------------")
automatischPartner(tL)

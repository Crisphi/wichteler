# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:39:27 2019

@author: CrisO
"""

"""Programm zum Auslosen von Wichtelpartnern"""
import json
from random import randint
tL = [] #Liste Teilnehmer

def weitermachen(antwort, liste, b = False):
    "Testet, ob Teilnehmer*in weitermachen will"
    a = str(antwort)
    if a == "nein" or a == "Nein" or a == "n":
        if len(liste) < 2:
            if b == False:
                print("Du hast zu wenige Teilnehmer*innen!")
                return True
            else:
                return False
        else:
            return False
    elif a == "ja" or a == "Ja" or a == "j":
        return True
    else:
        a2 = input("Falsche Eingabe! Nur 'Ja' oder 'Nein'. Versuch es nochmal: ")
        while True:
             if a2 == "nein" or a2 == "Nein" or a2 == "n":
                 return False
             elif a2 == "ja" or a2 == "Ja" or a2 == "j":
                 return True

def automatischPartner(tL):
    "Alle Partner*innen automatisch aussuchen"
    pL1 = tL.copy() #Liste-Partner 1 (Schenkender)
    pL2 = tL.copy() #Liste-Partner 2 (Beschenkter)
    partner = dict() #Dictionary in der Partner*innen gespeichert werden

    """Partner*innen suchen"""
    for x in range(len (pL1)):
        p1 = pL1.pop(0) #Übergibt Name und entfernt ihn danach aus der Liste
        while True:
            ridx = randint(0,len(pL2)-1) #Random Index
            if p1 != pL2[ridx]: #Stellt sicher, dass man sich nicht selber ziehen kann
                break
            elif len(pL2) == 1 and p1 == pL2[ridx]:
                automatischPartner(tL)
                break
        p2 = pL2.pop(ridx) #Übergibt Name und entfernt ihn danach aus der Liste
        partner.update({p1:p2})

    """Noch einmal überprüfen"""
    for (k,v) in partner.items():
        if k == v:
            automatischPartner(tL)

    """Dokumenterstellung"""
    #for x in partner:
     #   f = open(str(x)+".txt", "w+")
      #  f.write("Dein*e Partner*in ist... \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + str(partner[x]))
       # f.close()
   
    j = json.dumps(partner)
    f = open("matches.json", "w+")
    f.write(j)
    f.close()
        
    print("Alle Teilnehmer*innen haben jetzt eine*n Partner*in!\nDie Dateien sind Abgespeichert.\nViel Spaß beim Wichteln!")

""" Manuell Teilnehmer*innen hinzufügen"""
def manuellhinzufuegen():
    while True:
        teilnehmer = str(input("Teilnehmer*in eingeben: "))
        print("Eingabe: " + teilnehmer)
        answer = input("Teilnehmer*in so hinzufügen?")
        if weitermachen(answer,tL, True) == False:
            answer2 = input("Noch jemanden hinzufügen?")
            if weitermachen(answer2, tL) == False:
                break
            else:
                continue
        if teilnehmer in tL:
            print("Person ist schon Teilnehmer*in!")
            answer = input("Noch ein*e Teilnehmer*in? ")
            if weitermachen(answer, tL) == False:
                break
            else:
                continue
        else:
            tL.append(teilnehmer)
    
        answer = input("Noch ein*e Teilnehmer*in?")
        if weitermachen(answer,tL) == False:
            break
""" Automatisch Teilnehmer*innen hinzufügen"""
def automatischhinzufuegen():
    p = open("participants.json", "r")
    participants = json.load(p)
    p.close()
    
    for (k, v) in participants.items():
        tL.append(k)



"""Fragt ab, ob manuell oder automatisch hinzugefügt werdden soll"""
def autovsmanu():
    answer = input("Soll manuell oder automatisch hinzugefuegt werden?")
    if answer == "manuell" or answer == "manu" or answer == "m":
        manuellhinzufuegen()
    elif answer == "automatisch" or answer == "auto" or answer == "a":
        beshure()
    else:
        print("Falsche Eingabe! Nur 'automatisch' oder 'manuell'. Versuch es nochmal:")
        autovsmanu()
        
        
def beshure():
    shure = input("Sicher, dass automatisch hinzugefuegt werden soll? Eine Datei 'participants.json' muss bereitgestellt werden:")
    if shure == "ja" or shure == "j" or shure == "Ja":
        automatischhinzufuegen()
    elif shure == "nein" or shure == "n" or shure == "Nein":
        autovsmanu()
    else:
        print("Falsche Eingabe! Nur 'Ja' oder 'Nein'. Versuch es nochmal:")
        beshure()


autovsmanu()

print("Teilnehmer*innen: ")
for x in tL:
    print(x)

automatischPartner(tL)









"""Partner*innen suchen"""

"""pL1 = tL.copy() #Liste-Partner 1 (Schenkender)
pL2 =tL.copy() #Liste-Partner 2 (Beschenkter)
partner = set() #Liste- Kombi

while len(pL1) >= 1:
    pTemp = str(input("Für wen soll ein*e Wichtelpartner*in gesucht werden?"))
    try:
        pL1.index(pTemp)
    except ValueError:
        print("Name nicht enthalten oder hat schon Wichtelpartner*in!")
        continue
    else:
        idx1 = pL1.index(pTemp)
        p1 = pL1.pop(idx1) #Übergibt Name und entfernt ihn danach aus der Liste
    while True:
        ridx = randint(0,len(pL2)-1) #Random Index
        if p1 != pL2[ridx]: #Stellt sicher, dass man sich nicht selber ziehen kann
            break

    p2 = pL2.pop(ridx) #Übergibt Name und entfernt ihn danach aus der Liste
    partner.add((p1,p2))

    Dokumenterstellung
    f = open(str(p1)+".txt", "w+")
    f.write("Dein*e Partner*in steht weiter unten\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + str(p2))
    f.close()

    print("Noch Partner*innenlose Teilnehmer*innen: ")
    for x in pL1:
        print(x)


print("Alle Teilnehmer*innen haben jetzt eine*n Partner*in!\nDie Dateien sind Abgespeichert.\nViel Spaß beim Wichteln!")"""

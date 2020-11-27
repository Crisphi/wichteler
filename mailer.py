# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 18:01:57 2019

@author: CrisO
"""
#import all necessary libraries
import json
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#your email account details
ad = "example@mail.de"
pw = "password"

#load template for email
f = open("template.txt", "r")
template = Template(f.read())
f.close()

#load wichtel data
w = open("matches.json", "r")
matches = json.load(w)
w.close()

#load email data
e = open("participants.json", "r")
data = json.load(e)
e.close()

#start smtp server
s = smtplib.SMTP(host="smtp-mail.outlook.com", port=587) #replace with your mailing host
s.starttls()
s.login(ad, pw)

for (k, v) in matches.items():
    #create message
    msg = MIMEMultipart()
    message = template.substitute(NAME = k, PARTNER = v, ADRESSE = data[v]["adress"])

    #parameters of message
    msg["From"] = ad
    msg["To"] = data[k]["mail"]
    msg["Subject"] = "Postwichteln 2020"

    #add message body
    msg.attach(MIMEText(message.encode("utf-8"), "plain", _charset="utf-8"))

    #send message and delete it afterwards
    s.send_message(msg)
    print("Gesendet:")
    print(k)
    del msg

#close smtp server
s.quit()

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
pw = "passwort"

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
emails = json.load(e)
e.close()

#start smtp server
s = smtplib.SMTP(host="smtp-mail.outlook.com", port=587)
s.starttls()
s.login(ad, pw)

for (k, v) in matches.items():
    #create message
    msg = MIMEMultipart()
    message = template.substitute(NAME = k, PARTNER = v)
    print(message)
    
    #parameters of message
    msg["From"] = ad
    msg["To"] = emails[k]
    msg["Subject"] = "Dein*e Wichtelpartner*in"
    
    #add message body
    msg.attach(MIMEText(message, "plain"))
    
    #send message and delete it afterwards
    s.send_message(msg)
    del msg

#close smtp server
s.quit()

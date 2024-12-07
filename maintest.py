# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 19:57:11 2021

@author: CrisO
"""

from flask import Flask, render_template, request, url_for, flash, redirect, session
import mysql.connector
from werkzeug.exceptions import abort
from passlib.hash import sha256_crypt
import os
import operator

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
    global text
    counter2 = 0 #Counter für die Versuche Matches zu finden
    #print("Suche Matches unter Berücksichtigung der Blacklists\n...")
    text = text + "Suche Matches unter Berücksichtigung der Blacklists\n...\n"
    while counter2 < 100:
        result = matchfinder(tL)
        if result == True:
            ergebnissespeichern()
            break
        else:
            #print("...")
            text = text + "...\n"
            counter2 = counter2+1
    if counter2 >= 100:
        #print("Es wurde keine Lösung mit den aktuellen Blacklists gefunden!")
        text = text + "Es wurde keine Lösung mit den aktuellen Blacklists gefunden!\n"
        #print("Auslosung abgebrochen! Versuche es erneut oder verändere die Blacklists")
        text = text + "Auslosung abgebrochen! Versuche es erneut oder verändere die Blacklists\n"

#Erstellt File matches.json mit den ausgelosten Partner*innen, die vom mailer.py genutzt wird um die Mails zu versenden
def ergebnissespeichern():
    global partner
    global text
    j = json.dumps(partner)
    f = open("matches.json", "w+")
    f.write(j)
    f.close()
    #print("------------------------------------------")
    text = text + "------------------------------------------\n"
    #print("Alle Teilnehmer*innen haben jetzt eine*n Partner*in!\nDie Dateien sind Abgespeichert.\nViel Spaß beim Wichteln!")
    text = text + "Alle Teilnehmer*innen haben jetzt eine*n Partner*in!\nDie Dateien sind Abgespeichert.\nViel Spaß beim Wichteln!\n"

#Automatisch Teilnehmer*innen hinzufügen
def automatischhinzufuegen():
    p = open("participants.json", "r")
    participants = json.load(p)
    p.close()

    for (k, v) in participants.items():
        entree = {"name": k, "blacklist": v["blacklist"]}
        tL.append(entree)

#____________________________________________________________________________________________________
def getDBconnection():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
      database="wichtelerdb"
    )
    print(mydb)
    return mydb

def getParticipant(id):
    mydb = getDBconnection()
    mycursor = mydb.cursor(dictionary = True)
    sqlget = "SELECT * FROM Participants WHERE id = %s"
    idval = (id,)
    mycursor.execute(sqlget, idval)
    pa = mycursor.fetchone()
    mydb.close()
    if pa is None:
        abort(404)
    return pa
#____________________________________________________________________________________________________
app = Flask(__name__)
#____________________________________________________________________________________________________
"""from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)
class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        #True, as all users are active.
        return True

    def get_id(self):
        #Return the email address to satisfy Flask-Login's requirements.
        return self.email

    def is_authenticated(self):
        #Return True if the user is authenticated.
        return self.authenticated

    def is_anonymous(self):
        #False, as anonymous users aren't supported.
        return False

@login_manager.user_loader
def user_loader(user_id):
    #Given *user_id*, return the associated User object.

    #:param unicode user_id: user_id (email) user to retrieve

    return User.get(user_id)

#____________________________________________________________________________________________________
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#____________________________________________________________________________________________________


@app.route("/test")
#@login_required
def test():
    return render_template("base.html")

@app.route("/testlogin", methods=["GET", "POST"])
def testlogin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('testlogin'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('logintest.html', title='Sign In', form=form)

@app.route("/testlogout", methods=["GET"])
#@login_required
def testlogout():
    #Logout the current user.
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("index.html")"""


@app.route("/")
def index():
    if not session.get("logged_in"):
        return render_template("login.html")
    else:
        mydb = getDBconnection()

        mycursor = mydb.cursor(dictionary = True)
        #mycursor.execute("SHOW TABLES")

        #for x in mycursor:
          #print(x)
        print("Fetching DB Data")
        mycursor.execute("SELECT * FROM Participants WHERE email='" + session["user_id"] +"'")
        print("Executed SQL Command")

        dbparticipants = mycursor.fetchall()

        mydb.close()
        print("Feched Results")
        for x in dbparticipants:
          print(x)
        print("Rendering Template")
        return render_template('index.html', participants = dbparticipants)

@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if not session.get("logged_in"):
        if request.method == "POST":
            login = request.form
            print(login)
            email = login["email"]
            password = login["password"]
            account = False

            mydb = getDBconnection()
            mycursor = mydb.cursor()

            mycursor.execute("SELECT password FROM Participants WHERE email = %s", (email,))
            pwData = mycursor.fetchone()
            print(pwData)
            mydb.close()

            if pwData and sha256_crypt.verify(password, pwData[0]):
                account = True

            if account:
                session["logged_in"] = True
                session["user_id"] = email
                flash("Du hast dich erfolgreich eingeloggt!" , "info")
                return redirect(url_for("index"))
            else:
                error ="Falsches Passwort oder E-Mail Adresse!"
                #flash("Falsches Passwort oder E-Mail Adresse!")
                return render_template("login.html", error = error)
        else:
            flash("Du bist bereits angemeldet!", "error")
            return redirect(url_for("index"))
    return render_template("login.html", error = error)

@app.route("/registration", methods=["GET","POST"])
def registration():
    if not session.get("logged_in"):
        if request.method == "POST":
            registration = request.form
            password = registration["password"]
            password2 = registration["password2"]
            if password != password2:
                flash("Paswörter stimmen nicht überein!", "error")
                return (redirect(url_for("registration")))
            pwhash = sha256_crypt.hash(password)
            email = registration["email"]
            if registration["name"] != "":
                name = registration["name"]
            else:
                name = None
            if registration["pronouns"] != "":
                pronouns = registration["pronouns"]
            else:
                pronouns= None
            if registration["shippingname"] != "":
                shippingname = registration["shippingname"]
            else:
                shippingname = None
            if registration["streetandnr"] != "":
                streetandnr = registration["streetandnr"]
            else:
                streetandnr = None
            if registration["city"] != "":
                city = registration["city"]
            else:
                city = None
            if registration["plz"] != "":
                plz = registration["plz"]
            else:
                plz = None
            if registration["shippingnotes"] != "":
                shippingnotes = registration["shippingnotes"]
            else:
                shippingnotes = None

            mydb = getDBconnection()
            mycursor = mydb.cursor()

            mycursor.execute("SELECT email FROM Participants")
            emails = mycursor.fetchall()
            for x in emails:
                if email == x[0]:
                    flash("Die angegebene E-Mail Adresse wird bereits genutzt!", "error")
                    print("error")
                    return(redirect(url_for("registration")))

            sqlinsert = "INSERT INTO Participants (name, pronouns, email, password, shippingname, streetandnr, plz, city, shippingnotes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valinsert = (name, pronouns, email, pwhash, shippingname, streetandnr, plz, city, shippingnotes)
            print(valinsert)
            mycursor.execute(sqlinsert, valinsert)

            mycursor.execute("SELECT * FROM Participants")
            myresult = mycursor.fetchall()
            for x in myresult:
              print(x)
            mydb.commit()
            mydb.close()

            flash("Du hast dich erfolgreich registriert!", "info")
            session["logged_in"] = True
            session["user_id"] = email
            return redirect(url_for("index"))
    else:
        flash("Logge dich aus, um einen neuen Account zu erstellen!", "error")
        return redirect(url_for("index"))
    return render_template("registration.html")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    session["user_id"] = None
    flash("Du bist jetzt ausgeloggt!", "info")
    return redirect(url_for("index"))

@app.route("/wichteler")
def start():
    global text
    text = "" #Ausgabetext
    automatischhinzufuegen()
    #print("Teilnehmer*innen: ")
    text = text + "Teilnehmer*innen: \n"
    for x in tL:
        #print(x["name"])
        text = text + x["name"] + "\n"
    #print("------------------------------------------")
    text = text + "------------------------------------------\n"
    automatischPartner(tL)
    print(text)
    return render_template('index.html')

@app.route("/<int:id>")
def participant(id):
    participant = getParticipant(id)
    return render_template('participant.html', participant = participant)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host="127.0.0.1", port=8080, debug=True)

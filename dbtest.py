import mysql.connector
from passlib.hash import sha256_crypt

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="wichtelerdb"
)

print(mydb)

mycursor = mydb.cursor()

###mycursor.execute("CREATE DATABASE wichtelerdb")###

#mycursor.execute("SHOW DATABASES")

#for x in mycursor:
  #print(x)

#mycursor.execute("CREATE TABLE Participants (id INTEGER PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, pronouns VARCHAR(255), email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, shippingname VARCHAR(255), streetandnr VARCHAR(255), plz INTEGER, city VARCHAR(255), shippingnotes VARCHAR(255), shippingsent BOOLEAN)")

#mycursor.execute("CREATE TABLE Matches (id INTEGER PRIMARY KEY AUTO_INCREMENT, giver INTEGER, reciever INTEGER, FOREIGN KEY (giver) REFERENCES Participants(id), FOREIGN KEY (reciever) REFERENCES Participants(id))")

#mycursor.execute("CREATE TABLE Blacklists (id INTEGER PRIMARY KEY AUTO_INCREMENT, participant INTEGER, blacklisted INTEGER, FOREIGN KEY (participant) REFERENCES Participants(id), FOREIGN KEY (blacklisted) REFERENCES Participants(id))")

#mycursor.execute("SHOW TABLES")

#for x in mycursor:
  #print(x)

mycursor.execute("DELETE FROM Participants")

password = sha256_crypt.hash("password")
password2 = sha256_crypt.hash("password2")
print(password)

sqlinsert = "INSERT INTO Participants (name, pronouns, email, password, shippingname, streetandnr, plz, city, shippingnotes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
valinsert = [("Cris", "er/ihm", "cris.ortega@outlook.de", password, "Cristian Ortega Singer", "Drausnickstr. 6", "91052", "Erlangen", "2. Stock links"),("Washi", "fancyness", "stripezz1@freeroll.de", password2, "Washi Tape", "Gesines Schreibtisch 1b", "91245", "Simmelsdorf", ":3"), ("Waschbär", "xier/xim", "uwubaer42@hotfur.com", password, "Waschbär Kernseife", "An der Mülltonne 3", "91052", "Erlangen", "Hinter der Banane")]

for x in valinsert:
    mycursor.execute(sqlinsert, x)

mycursor.execute("SELECT * FROM Participants")

myresult = mycursor.fetchall()
for x in myresult:
  print(x)

mydb.commit()
mydb.close()

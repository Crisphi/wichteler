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

#mycursor.execute("CREATE TABLE Games (id INTEGER PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, participant INTEGER, FOREIGN KEY (participant) REFERENCES Participants(id))")


mycursor.execute( "INSERT INTO Games (name) VALUES ('Crisises Weihnachtswichteln 2021-22')")

mycursor.execute("SELECT * FROM Games")

myresult = mycursor.fetchall()
for x in myresult:
  print(x)


"""mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)"""

mydb.commit()
mydb.close()

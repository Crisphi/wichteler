import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="wichtelerdb"
)

print(mydb)

mycursor = mydb.cursor(dictionary = True)


#mycursor.execute("SHOW TABLES")
#for x in mycursor:
  #print(x)




#mycursor.execute("SELECT * FROM Participants")

#myresult = mycursor.fetchall()
#for x in myresult:
  #print(x)
id = 1
sql = "SELECT * FROM Participants WHERE id = %s"
mycursor.execute(sql,id) #, (id,)).fetchone()
pa = mycursor.fetchone()
print(pa)

mydb.close()
#print(myresult)

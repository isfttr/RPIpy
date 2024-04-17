import mysql.connector

# Establish a connection to the database
db = mysql.connector.connect(
  host="localhost",
  user="admin",
  passwd="14ks06rfg",
  database="protecoes"
)

# Create a cursor object
mycursor = db.cursor()
print(db)

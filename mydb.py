# import pymongo
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# database = client["PayrollDatabase"]
# print("Connected to MongoDB!")
# employees_collection = database["PayrollCollection"]
# print("Document inserted successfully!")
# client.close()
import mysql.connector

dataBase = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'password'

	)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE AttPay")

print("All Done!")

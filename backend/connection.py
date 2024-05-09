from pymongo import MongoClient

# Specify the ClusterIP service name
db_service_name = "localhost"

# Specify the port defined in your service
db_port = 27017

# Connect to the MongoDB service
client = MongoClient(db_service_name, db_port)

# Access the databases and collections
db1 = client.users
db2 = client.items

userdb = db1.myusers
itemdb = db2.credentials
from pymongo import MongoClient

# Specify the ClusterIP service name
db_service_name = "mdb-service"

# Specify the port defined in your service
db_port = 27017

# Construct the connection string using the service name and port
db_uri = f"mongodb://{db_service_name}:{db_port}"

# Connect to the MongoDB service
client = MongoClient(db_uri)

# Access the databases and collections
db1 = client.users
db2 = client.items

userdb = db1.myusers
itemdb = db2.credentials
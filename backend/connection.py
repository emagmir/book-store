from pymongo import MongoClient
import os
import json


secret_file_path = "/mnt/secrets-store/mongo_string"

def get_secret():
    with open(secret_file_path, 'r') as secret_file:
        data = secret_file.read()
        secret_data = json.loads(data)
        secret_string = secret_data['MONGO_CONNECTION_STRING']
        return secret_string

# Read the secret
mongo_connection_string = get_secret()

# Connect to the MongoDB service
client = MongoClient(mongo_connection_string)

# Access the databases and collections
db1 = client.users
db2 = client.items

userdb = db1.myusers
itemdb = db2.credentials
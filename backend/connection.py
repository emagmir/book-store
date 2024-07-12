from pymongo import MongoClient
import os


secret_file_path = "/mnt/secrets-store/mongo_string"

def get_secret():
    with open(secret_file_path, 'r') as secret_file:
        for line in secret_file:
            key, value = line.strip().split('=', 1)
            if key == 'MONGO_CONNECTION_STRING':
                return value

# Read the secret
mongo_connection_string = get_secret()

# Connect to the MongoDB service
client = MongoClient(mongo_connection_string)

# Access the databases and collections
db1 = client.users
db2 = client.items

userdb = db1.myusers
itemdb = db2.credentials
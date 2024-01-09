# db_config.py
import pymongo

host = "mongodb"
port = 27017
database_name = "default"
collection_name = "realEstate"

try:
    client = pymongo.MongoClient(host, port)
    print("Connection to MongoDB successful")
except pymongo.errors.ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit()

db = client[database_name]

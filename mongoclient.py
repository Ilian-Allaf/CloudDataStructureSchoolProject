import pymongo

host = "localhost"
port = 27017
database_name = "default"
collection_name = "realEstate"

try:
    client = pymongo.MongoClient(host, port)
    print("Connexion réussie à MongoDB")
except pymongo.errors.ConnectionFailure as e:
    print(f"Échec de la connexion à MongoDB: {e}")
    exit()

import pandas as pd
from utils import cleanData
from mongoclient import client, collection_name, database_name

# # Sélectionner la base de données
db = client[database_name]

# Vérifier si la collection existe, sinon la créer
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)
    print(f"Collection '{collection_name}' créée avec succès.")

# Inserer les données dans la collection
data_path = './valeursfoncieres-2023.txt'
data = pd.read_csv(data_path, sep="|", dtype=str)
data = cleanData(data)
data_dict_list = data.to_dict(orient='records')
db[collection_name].insert_many(data_dict_list)

# Fermer la connexion à MongoDB
client.close()

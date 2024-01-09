from mongoclient import client, collection_name, database_name

db = client[database_name]
result = db[collection_name].find_one({"Commune": "ST-GENIS-POUILLY"})
print(result)
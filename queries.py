from mongoclient import client, collection_name, database_name
import matplotlib.pyplot as plt
import base64
from io import BytesIO


db = client[database_name]
collection = db[collection_name]

def plot_transaction_distribution():
    

     # Effectuer une agrégation pour compter le nombre de transactions par type
    pipeline = [
        {"$group": {"_id": "$Nature mutation", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "Type de transaction": "$_id", "Nombre de transactions": "$count"}}
    ]

    result = list(collection.aggregate(pipeline))

    # Créer un graphique à barres
    types_transaction = [entry["Type de transaction"] for entry in result]
    nombre_transactions = [entry["Nombre de transactions"] for entry in result]

    plt.figure(figsize=(10, 6))
    plt.bar(types_transaction, nombre_transactions, color='skyblue')
    plt.title('Répartition des types de transactions')
    plt.xlabel('Type de transaction')
    plt.ylabel('Nombre de transactions')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Convertir le graphique en base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Convertir l'objet BytesIO en une chaîne base64 pour l'inclure dans l'HTML
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Fermer la connexion à MongoDB
    client.close()

    return image_base64

def get_transactions_by_commune(commune_name):

    collection = db[collection_name]

    # Effectuer une agrégation pour compter le nombre de transactions par commune
    pipeline = [
        {"$match": {"Commune": commune_name}},
        {"$group": {"_id": "$Nature mutation", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "Type de transaction": "$_id", "Nombre de transactions": "$count"}}
    ]

    result = list(collection.aggregate(pipeline))

    # Create a bar plot of the transaction counts
    transaction_types = [doc['Type de transaction'] for doc in result]
    transaction_counts = [doc['Nombre de transactions'] for doc in result]
    plt.bar(transaction_types, transaction_counts)

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the BytesIO object to a base64-encoded string
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Fermer la connexion à MongoDB
    client.close()

    return graphic

def plot_geographical_distribution():

    # Perform an aggregation to count the number of transactions per commune
    pipeline = [
        {"$group": {"_id": "$Commune", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "Commune": "$_id", "Nombre de transactions": "$count"}}
    ]

    result = list(collection.aggregate(pipeline))

    # Create a bar plot of the transaction counts
    communes = [doc['Commune'] for doc in result]
    transaction_counts = [doc['Nombre de transactions'] for doc in result]
    plt.bar(communes, transaction_counts)

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the BytesIO object to a base64-encoded string
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def plot_temporal_evolution():
    pipeline = [
        {"$group": {"_id": "$Date mutation", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    result = list(collection.aggregate(pipeline))

    # Créer un graphique à barres pour l'évolution temporelle
    dates = [entry["_id"] for entry in result]
    transaction_counts = [entry["count"] for entry in result]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, transaction_counts, marker='o', linestyle='-')
    plt.title('Évolution temporelle des transactions')
    plt.xlabel('Date de mutation')
    plt.ylabel('Nombre de transactions')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Convertir le graphique en base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plt.close()

    # Convertir l'objet BytesIO en une chaîne base64 pour l'inclure dans l'HTML
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Fermer la connexion à MongoDB
    client.close()

    return image_base64
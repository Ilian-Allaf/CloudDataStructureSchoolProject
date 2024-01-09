from mongoclient import client, collection_name, database_name
import matplotlib
import matplotlib.pyplot as plt
import base64
import pandas as pd
from io import BytesIO
import seaborn as sns
matplotlib.use('Agg')

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
    plt.xlabel('Type de transaction')
    plt.ylabel('Nombre de transactions')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    
    # Convertir le graphique en base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    

    # Convertir l'objet BytesIO en une chaîne base64 pour l'inclure dans l'HTML
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Fermer la connexion à MongoDB
    # client.close()

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
    # client.close()

    return graphic

def plot_geographical_distribution():
    plt.clf()
    # Perform an aggregation to count the number of transactions per commune
    pipeline = [
        {"$group": {"_id": "$Commune", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "Commune": "$_id", "Nombre de transactions": "$count"}}
    ]

    result = list(collection.aggregate(pipeline))

    # Create a bar plot of the transaction counts
    communes = [doc['Commune'] for doc in result]
    transaction_counts = [doc['Nombre de transactions'] for doc in result]

    plt.bar(range(len(communes)), transaction_counts)
    plt.xticks(range(len(communes)), communes, rotation='vertical')
    
    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the Matplotlib figure and close it
    plt.clf()
    plt.close()

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
    plt.xlabel('Date de mutation')
    plt.ylabel('Nombre de transactions')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    
    # Convertir le graphique en base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Convertir l'objet BytesIO en une chaîne base64 pour l'inclure dans l'HTML
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Fermer la connexion à MongoDB
    # client.close()

    return image_base64

def plot_mean_squared_meter():
    '''data = collection.find({
    'Type local': {'$in': ['Maison', 'Appartement']},
    'Surface reelle bati': {'$type': 1},  # Check if 'Surface reelle bati' is numeric
    'Valeur fonciere': {'$type': 1},  # Check if 'Valeur fonciere' is numeric
    })'''
    data = collection.find({}, {
    'Type local': 1,
    'Surface reelle bati': 1,
    'Valeur fonciere': 1
})

    df = pd.DataFrame(data)

    df['Surface reelle bati'] = pd.to_numeric(df['Surface reelle bati'], errors='coerce')
    df['Valeur fonciere'] = pd.to_numeric(df['Valeur fonciere'], errors='coerce')

    # Drop rows with missing values
    df = df.dropna(subset=['Surface reelle bati', 'Valeur fonciere'])

    # Filter data for 'Maison' and 'Appartement'
    df = df[df['Type local'].isin(['Maison', 'Appartement'])]

    # Calculate price per square meter
    df['Price per m2'] = df['Valeur fonciere'] / df['Surface reelle bati']

    # Set seaborn style
    sns.set(style="whitegrid")

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Type local', y='Price per m2', data=df, estimator='mean', errorbar=None)
    plt.title('Prix moyen au m² entre un appartement et une maison')
    plt.xlabel('Type de transaction')
    plt.ylabel('Average Price per Square Meter')
    plt.tight_layout()

    # Convertir le graphique en base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Convertir l'objet BytesIO en une chaîne base64 pour l'inclure dans l'HTML
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    return image_base64
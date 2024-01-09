from flask import Flask, render_template, redirect, url_for
from plots import (
    plot_transaction_distribution,
    plot_temporal_evolution,
    plot_geographical_distribution,
    plot_mean_squared_meter
)
from db_config import client, database_name, collection_name
import pandas as pd
app = Flask(__name__)

def cleanData(data):
    filter_colums = ['Date mutation', 'Valeur fonciere', 'Commune', 'Code departement', 'Type local', 'Type de voie', 'Surface reelle bati', 'Surface terrain', 'Nature mutation']
    data = data[filter_colums]
    data.loc[:, 'Valeur fonciere'] = data['Valeur fonciere'].str.replace(',', '.').astype(float)
    data.loc[:, 'Date mutation'] = pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')
    return data

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


# Flask routes
@app.route("/")
def hello_world():
    return redirect(url_for('func_geographical_distribution'))

@app.route("/geographical_distribution")
def func_geographical_distribution():
    input_image = plot_geographical_distribution()
    title = "Distribution géographique des ventes"
    return render_template('home.html', title=title, image=input_image)

@app.route("/transaction_distribution")
def func_transaction_distribution():
    input_image = plot_transaction_distribution()
    title = "Répartition des types de transactions"
    return render_template('home.html', title=title, image=input_image)

@app.route("/temporal_evolution")
def func_temporal_evolution():
    input_image = plot_temporal_evolution()
    title = "Évolution temporelle des transactions"
    return render_template('home.html', title=title, image=input_image)

@app.route("/mean_squared_meter")
def func_mean_squared_meter():
    input_image = plot_mean_squared_meter()
    title = "Prix moyen du m2 par type de transaction"
    return render_template('home.html', title=title, image=input_image)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

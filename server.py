from flask import Flask, render_template
from plots import plot_transaction_distribution, plot_temporal_evolution, plot_geographical_distribution, get_transactions_by_commune

app = Flask(__name__)

@app.route("/")
def hello_world(name=None):
    return render_template('test.html')

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

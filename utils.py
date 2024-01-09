import pandas as pd

# Clean data before inserting into MongoDB
def cleanData(data):
    filter_colums = ['Date mutation', 'Valeur fonciere', 'Commune', 'Code departement', 'Type local', 'Type de voie', 'Surface reelle bati', 'Surface terrain', 'Nature mutation']
    data = data[filter_colums]
    data.loc[:, 'Valeur fonciere'] = data['Valeur fonciere'].str.replace(',', '.').astype(float)
    data.loc[:, 'Date mutation'] = pd.to_datetime(data['Date mutation'], format='%d/%m/%Y')
    return data


# Importa le librerie necessarie
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import os

# Carica il dataset completo
dataset = pd.read_csv('./merged_dataset_races.csv')

# Creazione del vettore da 1 a 20
drivers = [1, 855, 20, 839, 807, 830, 832, 840, 847, 848, 849, 13, 4]
myMap = {}

for pilota in drivers:
    myMap[pilota] = 0

print(myMap)

counter = 0

for counter in range (0, 14):
    # Applica i filtri desiderati, ad esempio, consideriamo solo i record con driverId=1 e circuitId=1
    print("Iterazione" + str(counter) + "-" + str(drivers[counter]))
    filtered_data = dataset[(dataset['driverId'] == drivers[counter]) & (dataset['circuitId'] == 3)]
    print("Iterazione" + str(counter))

    # Seleziona solo le colonne desiderate
    selected_columns = ['driverId', 'circuitId', 'time_lap']
    df = filtered_data[selected_columns]

    df.to_csv('aaaaa.csv', index=False)

    # Seleziona le colonne necessarie
    features = ['driverId', 'circuitId', 'time_lap']
    target = 'time_lap'  # ora prevediamo direttamente i tempi dei giri

    # Crea il set di addestramento e di test
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

    # Definisci la trasformazione delle colonne
    preprocessor = StandardScaler()

    # Crea il modello di regressione
    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('regressor', LinearRegression())])

    # Addestra il modello
    model.fit(X_train, y_train)

    # Fai le previsioni sui dati di test
    predictions = model.predict(X_test)

    # Ottieni solo la prima previsione (considerando solo un prossimo giro)
    next_lap_prediction = predictions[0]

    # Stampa la previsione per il prossimo giro
    print("Ecco il prossimo giro:", next_lap_prediction)


    # Converti millisecondi a secondi
    seconds, milliseconds = divmod(next_lap_prediction, 1000)

    # Converti secondi a minuti e ore
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # Formatta il risultato
    formatted_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    print("Tempo convertito:", formatted_time)

    myMap[counter] = milliseconds
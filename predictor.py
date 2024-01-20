# Import delle librerie
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Caricamento dei dati
# Assicurati che il tuo dataset sia in formato CSV o un altro formato supportato da pandas
data = pd.read_csv('./merged_dataset_races.csv')

data = data.replace('\\N', pd.NA)
data = data.apply(pd.to_numeric, errors='coerce')
data.fillna(data.median(), inplace=True)

# Preparazione dei dati
# Seleziona le colonne rilevanti per l'addestramento del modello
selected_columns = ['lap', 'position_lap', 'milliseconds_lap', 'grid', 'positionOrder', 'fastestLap', 'rank', 'fastestLapSpeed', 'statusId']

# Elimina le righe con valori mancanti, se presenti
data = data[selected_columns].dropna()

# Definizione delle variabili indipendenti (X) e dipendenti (y)
X = data.drop('positionOrder', axis=1)
y = data['positionOrder']

# Suddivisione del dataset in set di addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creazione del modello
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Addestramento del modello
model.fit(X_train, y_train)

# Valutazione del modello
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Visualizzazione del report di classificazione
classification_rep = classification_report(y_test, y_pred)
print('Classification Report:\n', classification_rep)

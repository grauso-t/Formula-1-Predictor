import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

# Carica i dati
data = pd.read_csv("merged_dataset_races.csv", low_memory=False)
data.replace("\\N", pd.NA, inplace=True)

# Prepara i dati
features = ['lap', 'position_lap', 'milliseconds_lap', 'number', 'grid', 'rank', 'fastestLap', 'fastestLapTime', 'fastestLapSpeed']
target = 'positionOrder'

X = data[features]
y = data[target]

# Sostituisci i valori mancanti con la media della colonna
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Suddividi i dati in set di addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crea il modello
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Addestra il modello
model.fit(X_train, y_train)

# Effettua predizioni sul set di test
predictions = model.predict(X_test)

# Valuta le prestazioni del modello
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

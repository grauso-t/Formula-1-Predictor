import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Caricamento dataset
oversampled = pd.read_csv("./balanced_dataset.csv")
not_oversampled = pd.read_csv("./merged_dataset_races.csv")

# Selezione features e la variabile target
X_oversampled = oversampled[['driverId', 'circuitId', 'lap', 'weather_code']]
y_oversampled = oversampled['time_lap']

X_not_oversampled = not_oversampled[['driverId', 'circuitId', 'lap', 'weather_code']]
y_not_oversampled = not_oversampled['time_lap']

# Suddivisione dati in set di addestramento e test
X_train = X_oversampled
y_train = y_oversampled

X_test = X_not_oversampled
y_test = y_not_oversampled

# Addestramento del modello RandomForestRegressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Valutazione del modello
rf_pred = rf_model.predict(X_test)
rf_rmse = mean_absolute_error(y_test, rf_pred)
rf_accuracy = r2_score(y_test, rf_pred)

print("Mean Absolute Error (RF):", rf_rmse / 10)
print("Accuracy (RF):", rf_accuracy)

# Salvataggio del modello
joblib.dump(rf_model, 'rf_model.pkl')

print("Modello addestrato e salvato con successo.")

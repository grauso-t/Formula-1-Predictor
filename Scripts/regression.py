import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import root_mean_squared_error
import joblib

# Carica il dataset
data = pd.read_csv("balanced_dataset.csv")

# Seleziona le colonne predittive (features) e la variabile target
X = data[['driverId', 'circuitId', 'lap', 'weather_code']]
y = data['time_lap']

# Suddividi i dati in set di addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crea e addestra lo scaler sui dati di addestramento
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Addestramento del modello RandomForestRegressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Addestramento del modello SVR
svr_model = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
svr_model.fit(X_train_scaled, y_train)

# Addestramento del modello MLPRegressor
mlp_model = make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42))
mlp_model.fit(X_train_scaled, y_train)

# Valutazione dei modelli
rf_pred = rf_model.predict(X_test)
svr_pred = svr_model.predict(X_test)
mlp_pred = mlp_model.predict(X_test)

rf_rmse = root_mean_squared_error(y_test, rf_pred)
svr_rmse = root_mean_squared_error(y_test, svr_pred)
mlp_rmse = root_mean_squared_error(y_test, mlp_pred)

# Salva i modelli e lo scaler
joblib.dump(rf_model, 'rf_model.pkl')
joblib.dump(svr_model, 'svr_model.pkl')
joblib.dump(mlp_model, 'mlp_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Modelli addestrati e salvati con successo.")

input_data = pd.DataFrame({'driverId': [844], 'circuitId': [3], 'lap': [3], 'weather_code': [0.0]})

# Applica lo scaler ai dati di input
input_data_scaled = scaler.transform(input_data)

# Effettua le previsioni utilizzando i modelli
rf_prediction = rf_model.predict(input_data_scaled)
svr_prediction = svr_model.predict(input_data_scaled)
mlp_prediction = mlp_model.predict(input_data_scaled)

print("Previsione con RandomForestRegressor:", rf_prediction)
print("Previsione con SVR:", svr_prediction)
print("Previsione con MLPRegressor:", mlp_prediction)
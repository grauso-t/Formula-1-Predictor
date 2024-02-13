import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
# from sklearn.svm import SVR
# from sklearn.neural_network import MLPRegressor
# from sklearn.preprocessing import StandardScaler
#from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Caricamento dataset
data = pd.read_csv("./balanced_dataset.csv")

# Selezione features e la variabile target
X = data[['driverId', 'circuitId', 'lap', 'weather_code']]
y = data['time_lap']

# Suddivisione dati in set di addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Addestramento del modello RandomForestRegressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Addestramento del modello SVR
# svr_model = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
#svr_model.fit(X_train, y_train)

# Addestramento del modello MLPRegressor
# mlp_model = make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42))
# mlp_model.fit(X_train, y_train)

# Valutazione dei modelli
rf_pred = rf_model.predict(X_test)
# svr_pred = svr_model.predict(X_test)
# mlp_pred = mlp_model.predict(X_test)

rf_rmse = mean_absolute_error(y_test, rf_pred)
# svr_rmse = mean_absolute_error(y_test, svr_pred)
# mlp_rmse = mean_absolute_error(y_test, mlp_pred)

print("mean_absolute_error rf_rmse in secondi", rf_rmse / 10)
# print("mean_absolute_error svr_rmse in secondi", svr_rmse / 10)
# print("mean_absolute_error mlp_rmse in secondi", mlp_rmse / 10)

print("accuracy rf_rmse", r2_score(y_test, rf_pred))
# print("accuracy svr_rmse", r2_score(y_test, svr_pred))
# print("accuracy mlp_rmse", r2_score(y_test, mlp_model))

# Salvataggio modelli e scaler
joblib.dump(rf_model, 'rf_model.pkl')
# joblib.dump(svr_model, 'svr_model.pkl')
# joblib.dump(mlp_model, 'mlp_model.pkl')

print("Modelli addestrati e salvati con successo.")
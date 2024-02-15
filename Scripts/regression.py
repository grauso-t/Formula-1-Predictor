import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
import oversampling
import joblib

# Caricamento dataset
print("Apertura dataset...")
data = pd.read_csv("./merged_dataset_races.csv")

# Suddivisione dati in set di addestramento e test
print("Suddivisione dataset...")
train_data, test_data = train_test_split(data, test_size=0.22, random_state=42)
train_data = oversampling.oversampling(train_data)

# Variabili
X_train_resampled = train_data[['driverId', 'circuitId', 'lap', 'weather_code']]
y_train_resampled = train_data['time_lap']

X_test = test_data[['driverId', 'circuitId', 'lap', 'weather_code']]
y_test = test_data['time_lap']

print("Addestramento ExtraTreesRegressor...")

# Addestramento del modello RandomForestRegressor
et_model = ExtraTreesRegressor(n_estimators=100, random_state=0)
et_model.fit(X_train_resampled, y_train_resampled)

# Valutazione del modello
et_pred = et_model.predict(X_test)
et_rmse = mean_absolute_error(y_test, et_pred)
et_accuracy = r2_score(y_test, et_pred)

print("Mean Absolute Error (RF):", et_rmse / 10)
print("Accuracy (RF):", et_accuracy)

# Salvataggio del modello
joblib.dump(et_model, 'et_model.pkl')

print("Modello Extra Trees Regressor addestrato e salvato con successo.\n")

print("Addestramento RandomForestRegressor...")

# Addestramento del modello RandomForestRegressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_resampled, y_train_resampled)

# Valutazione del modello
rf_pred = rf_model.predict(X_test)
rf_rmse = mean_absolute_error(y_test, rf_pred)
rf_accuracy = r2_score(y_test, rf_pred)

print("Mean Absolute Error (RF):", rf_rmse / 10)
print("Accuracy (RF):", rf_accuracy)

# Salvataggio del modello
joblib.dump(rf_model, 'rf_model.pkl')

print("Modello Random Forest Regressor addestrato e salvato con successo. \n")

print("Addestramento DecisionTreeRegressor...")

# Addestramento del modello Decision Tree
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train_resampled, y_train_resampled)

# Valutazione del modello Decision Tree
dt_pred = dt_model.predict(X_test)
dt_rmse = mean_absolute_error(y_test, dt_pred)
dt_accuracy = r2_score(y_test, dt_pred)

print("Mean Absolute Error (Decision Tree):", dt_rmse / 10)
print("Accuracy (Decision Tree):", dt_accuracy)

# Salvataggio del modello Decision Tree
joblib.dump(dt_model, 'dt_model.pkl')

print("Modello Decision Tree addestrato e salvato con successo.\n")

print("Addestramento GradientBoostingRegressor...")

# Addestramento del modello Gradient Boosting
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train_resampled, y_train_resampled)

# Valutazione del modello Gradient Boosting
gb_pred = gb_model.predict(X_test)
gb_rmse = mean_absolute_error(y_test, gb_pred)
gb_accuracy = r2_score(y_test, gb_pred)

print("Mean Absolute Error (Gradient Boosting):", gb_rmse / 10)
print("Accuracy (Gradient Boosting):", gb_accuracy)

# Salvataggio del modello Gradient Boosting
joblib.dump(gb_model, 'gb_model.pkl')

print("Modello Gradient Boosting addestrato e salvato con successo.")
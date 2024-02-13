import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
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

print("Modello RandomForestRegressor addestrato e salvato con successo.")

# Addestramento del modello Decision Tree
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train, y_train)

# Valutazione del modello Decision Tree
dt_pred = dt_model.predict(X_test)
dt_rmse = mean_absolute_error(y_test, dt_pred)
dt_accuracy = r2_score(y_test, dt_pred)

print("Mean Absolute Error (Decision Tree):", dt_rmse / 10)
print("Accuracy (Decision Tree):", dt_accuracy)

# Salvataggio del modello Decision Tree
joblib.dump(dt_model, 'dt_model.pkl')

print("Modello Decision Tree addestrato e salvato con successo.")

# Addestramento del modello Gradient Boosting
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)

# Valutazione del modello Gradient Boosting
gb_pred = gb_model.predict(X_test)
gb_rmse = mean_absolute_error(y_test, gb_pred)
gb_accuracy = r2_score(y_test, gb_pred)

print("Mean Absolute Error (Gradient Boosting):", gb_rmse / 10)
print("Accuracy (Gradient Boosting):", gb_accuracy)

# Salvataggio del modello Gradient Boosting
joblib.dump(gb_model, 'gb_model.pkl')

print("Modello Gradient Boosting addestrato e salvato con successo.")

# Addestramento del modello di regressione lineare
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Valutazione del modello di regressione lineare
lr_pred = lr_model.predict(X_test)
lr_rmse = mean_absolute_error(y_test, lr_pred)
lr_accuracy = r2_score(y_test, lr_pred)

print("Mean Absolute Error (Linear Regression):", lr_rmse / 10)
print("Accuracy (Linear Regression):", lr_accuracy)

# Salvataggio del modello di regressione lineare
joblib.dump(lr_model, 'lr_model.pkl')

print("Modello di regressione lineare addestrato e salvato con successo.")

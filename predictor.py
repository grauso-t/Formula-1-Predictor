from datetime import timedelta
import pandas as pd

# Carica i dati dai file CSV
results = pd.read_csv(r'./Datasets/results.csv')
races = pd.read_csv(r'./Datasets/races.csv')
qualifying = pd.read_csv(r'./Datasets/qualifying.csv')
drivers = pd.read_csv(r'./Datasets/drivers.csv')
constructors = pd.read_csv(r'./Datasets/constructors.csv')
circuit = pd.read_csv(r'./Datasets/circuits.csv')

# Esegue le fusioni dei dataframe
df1 = pd.merge(races, results, how='inner', on=['raceId'])
df2 = pd.merge(df1, qualifying, how='inner', on=['raceId', 'driverId', 'constructorId'])
df3 = pd.merge(df2, drivers, how='inner', on=['driverId'])
df4 = pd.merge(df3, constructors, how='inner', on=['constructorId'])
df5 = pd.merge(df4, circuit, how='inner', on=['circuitId'], suffixes=('_df4', '_circuit'))

# Rimuove le colonne specificate
columns_to_remove = ['round', 'time_x', 'fp1_time', 'fp2_time', 'fp3_time', 'sprint_date', 'sprint_time', 'laps', 'forename', 'surname', 'nationality_x', 'nationality_y', 'url_circuit', 'url_x', 'resultId', 'quali_time', 'fp1_date', 'fp2_date', 'fp3_date', 'number_x', 'positionText', 'position_x', 'positionOrder', 'driverRef', 'number', 'dob', 'url_y', 'name_y', 'url_df4', 'time_y']
df5 = df5.drop(columns=columns_to_remove, errors='ignore')

# Converte la colonna 'date' al formato datetime
df5['date'] = pd.to_datetime(df5['date'], errors='coerce')

# Identifica le righe con "\N" nella colonna 'quali_date'
rows_with_NA = df5[df5['quali_date'] == '\\N']

# Converte la colonna 'date' al formato datetime solo per le righe con "\N" nella colonna 'quali_date'
df5.loc[rows_with_NA.index, 'date'] = pd.to_datetime(df5.loc[rows_with_NA.index, 'date'], errors='coerce')

# Sottrai un giorno dalla colonna 'date' per le righe con "\N" nella colonna 'quali_date'
df5.loc[rows_with_NA.index, 'quali_date'] = (df5.loc[rows_with_NA.index, 'date'] - pd.to_timedelta(1, unit='d'))

# Converte la colonna 'quali_date' al formato datetime
df5['quali_date'] = pd.to_datetime(df5['quali_date'], errors='coerce')

# Converte la colonna 'quali_date' al formato stringa desiderato "YYYY/MM/DD"
df5['quali_date'] = df5['quali_date'].dt.strftime('%Y-%m-%d')

# Salva il dataframe modificato in un file CSV
df5.to_csv('merged_dataset.csv', index=False)
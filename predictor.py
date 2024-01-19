import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv(r'./merged_dataset_races.csv', low_memory=False)

dataset['date'] = pd.to_datetime(dataset['date'])

# Filtra il DataFrame eliminando le righe con 'date' minore di '2020-01-01'
dataset = dataset[dataset['date'] >= '2022-01-01']

nan_mask = dataset.applymap(lambda x: x == '\\N')
nan_count = nan_mask.sum()

print(nan_count)

# Raggruppa per 'driverId' e conta le occorrenze
conteggio_per_id = dataset.groupby('driverId').size().reset_index(name='numero_occorrenze')

# Crea un grafico a barre
plt.bar(conteggio_per_id['driverId'], conteggio_per_id['numero_occorrenze'])
plt.xlabel('Driver ID')
plt.ylabel('Numero di Occorrenze')
plt.title('Conteggio delle Occorrenze per Driver ID')
plt.show()

conteggio_per_id = dataset.groupby('driverId').size().reset_index(name='numero_occorrenze')

print(len(conteggio_per_id[(conteggio_per_id['numero_occorrenze'] > 2000)]))
print(len(conteggio_per_id[(conteggio_per_id['numero_occorrenze'] <= 2000)]))
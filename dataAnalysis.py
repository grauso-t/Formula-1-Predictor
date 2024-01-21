import pandas as pd

ds = pd.read_csv(r'./merged_dataset_races.csv', low_memory=False)

lista = [1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 45, 50, 128, 53, 55, 58, 88, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125, 127, 133, 134]

# Conta il numero di righe in cui statusId è uguale a uno dei valori nella lista
count = len(ds[ds['statusId'].isin(lista)])

# Totale
print("Ecco il numero di gare che non sono terminate precocemente: " + str(count))

### Buon valore, significa che abbiamo un numero elevato, rispetto al totale, di informazione sui giri

raggruppato_ds = ds.groupby(['raceId', 'driverId', 'driver_name', 'circuitId', 'cirtuit_name', 'race_date', 'time_race']).size().reset_index(name='conteggio')

# Visualizza il DataFrame risultante
print(raggruppato_ds)

raggruppato_ds.to_csv('raggruppato.csv', index=False)

print("Piloti che hanno effettuato almeno 40 giri: " + str(len(raggruppato_ds[(raggruppato_ds['conteggio'] >= 40)])))
# Numero di elementi per la classe "Non sopravvissuti"
print("Piloti che non hanno effettuato almeno 40 giri: " + str(len(raggruppato_ds[(raggruppato_ds['conteggio'] < 40)])))

# Totale
print("Piloti totale: " + str(len(raggruppato_ds)))
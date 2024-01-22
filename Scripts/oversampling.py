import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import RandomOverSampler
import numpy as np

df = pd.read_csv(r'./merged_dataset_races.csv', low_memory=False)

lista = [1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 45, 50, 128, 53, 55, 58, 88, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125, 127, 133, 134]
valutazione_giri = 1000

df_filtrato = df[df['statusId'].isin(lista)]

raggruppato_ds = df_filtrato.groupby(['driverId', 'driver_name']).size().reset_index(name='conteggio')

raggruppato_ds_filtrato = raggruppato_ds[raggruppato_ds['conteggio'] > valutazione_giri]

media_desiderata = raggruppato_ds_filtrato['conteggio'].mean()


raggruppato_ds_filtrato = raggruppato_ds[raggruppato_ds['conteggio'] <= valutazione_giri]

media_attuale = raggruppato_ds_filtrato['conteggio'].mean()

differenza_media = media_desiderata - media_attuale
differenza_media = differenza_media.round().astype(int)

print(f"Media desiderata: {media_desiderata}, media attuale: {media_attuale}. Differenza: {differenza_media}")

raggruppato_ds_filtrato['giri_da_aggiungere'] = differenza_media.round().astype(int)

print(raggruppato_ds_filtrato)

driver_ids_da_replicare = raggruppato_ds_filtrato['driverId'].tolist()

print(driver_ids_da_replicare)

nuovi_giri = pd.DataFrame()

for driver_id in driver_ids_da_replicare:
    giri_driver = df[df['driverId'] == driver_id]

    if len(giri_driver) < differenza_media:
        giri_replicati = pd.concat([giri_driver] * (differenza_media // len(giri_driver)) + [giri_driver.head(differenza_media % len(giri_driver))])
    else:
        giri_replicati = giri_driver.sample(n=differenza_media, replace=True)

    nuovi_giri = pd.concat([nuovi_giri, giri_replicati])

nuovi_giri.to_csv(r'./nuovi_giri_replicati.csv', index=False)

df_finale = pd.concat([df, nuovi_giri])

raggruppato_ds = df_finale.groupby(['driverId', 'driver_name']).size().reset_index(name='conteggio')
raggruppato_ds.to_csv(r'./merged_dataset_races_balanced.csv', index=False)

plt.figure(figsize=(12, 8))
sns.barplot(x='conteggio', y='driver_name', data=raggruppato_ds, orient='h', color='red')
plt.title('Numero di giri effettuati da ogni pilota nelle stagioni 2022 e 2023')
plt.xlabel('Giri effettuati')
plt.ylabel('Pilota')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import RandomOverSampler
import numpy as np

# Load the dataset
ds = pd.read_csv(r'./merged_dataset_races.csv', low_memory=False)

lista = [1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 45, 50, 128, 53, 55, 58, 88, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125, 127, 133, 134]

# Count the number of rows where 'statusId' is in the given list
count = len(ds[ds['statusId'].isin(lista)])

# Print the total count
print("Ecco il numero di gare che non sono terminate precocemente: " + str(count))

# Group by 'driverId' and 'driver_name' and sum the number of laps
raggruppato_ds = ds.groupby(['driverId', 'driver_name']).size().reset_index(name='conteggio')

# Compute class weights
class_weights = compute_class_weight('balanced', classes=np.unique(raggruppato_ds['conteggio']), y=raggruppato_ds['conteggio'])
class_weight_dict = dict(zip(np.unique(raggruppato_ds['conteggio']), class_weights))

# Display the resulting DataFrame
print(raggruppato_ds)

# Save the grouped DataFrame to a CSV file
raggruppato_ds.to_csv('raggruppato.csv', index=False)

# Print the number of drivers who have completed at least 40 laps
print("Piloti che hanno effettuato almeno 40 giri: " + str(len(raggruppato_ds[(raggruppato_ds['conteggio'] >= 40)])))

# Print the number of drivers who have not completed at least 40 laps
print("Piloti che non hanno effettuato almeno 40 giri: " + str(len(raggruppato_ds[(raggruppato_ds['conteggio'] < 40)])))

# Print the total number of drivers
print("Piloti totale: " + str(len(raggruppato_ds)))

# Apply oversampling specifically to the number of laps
X = raggruppato_ds.drop('conteggio', axis=1)
y = raggruppato_ds['conteggio']

ros = RandomOverSampler(sampling_strategy='auto', random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)

# Create a new DataFrame with the resampled data
resampled_ds = pd.DataFrame({'driverId': X_resampled['driverId'], 'driver_name': X_resampled['driver_name'], 'conteggio': y_resampled})

# Visualize the resampled DataFrame
print(resampled_ds)

# Save the resampled DataFrame to a CSV file
resampled_ds.to_csv('resampled_raggruppato.csv', index=False)

# Show the plot
plt.figure(figsize=(12, 8))
sns.barplot(x='conteggio', y='driver_name', data=resampled_ds, orient='h', color='red')
plt.title('Numero di giri effettuati da ogni pilota nelle stagioni 2022 e 2023')
plt.xlabel('Giri effettuati')
plt.ylabel('Pilota')
plt.show()

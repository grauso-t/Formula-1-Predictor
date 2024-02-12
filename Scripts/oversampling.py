import pandas as pd
import numpy as np

# Caricamento dataset
balanced_df = pd.read_csv(r'./merged_dataset_races.csv')

# Numero di giri da raggiungere
desired_laps = 600

# Calcolo del numero minimo di giri
min_laps = balanced_df.groupby('driverId').size().min()

# Bilanciamento del dataset
for driver_id, group in balanced_df.groupby('driverId'):
    num_laps = len(group)
    if num_laps < desired_laps:
        # Add laps
        additional_laps = desired_laps - num_laps
        additional_samples = group.sample(n=additional_laps, replace=True)
        balanced_df = pd.concat([balanced_df, additional_samples])
        print(f"Added {additional_laps} laps for driver {group['driver_name'].iloc[0]}")
    # elif num_laps > desired_laps:
        # Remove laps
    #     remove_indices = group.sample(n=num_laps - desired_laps).index
    #     balanced_df = balanced_df.drop(remove_indices)
    #    print(f"Removed {num_laps - desired_laps} laps for driver {group['driver_name'].iloc[0]}")

# Salvataggio dataset
balanced_df.to_csv(r'./balanced_dataset.csv', index=False)

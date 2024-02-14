import pandas as pd
import random

def oversampling(dataset):
    # Numero di giri da raggiungere
    max_laps = dataset.groupby('driverId').size().max()

    # Bilanciamento del dataset
    for driver_id, group in dataset.groupby('driverId'):
        num_laps = len(group)
        desired_laps = random.randint(max_laps - 800, max_laps)
        if num_laps < desired_laps:
            # Add laps
            additional_laps = desired_laps - num_laps
            additional_samples = group.sample(n=additional_laps, replace=True)
            dataset = pd.concat([dataset, additional_samples])

    return dataset
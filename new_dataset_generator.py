import pandas as pd

lap_times = pd.read_csv(r'./Datasets/lap_times.csv', low_memory=False)
race = pd.read_csv(r'aaaa.csv', low_memory=False)

merge = pd.merge(race, lap_times, how='left', on=['raceId'])

merge.to_csv('aaaaa.csv', index=False)
import pandas as pd

lap_times = pd.read_csv(r'./Datasets/lap_times.csv', low_memory=False)
results = pd.read_csv(r'./Datasets/results.csv', low_memory=False)
drivers = pd.read_csv(r'./Datasets/drivers.csv', low_memory=False)
races = pd.read_csv(r'./Datasets/races.csv', low_memory=False)
status = pd.read_csv(r'./Datasets/status.csv', low_memory=False)
circuit = pd.read_csv(r'./Datasets/circuits.csv', low_memory=False)

merge1 = pd.merge(lap_times, drivers, how='left', on=['driverId'])
merge1 = merge1.rename(columns={'position': f'position_lap'})
merge1 = merge1.rename(columns={'time': f'time_lap'})
merge1 = merge1.rename(columns={'milliseconds': f'milliseconds_lap'})
merge1 = merge1.rename(columns={'number': f'number_driver'})
merge1 = merge1.drop('url', axis=1)
merge1 = merge1.drop('driverRef', axis=1)
merge1['driver_name'] = merge1['forename'] + ' ' + merge1['surname']
merge1 = merge1.drop(['forename', 'surname'], axis=1)
merge1 = merge1.drop(['dob', 'nationality'], axis=1)
merge1 = merge1.drop(['number_driver', 'code'], axis=1)

merge2 = pd.merge(merge1, races, how='left', on=['raceId'])
merge2 = merge2.rename(columns={'time': f'time_race'})
merge2 = merge2.drop(['year', 'round', 'url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'sprint_time'], axis=1)

merge3 = pd.merge(merge2, results, how='left', on=['raceId', 'driverId'])
merge3 = merge3.drop(['constructorId'], axis=1)

merge4 = pd.merge(merge3, status, how='left', on=['statusId'])

merge5 = pd.merge(merge4, circuit, how='left', on=['circuitId'])

merge5.to_csv('merged_dataset_races.csv', index=False)
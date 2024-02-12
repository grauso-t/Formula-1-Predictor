import pandas as pd
import openmeteo_requests
import requests_cache

from retry_requests import retry

# Apertura dei file datasets
lap_times = pd.read_csv(r'./Datasets/lap_times.csv', low_memory=False)
results = pd.read_csv(r'./Datasets/results.csv', low_memory=False)
drivers = pd.read_csv(r'./Datasets/drivers.csv', low_memory=False)
races = pd.read_csv(r'./Datasets/races.csv', low_memory=False)
status = pd.read_csv(r'./Datasets/status.csv', low_memory=False)
circuits = pd.read_csv(r'./Datasets/circuits.csv', low_memory=False)

# Operazioni di merge e pulizia dei datasets
merge1 = pd.merge(lap_times, drivers, how='left', on=['driverId'])
merge1['driver_name'] = merge1['forename'] + ' ' + merge1['surname']
merge1 = merge1.rename(columns={'number': f'number_driver', 'milliseconds': f'time_lap', 'position': f'position_lap'})
merge1 = merge1.drop(['number_driver', 'code', 'url', 'time', 'driverRef', 'forename', 'surname', 'dob', 'nationality'], axis=1)

merge2 = pd.merge(merge1, races, how='left', on=['raceId'])
merge2 = merge2.rename(columns={'time': f'time_race'})
merge2 = merge2.drop(['year', 'round', 'url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'sprint_time'], axis=1)

merge3 = pd.merge(merge2, results, how='left', on=['raceId', 'driverId'])
merge3 = merge3.rename(columns={'name': f'circuit_name'})
merge3 = merge3.drop(['resultId','number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed'], axis=1)

merge4 = pd.merge(merge3, status, how='left', on=['statusId'])
merge4 = merge4.rename(columns={'date': f'race_date'})

merge5 = pd.merge(merge4, circuits, how='left', on=['circuitId'])
merge5 = merge5.drop(['circuitRef', 'name', 'location', 'country', 'url'], axis=1)







ds_final = merge5[merge5['race_date'] >= '2022-01-01']

grouped_ds = ds_final.groupby('raceId')

# Configurazione delle API Open-Meteo
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

final_results = pd.DataFrame()

# Iterazione sui gruppi, in modo da eseguire meno richieste alle API
for race_id, group_df in grouped_ds:

    latitude = str(group_df['lat'].iloc[0])
    longitude = str(group_df['lng'].iloc[0])
    date = group_df['race_date'].iloc[0]
    time_str = str(group_df['time_race'].iloc[0])
    hour = int(time_str.split(':')[0])

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "hourly": ["weather_code"]
    }

    # Operazioni per ottenere il meteo per ogni data
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_weather_code = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["weather_code"] = hourly_weather_code
    group_df['weather_code'] = hourly_data["weather_code"][hour]
    
    final_results = final_results._append(group_df, ignore_index=True)

# Mapping codice meteo
wmo_mapping = {
    0: 'Clear sky',
    1: 'Clear sky',
    2: 'Cloudy',
    3: 'Cloudy',
    4: 'Cloudy',
    5: 'null',
    10: 'null',
    45: 'null',
    50: 'Rain',
    51: 'Rain',
    52: 'Rain',
    53: 'Rain',
    54: 'null',
    55: 'Rain',
    56: 'null',
    57: 'null',
    58: 'null',
    60: 'Rain',
    61: 'null',
    62: 'Rain',
    63: 'Rain',
    64: 'Rain',
    65: 'Rain',
    66: 'Rain',
    67: 'Rain',
    68: 'Rain',
    70: 'null',
    71: 'null',
    72: 'null',
    73: 'null',
    74: 'null',
    75: 'null',
}

# Conversione dei weather_code in descrizione testuale
final_results['weather_description'] = final_results['weather_code'].map(wmo_mapping)

# Ordinamento del dataset
new_order = ['raceId', 'driverId', 'driver_name', 'circuitId', 'circuit_name', 'race_date', 'time_race', 'lap', 'position_lap', 'time_lap', 'statusId', 'status', 'weather_code', 'weather_description']
final_results = final_results[new_order]

# Conversione dei millisecondi in decimi di secondo
# final_results['time_lap'] = final_results['time_lap'] / 100

# Salvataggio del dataset finale
final_results.to_csv('merged_dataset_races.csv', index=False)
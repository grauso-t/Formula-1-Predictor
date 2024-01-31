import pandas as pd
import openmeteo_requests
import requests_cache

from retry_requests import retry

lap_times = pd.read_csv(r'./Datasets/lap_times.csv', low_memory=False)
results = pd.read_csv(r'./Datasets/results.csv', low_memory=False)
drivers = pd.read_csv(r'./Datasets/drivers.csv', low_memory=False)
races = pd.read_csv(r'./Datasets/races.csv', low_memory=False)
status = pd.read_csv(r'./Datasets/status.csv', low_memory=False)
circuits = pd.read_csv(r'./Datasets/circuits.csv', low_memory=False)

merge1 = pd.merge(lap_times, drivers, how='left', on=['driverId'])
merge1['driver_name'] = merge1['forename'] + ' ' + merge1['surname']
merge1 = merge1.rename(columns={'number': f'number_driver', 'milliseconds': f'time_lap', 'position': f'position_lap'})
merge1 = merge1.drop(['number_driver', 'code', 'url', 'time', 'driverRef', 'forename', 'surname', 'dob', 'nationality'], axis=1)

merge2 = pd.merge(merge1, races, how='left', on=['raceId'])
merge2 = merge2.rename(columns={'time': f'time_race'})
merge2 = merge2.drop(['year', 'round', 'url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'sprint_time'], axis=1)

merge3 = pd.merge(merge2, results, how='left', on=['raceId', 'driverId'])
merge3 = merge3.rename(columns={'name': f'cirtuit_name'})
merge3 = merge3.drop(['constructorId', 'resultId','number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed'], axis=1)

merge4 = pd.merge(merge3, status, how='left', on=['statusId'])
merge4 = merge4.rename(columns={'date': f'race_date'})

merge5 = pd.merge(merge4, circuits, how='left', on=['circuitId'])

ds_final = merge5[merge5['race_date'] >= '2022-01-01']

grouped_ds = ds_final.groupby('raceId')

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Create an empty DataFrame to store the final results
final_results = pd.DataFrame()

# Iterate over groups
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
    
    # Append the modified group DataFrame to the final results
    final_results = final_results._append(group_df, ignore_index=True)

wmo_mapping = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Cloudy',
    4: 'Overcast',
    5: 'Mist',
    10: 'Patchy fog',
    45: 'Fog',
    50: 'Freezing drizzle',
    51: 'Drizzle',
    52: 'Freezing rain',
    53: 'Rain',
    54: 'Snow',
    55: 'Thunderstorm',
    56: 'Sleet',
    57: 'Hail',
    58: 'Freezing spray',
    60: 'Showers of rain',
    61: 'Showers of snow',
    62: 'Showers of rain and snow',
    63: 'Showers of hail',
    64: 'Showers of rain and hail',
    65: 'Showers of snow and hail',
    66: 'Showers of rain, snow, and hail',
    67: 'Drizzle and rain',
    68: 'Drizzle and snow',
    70: 'Widespread dust',
    71: 'Duststorm or sandstorm',
    72: 'Volcanic ash',
    73: 'Squalls',
    74: 'Funnel cloud',
    75: 'Tornado',
}

final_results['weather_description'] = final_results['weather_code'].map(wmo_mapping)

new_order = ['raceId', 'driverId', 'driver_name', 'circuitId', 'cirtuit_name', 'race_date', 'time_race', 'lap', 'position_lap', 'time_lap', 'statusId', 'status', 'weather_code', 'weather_description']
final_results = final_results[new_order]

# Save the final results to a CSV file
final_results.to_csv('merged_dataset_races.csv', index=False)
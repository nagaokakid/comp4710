
import os
import pandas as pd

data = pd.read_csv(os.getcwd() + '/passup_anomaly/pass_up_with_stopID.csv')
data['Time'] = pd.to_datetime(data['Time'])

list_of_routes = data['Route Number'].unique()

# Count total number of pass-up for each route and save to csv file
for route in list_of_routes:
    stops_passup = data[data['Route Number'] == route]
    stops_passup = stops_passup.groupby(
        ['stop_id']).size().reset_index(name='count')
    stops_passup = stops_passup.sort_values('count', ascending=False)
    stops_passup = stops_passup.reset_index(drop=True)
    stops_passup.to_csv(
        os.getcwd() + '/passup_anomaly/stops_data/' + route + '.csv', index=False)


# Pass up data for each route
for route in list_of_routes:
    route_data = data[data['Route Number'] == route]
    route_data = route_data.sort_values('Time', ascending=False)
    route_data = route_data.reset_index(drop=True)
    route_data.to_csv(
        os.getcwd() + '/passup_anomaly/route_data/' + route + '.csv', index=False)

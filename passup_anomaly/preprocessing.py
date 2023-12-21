
import os
import pandas as pd

data = pd.read_csv('pass_up_with_stopID.csv')
data['Time'] = pd.to_datetime(data['Time'])

list_of_routes = data['Route Number'].unique()


# Count total number of pass-up for each route and save to csv file
def stops_data():
    for route in list_of_routes:
        stops_passup = data[(data['Route Number'] == route) & (
            data['Time'] >= '2022-09-01') & (data['Time'] <= '2022-12-31')]
        stops_passup = stops_passup.groupby(
            ['stop_id']).size().reset_index(name='count')
        stops_passup = stops_passup.sort_values('count', ascending=False)
        stops_passup = stops_passup.reset_index(drop=True)
        stops_passup.to_csv('stops_data/' + route + '.csv', index=False)


# Pass up data for each route
def route_data():
    for route in list_of_routes:
        route_data = data[(data['Route Number'] == route) & (
            data['Time'] >= '2022-09-01') & (data['Time'] <= '2022-12-31')]
        route_data = route_data.sort_values('Time', ascending=False)
        route_data = route_data.reset_index(drop=True)
        route_data.to_csv('route_data/' + route + '.csv', index=False)

# Count number of pass-up each day for each route


def route_passup():
    for route in list_of_routes:
        route_data = data[(data['Route Number'] == route) & (
            data['Time'] >= '2022-01-01') & (data['Time'] <= '2022-12-31')].copy()
        route_data['Time'] = pd.to_datetime(route_data['Time']).dt.date
        if not route_data.empty:
            route_data = route_data.groupby(
                'Time').size().reset_index(name='Passup')
            route_data = route_data.sort_values('Time', ascending=False)
            route_data = route_data.reset_index(drop=True)
            # Set 'Time' as index
            route_data.set_index('Time', inplace=True)
            date_range = pd.date_range(
                start=route_data.index.min(), end=route_data.index.max())
            # Reindex with date range
            route_data_reindexed = route_data.reindex(
                date_range, fill_value=0).rename_axis('Time').reset_index()
            route_data_reindexed = route_data_reindexed.sort_values(
                'Time', ascending=False)
            # Save to csv file
            route_data_reindexed.to_csv('route_passup/' + route + '.csv', index=False)
            print('Route: ', route)


def main():
    stops_data()
    route_data()
    route_passup()


main()

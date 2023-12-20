import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def time_series(pass_up, decomposition, route_number):
    # Plotting the decomposed time series components
    plt.figure(figsize=(14, 7))

    # Trend Component
    plt.subplot(411)
    plt.plot(decomposition.trend, label='Trend')  # Added marker
    plt.legend(loc='upper left')

    # Seasonal Component
    plt.subplot(412)
    plt.plot(decomposition.seasonal, label='Seasonal')  # Added marker
    plt.legend(loc='upper left')

    # Residual Component
    plt.subplot(413)
    plt.plot(decomposition.resid, label='Residual')  # Added marker
    plt.legend(loc='upper left')

    # Original Series
    plt.subplot(414)
    plt.plot(pass_up, label='Original', marker='o')  # Added marker
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig(os.getcwd() + '/passup_anomaly/time_series/' +
                route_number+'.png')
    plt.close()


def anomaly_detection(decomposition, route_number):
    residual = decomposition.resid
    # Extract anomalies from residual with more than 2 standard deviations from the mean
    mean = np.mean(residual)
    sd = np.std(residual)
    anomaly_line = sd * 1

    # Cross the threshold line
    lower_threshold = mean - anomaly_line
    upper_threshold = mean + anomaly_line
    anomalies = residual[(residual < lower_threshold) |
                         (residual > upper_threshold)]

    # Dates of anomalies
    anomalies_df = anomalies.to_frame(name='Residual values')
    anomalies_df['Date'] = anomalies_df.index
    anomalies_df.reset_index(drop=True, inplace=True)  # Modify df inplace
    anomalies_df['Date'].to_csv(
        os.getcwd()+'/passup_anomaly/anomaly_dates/'+route_number+'.csv', index=False, header=False)

    # Plot the anomalies
    plt.figure(figsize=(12, 6))
    plt.plot(residual, label='Residual')
    plt.axhline(mean, color='gray', linestyle='--', label='Mean')
    plt.axhline(lower_threshold, color='red',
                linestyle='--', label='Lower Threshold')
    plt.axhline(upper_threshold, color='red',
                linestyle='--', label='Upper Threshold')
    plt.scatter(anomalies.index, anomalies, color='lawngreen', label='Anomaly')
    plt.legend()
    plt.title('Residual based for Anomaly Detection')
    plt.savefig(os.getcwd() + '/passup_anomaly/anomaly_detection/' +
                route_number+'.png')
    plt.close()


def plot_passup(route_number):
    data = pd.read_csv(
        os.getcwd() + '/passup_anomaly/route_passup/'+route_number+'.csv')
    data['Time'] = pd.to_datetime(data['Time'])
    data = data[(data['Time'] >= '2022-01-01') &
                (data['Time'] <= '2022-12-31')]
    plt.figure(figsize=(12, 6))
    plt.plot(data['Time'], data['Passup'], label='Pass-up')
    plt.legend()
    plt.title('Pass-up for Route' + route_number)
    plt.savefig(os.getcwd() + '/passup_anomaly/route_passup_img/' +
                route_number + '.png')
    plt.close()


def main():
    list_of_routes = pd.read_csv(
        os.getcwd() + '/passup/all-routes.csv', header=None)
    list_of_routes = list_of_routes[0].unique()
    # Get 10 most popular routes
    list_of_routes = ['11', 'BLUE', '75', '47',
                      '60', '36', '672', '33', '24', '14']

    for route in list_of_routes:
        data = pd.read_csv(
            os.getcwd() + '/passup_anomaly/route_data/' + route + '.csv')

        # Convert 'Time' to datetime and sort the data
        data['Time'] = pd.to_datetime(data['Time'])
        data.sort_values('Time', inplace=True)
        data = data[(data['Time'] >= '2022-09-01') &
                    (data['Time'] <= '2022-12-30')]
        if not data.empty:
            # Resample the data by day and create a time series of the count of pass-ups per day
            pass_ups = data.resample('D', on='Time').size()

            # Perform time series decomposition
            decomposition = seasonal_decompose(pass_ups, model='additive')
            print('ROUTE NUMBER: ', route)
            time_series(pass_ups, decomposition, route)
            anomaly_detection(decomposition, route)

            # Plot pass-up for each route
            plot_passup(route)
        else:
            print('Route: ' + route + ' is empty')


main()

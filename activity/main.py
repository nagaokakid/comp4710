import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
passenger_activity_data = pd.read_csv(os.getcwd() +
                                      '/Estimated_Daily_Passenger_Activity.csv')

seasons_order = {
    'Winter': 1,
    'Spring': 2,
    'Summer': 3,
    'Fall': 4
}

# Function to create sortable period key


def get_sort_key(period_name):
    # Split period name into season and year
    token = period_name.split(' ')
    season = token[0]
    year = token[1]
    # Map season to sort key and combine with year
    return int(year) * 100 + seasons_order[season]


def season_trend():
    # Create a new column for the period name and sort by it
    passenger_activity_data['sort_key'] = passenger_activity_data['Schedule Period Name'].apply(
        get_sort_key)
    # print(passenger_activity_data.head())

    seasonal_trends = passenger_activity_data.sort_values('sort_key').groupby(
        'Schedule Period Name')[['Average Boardings']].sum()
    # print(seasonal_trends.head())
    # todo need to sort base on season

    # Plotting
    seasonal_trends.plot(kind='bar')
    plt.title('Seasonal Trends in Passenger Activity')
    plt.ylabel('Total Passengers')
    plt.xlabel('Schedule Period')
    plt.show()


def day_type():
    day_type_analysis = passenger_activity_data.groupby(
        'Day Type')[['Average Boardings']].sum()
    print(day_type_analysis.head())
    day_type_analysis.plot(kind='bar')
    plt.title('Day Type in Passenger Activity')
    plt.ylabel('Total Passengers')
    plt.xlabel('Day Type')
    plt.show()


def time_of_day_trend():
    time_of_day_trends = passenger_activity_data.groupby(
        'Time Period')[['Average Boardings']].mean()

    # Plotting
    time_of_day_trends.plot(kind='bar')
    plt.title('Passenger Activity by Time of Day')
    plt.ylabel('Average Passengers')
    plt.xlabel('Time Period')
    plt.show()


def route_and_stop():
    # Convert 'Schedule Period Start Date' to datetime if not already done
    passenger_activity_data['Schedule Period Start Date'] = pd.to_datetime(
        passenger_activity_data['Schedule Period Start Date'])

    # Extract the year and create a new column
    passenger_activity_data['Year'] = passenger_activity_data['Schedule Period Start Date'].dt.year

    # Setting the number of routes and stops to display
    top_n = 10

    # Grouping by year, then route and stop, and calculating sum passenger activity
    busiest_by_year = passenger_activity_data.groupby(['Year', 'Route Number', 'Stop Number'])[
        'Average Boardings'].sum().sort_values(ascending=False).groupby(level=0).head(top_n)

    # Plotting for each year
    for year in busiest_by_year.index.get_level_values(0).unique():
        busiest_by_year.loc[year].plot(kind='bar', color='skyblue')
        plt.title('Top {} Busiest Routes and Stops in {}'.format(top_n, year))
        plt.ylabel('Average Total Passenger Activity')
        plt.xlabel('Route and Stop Numbers')
        plt.xticks(rotation=45)
        plt.show()


def main():
    # Convert date columns to datetime objects
    passenger_activity_data['Schedule Period Start Date'] = pd.to_datetime(
        passenger_activity_data['Schedule Period Start Date'])
    passenger_activity_data['Schedule Period End Date'] = pd.to_datetime(
        passenger_activity_data['Schedule Period End Date'])

    # Seasonal trend
    # season_trend()

    # Day type analysis
    # day_type()

    # Time of day trend
    # time_of_day_trend()

    # Busiest routes and stops
    # route_and_stop()


if __name__ == '__main__':
    main()

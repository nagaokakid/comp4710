import pandas
import matplotlib.pyplot as plt
import os
from sodapy import Socrata


MAX_ROWS = 170000  # set contains around 160k rows
PASSENGER_ACTIVITY_DATA_ID = "bv6q-du26"

client = Socrata(domain="data.winnipeg.ca",
                 app_token="VF3YwehWPH23DdQjpIcvm5YS1",
                 username="coopera@myumanitoba.ca",
                 password="Comp4710!")


def getPassengerData() -> pandas.DataFrame:
    # find rows with full pass-up type only
    queryStr = f"schedule_period_name LIKE '%2022'"
    results = client.get(PASSENGER_ACTIVITY_DATA_ID,
                         limit=MAX_ROWS, where=queryStr)   # we get back JSON
    results_df = pandas.DataFrame.from_records(
        results)     # convert to data frame
    client.close()
    return results_df       # return a data frame


# Load the data
passenger_activity_data = getPassengerData()
print(passenger_activity_data.head())

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
    passenger_activity_data['sort_key'] = passenger_activity_data['schedule_period_name'].apply(
        get_sort_key)
    # print(passenger_activity_data.head())

    seasonal_trends = passenger_activity_data.sort_values('sort_key').groupby(
        'schedule_period_name')[['average_boardings']].sum()
    # print(seasonal_trends.head())
    # todo need to sort base on season

    # Plotting
    fig, ax = plt.subplots()
    seasonal_trends.plot(kind='bar', ax=ax)
    plt.title('Seasonal Trends in Passenger Activity')
    plt.ylabel('Total Passengers')
    plt.xlabel('Schedule Period')
    fig.subplots_adjust(bottom=0.38)
    plt.savefig('seasonal_trends.png')
    plt.close()


def day_type():
    day_type_analysis = passenger_activity_data.groupby(
        'day_type')[['average_boardings']].sum()
    print(day_type_analysis.head())
    day_type_analysis.plot(kind='bar')
    fig, ax = plt.subplots()
    day_type_analysis.plot(kind='bar', ax=ax)
    plt.title('Day Type in Passenger Activity')
    plt.ylabel('Total Passengers')
    plt.xlabel('Day Type')
    fig.subplots_adjust(bottom=0.38)
    plt.savefig('day_type.png')
    plt.close()


def time_of_day_trend():
    time_of_day_trends = passenger_activity_data.groupby(
        'time_period')[['average_boardings']].mean()

    # Plotting
    fig, ax = plt.subplots()
    time_of_day_trends.plot(kind='bar', ax=ax)
    plt.title('Passenger Activity by Time of Day')
    plt.ylabel('Average Passengers')
    plt.xlabel('Time Period')
    fig.subplots_adjust(bottom=0.38)
    plt.savefig('time_of_day_trends.png')
    plt.close()


def route_and_stop():
    # Convert 'Schedule Period Start Date' to datetime if not already done
    passenger_activity_data['schedule_period_start_date'] = pandas.to_datetime(
        passenger_activity_data['schedule_period_start_date'])

    # Extract the year and create a new column
    passenger_activity_data['year'] = passenger_activity_data['schedule_period_start_date'].dt.year

    # Setting the number of routes and stops to display
    top_n = 10

    # Grouping by year, then route and stop, and calculating sum passenger activity
    busiest_by_year = passenger_activity_data.groupby(['year', 'route_number', 'stop_number'])[
        'average_boardings'].sum().sort_values(ascending=False).groupby(level=0).head(top_n)

    # Plotting for each year
    for year in busiest_by_year.index.get_level_values(0).unique():
        fig, ax = plt.subplots()
        busiest_by_year.loc[year].plot(kind='bar', color='skyblue', ax=ax)
        plt.title('Top {} Busiest Routes and Stops in {}'.format(top_n, year))
        plt.ylabel('Average Total Passenger Activity')
        plt.xlabel('Route and Stop Numbers')
        plt.xticks(rotation=45)
        fig.subplots_adjust(bottom=0.38)
        plt.savefig('busiest_routes_and_stops_{}.png'.format(year))
        plt.close()


def main():
    # Convert date columns to datetime objects
    passenger_activity_data['schedule_period_start_date'] = pandas.to_datetime(
        passenger_activity_data['schedule_period_start_date'])
    passenger_activity_data['schedule_period_end_date'] = pandas.to_datetime(
        passenger_activity_data['schedule_period_end_date'])
    passenger_activity_data['average_boardings'] = pandas.to_numeric(
        passenger_activity_data['average_boardings'])

    # Seasonal trend
    season_trend()

    # Day type analysis
    day_type()

    # Time of day trend
    time_of_day_trend()

    # Busiest routes and stops
    route_and_stop()


if __name__ == '__main__':
    main()

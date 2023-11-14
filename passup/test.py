#!/usr/bin/env python

# Make sure to run these two commands beforehand to install the required packages:
# 1) pip install pandas
# 2) pip install sodapy

import csv
import pandas
from sodapy import Socrata

PASS_UP_DATA_ID = "mer2-irmb"               # last URI field for pass up data set
PASSENGER_ACTIVITY_DATA_ID = "bv6q-du26"    # last URI field for passenger activity data set
CSV_FILE_PATH = "results.csv"               # local csv file
PASS_UP_MAX_ROWS = 170000                   # pass up data set contains around 160k rows
PASSENGER_ACTIVITY_MAX_ROWS = 1730000       # passenger activity data set contains around 1.71 million rows

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.winnipeg.ca", None)

# Authenticated client (less throttling when sending requests):
client = Socrata(domain="data.winnipeg.ca",
                 app_token="VF3YwehWPH23DdQjpIcvm5YS1",
                 username="coopera@myumanitoba.ca",
                 password="Comp4710!")

# -------------------------------------------------------------------------------

def findTotalPassupsByYear(year : str) -> pandas.DataFrame:
    
    # RESULT 1 - Find the frequency of pass-ups for every route number in 2023
    start_date = f'{year}-01-01T00:00:01'
    end_date = f'{year}-12-31T23:59:59'

    # get all rows that occurred btwn start date and end date
    results = client.get(PASS_UP_DATA_ID, where=f"time >= '{start_date}' AND time <= '{end_date}'", limit=PASS_UP_MAX_ROWS)

    # Convert JSON response from API to DataFrame object
    results_df = pandas.DataFrame.from_records(results)

    # display all rows
    pandas.set_option('display.max_rows', None)

    # calculate the frequency for each route number
    value_counts = results_df['route_number'].value_counts().reset_index()

    # assign column names to value counts
    value_counts.columns = ['Route Number', 'Pass-Ups']

    return value_counts


# Main -------
years = ["2023", "2022", "2021", "2020", "2019"]        # the past 5 years
data_frames_dict = {}                                   # data frames dictionary

for year in years:
    total_passups = findTotalPassupsByYear(year)        # get total pass ups per route for a given year
    data_frames_dict[year] = total_passups              # add data frame result to dictionary

with open(CSV_FILE_PATH, mode='w', newline='') as file:     # empty contents of csv file
    pass 

for key, value in data_frames_dict.items():                     # append title with data frame to csv file
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"Total Pass-Ups for {key}"])
        value.to_csv(file, mode="a", header=True, index=False)
        writer.writerow([])

# ---------------------------------------------------------------------------------

# RESULT 2



# close API client
client.close()
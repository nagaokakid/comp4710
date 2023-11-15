#!/usr/bin/env python

# Make sure to run these two commands beforehand to install the required packages:
# 1) pip install pandas
# 2) pip install sodapy

import csv
import pandas
from sodapy import Socrata
from aggregator import Aggregator as ag
import dataCollector as dc

PASS_UP_DATA_ID = "mer2-irmb"               # last URI field for pass up data set
PASSENGER_ACTIVITY_DATA_ID = "bv6q-du26"    # last URI field for passenger activity data set
PASS_UP_MAX_ROWS = 170000                   # pass up data set contains around 160k rows
PASSENGER_ACTIVITY_MAX_ROWS = 1730000       # passenger activity data set contains around 1.71 million rows


def main():
    print("\nStarting pass-up data collection...")

    results_df = dc.getPassupData()
    print("Retrieved " + str(len(results_df)) + " rows from pass-up database.\n")

    aggregator = ag(results_df)
    
    print("Initiating data mining procedures...")
    years = [2022, 2021, 2020, 2019, 2018, 2017]

    print("Phase 1: Calculate total pass-ups per year")
    aggregator.findTotalPassupsForAllYears(years)
    print("DONE")

    print("Phase 2: Calculate total pass-ups by route per year")
    aggregator.findTotalPassupsByRouteForAllYears(years)
    print("DONE")

    print("Phase 3: Calculate total pass-ups by month per year")
    aggregator.findTotalPassupsByMonthForAllYears(years)
    print("DONE")



# executes main method if file is ran directly (not imported as module)
if __name__ == "__main__":
    main()
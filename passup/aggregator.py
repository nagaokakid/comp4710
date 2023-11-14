import csv
import pandas
from typing import List


class Aggregator:

    # constructor
    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.data_frame["time"] = pandas.to_datetime(self.data_frame["time"])   # convert values in "time" column to datetime objs
    

    # create a custom CSV file name for a result
    def makeCSVFilename(self, appendName: str) -> str:
        return f"{appendName}.csv"
    

    # filter down data frame based on a given year for the column "time"
    def filterPassupsDataFrameByYear(self, target_year: str) -> pandas.DataFrame:
        # start_date = f"{year}-01-01T00:00:00"       # beginning of the year
        # end_date = f"{year}-12-31T23:59:59"         # end of the year

        filtered_df = self.data_frame[self.data_frame["time"].dt.year == target_year]

        # queryStr = f"time between '{start_date}' and '{end_date}' and pass_up_type = '{PASS_UP_TYPE_FULL}'"
        # # soql = f"SELECT * WHERE time between '{start_date}' and '{end_date}'"

        # results = self.client.get(PASS_UP_DATA_ID, limit=PASS_UP_MAX_ROWS, where=queryStr)  # get data w/ query
        # results_df = pandas.DataFrame.from_records(results)
        # results = self.client.get(PASS_UP_DATA_ID, query=soql)

        return filtered_df  # find total number of passups for the year (row count)
    

    # find total passups per year, then write to CSV file
    def findTotalPassupsForAllYears(self, years: List[int]):
        csv_file_name = self.makeCSVFilename("total_passups_per_year")

        with open(csv_file_name, mode='w', newline='') as file:     # overwrite csv file
            writer = csv.writer(file)
            writer.writerow(["Year","Pass-Ups"])                    # insert column headers

        for year in years:
            passups_df = self.filterPassupsDataFrameByYear(year)     # get passup data for the year as a data frame
            total_passups = len(passups_df)                          # get size of data frame (number of rows)
            with open(csv_file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([year,total_passups])
    

    # find total passups for every route per year, then write to CSV file
    def findTotalPassupsByRouteForAllYears(self, years : List[int]):
        csv_file_name = self.makeCSVFilename("total_passups_by_route_per_year")

        with open(csv_file_name, mode='w', newline='') as file:     # overwrite csv file
            writer = csv.writer(file)
            writer.writerow(["Total Pass-Ups By Route Per Year"])   # insert title
            writer.writerow([])                                     # insert new line

        for year in years:
            passups_df = self.filterPassupsDataFrameByYear(year)     # get passup data for the year as a data frame
            value_counts = passups_df['route_number'].value_counts().reset_index() # get frequency for each route
            value_counts.columns = ['Route Number', 'Pass-Ups']
            with open(csv_file_name, mode='a', newline='') as file:  # write to csv file
                writer = csv.writer(file)
                writer.writerow([f"In the Year {year}"])
                value_counts.to_csv(file, mode="a", header=True, index=False)
                writer.writerow([])
    

    # find the total number of passups for each month per year, then write to CSV file

# -------------------------------------------------------------------------------


# # Main -------
# years = ["2023", "2022", "2021", "2020", "2019"]        # the past 5 years
# data_frames_dict = {}                                   # data frames dictionary

# for year in years:
#     total_passups = findTotalPassupsByYear(year)        # get total pass ups per route for a given year
#     data_frames_dict[year] = total_passups              # add data frame result to dictionary

# with open(CSV_FILE_PATH, mode='w', newline='') as file:     # empty contents of csv file
#     pass 

# for key, value in data_frames_dict.items():                     # append title with data frame to csv file
#     with open(CSV_FILE_PATH, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([f"Total Pass-Ups for {key}"])
#         value.to_csv(file, mode="a", header=True, index=False)
#         writer.writerow([])

# # ---------------------------------------------------------------------------------

# # RESULT 2



# # close API client
# client.close()
The source code is broken up into 5 different directories, each serving a different purpose:

1. activity - analyze and visualize the passenger activity data
2. connect_passup_activity - form meaningful connections between the pass-up data set and passenger activity data set
3. passup - perform frequent pattern mining on the pass-up data set
4. passup_anomaly - identify anomalies in the pass-up data set
5. experimental_results - a collection of the final results obtained from running our code (CSV and PNG files used to create graphs and figures for our research paper)

### activity

To analyze and visualize the passenger activity data, navigate to the "activity" directory and run the command `python3 main.py`. This script processes the passenger activity data to perform various analyses and generate visualizations. The output includes:

- Seasonal trends in passenger activity.
- Analysis of passenger activity by day type.
- Trends in passenger activity across different times of the day.
- Identification of the busiest routes and stops based on average boardings.

### passup

To execute frequent pattern mining operations on the pass-up data set and obtain the results, navigate to the "passup" directory. Then, run the command `python3 main.py`. Two text files and 3 CSV files will be generated as output in the same directory:

- fp_growth_result_1.txt: contains the frequent item sets from the pass-up data set with a minimum support set at 10%
- fp_growth_result_2.txt: contains the frequent singleton item sets related to times of the day (24-hour format) from the pass-up data set with a minimum support set at 0.5%
- total_passups_per_year.csv: the total number of pass-ups per year from 2017 to 2022
- total_passups_by_month.csv: the total number of pass-ups per month for every year from 2017 to 2022
- total_passups_by_route.csv: the total number of pass-ups per route for every year from 2017 to 2022

### connect_passup_activity

To run this part, navigate to "connect_passup_activity" directory. Unzip the file "bus_stops_in_order". Then run the command `python3 main.py` (for Mac) or just click the "run" button in the main function. Four CSV files and four folders will be generated as output in the same directory:

- pass_up_apriori_result_pre.csv: contains the frequent 1-itemset from the pass-up dataset (I merged route number, stop_id and route destination as one item) with a minimum support 0.002%. The order is descending. Since there are 3958 pass-ups in 2022 fall and 1/3958>0.002%, it means every pass-up is in the ranking as long as it exists in the pass-up dataset.
- pass_up_apriori_result.csv: It is almost the same as the file above, except that it excludes some stops that cannot be found in the lists of bus stops in order. It also looks prettier since we separate the stop_id and the direction.
- severity_ranking.csv: The ranking of all routes (with directions) according to every route's severity factor in 2022 fall
- boarding_ranking.csv: The ranking of all routes (with directions) according to every route's average boardings per day in 2022 fall
- pass-ups for each stop of different directions: this folder contains the csv files similar to the lists of bus stops in order, except that I add a new column "pass_up_support" for each entry (stop).
- boardings for each stop of different directions: this folder contains the csv files similar to the lists of bus stops in order, except that I add a new column "average_boardings" for each entry (stop).
- combinations for top15 of severity rankings: Since we have known the average_boardings and the pass-up support for each stop, we put the two columns together. So for each entry in the files of the foler, there are three values: pass_up_support, boardings and stop_id. Here we only care about the top 15 routes in the ranking of severity.
- figures for top 15 of severity rankings: according to the files in the folder "combinations for top15 of severity rankings", we plot figures to visualize the pass-up support and avearge boardings of the top 15. There are 15 figures in this folder.

### passup_anomaly

The "passup_anomaly" directory is dedicated to identifying and analyzing anomalies in the pass-up data. This involves preprocessing the data, applying time series analysis, and detecting any unusual patterns or outliers that deviate from normal trends. To run this analysis, navigate to the "passup_anomaly" directory and execute the following commands:

- **Preprocessing the Data**: Start by running `python3 preprocessing.py`. This script prepares the pass-up data for analysis, ensuring it's in the correct format for time series decomposition. It cleans the data, handles missing values, and aggregates the pass-up occurrences to a daily frequency, making it suitable for trend and anomaly detection.
- **Time Series Analysis**: Next, execute `python3 time_series.py`. This script applies time series decomposition to the preprocessed data, breaking it down into trend, seasonal, and residual components. It helps to understand the underlying patterns in the pass-up occurrences over time, separating regular patterns from irregular ones.

The output from this directory includes several key components:

- **time_series**: This folder contains the detailed time series analysis for the listed bus routes. It includes graphs and data sets showing trends, seasonal variations, and residuals, offering a comprehensive view of the pass-up patterns over time.
- **anomaly_detection**: This folder is crucial as it highlights the anomalies detected in the pass-up data. It includes lists and visual representations of dates and times where the pass-up occurrences significantly deviate from the established patterns. This could indicate unusual events or changes in passenger behavior that are not captured by the regular trend and seasonal components.
- **route_passup_plot**: This folder contains aggregated daily pass-up data for the listed routes. It provides a visual representation of the frequency of pass-ups over time, allowing for a quick assessment of which routes and times are most prone to high pass-up rates. This can be especially useful for transit authorities looking to allocate resources more effectively and improve service reliability.

This repository is broken up into 4 different directories, each serving a different purpose:

1. activity -
2. connect_passup_activity -
3. passup - perform frequent pattern mining on the pass-up data set
4. passup_anomaly -

### Pass-Ups

To execute frequent pattern mining operations on the pass-up data set and obtain the results, navigate to the "passup" directory. Then, run the command `python main.py`. Two text files and 3 CSV files will be generated as output in the same directory:

- fp_growth_result_1.txt: contains the frequent item sets from the pass-up data set with a minimum support set at 10%
- fp_growth_result_2.txt: contains the frequent singleton item sets related to times of the day (24-hour format) from the pass-up data set with a minimum support set at 0.5%
- total_passups_per_year.csv: the total number of pass-ups per year from 2017 to 2022
- total_passups_by_month.csv: the total number of pass-ups per month for every year from 2017 to 2022
- total_passups_by_route.csv: the total number of pass-ups per route for every year from 2017 to 2022

### connect_passup_activity

To run this part, navigate to "connect_passup_activity" directory. Then run the command "python3 main.py" (for Mac) or just click the "run" button in the main fucntion. Four CSV files and four folders will be generated as ouput in the same directory:

- pass_up_apriori_result_pre.csv: contains the frequent 1-itemset from the pass-up dataset (I merged route number, stop_id and route destination as one item) with a minimum support 0.002%. The oder is descending. Since there are 3958 pass-ups in 2022 fall and 1/3958>0.002%, it means every pass-up is in the ranking as long as it exists in the pass-up dataset.
- pass_up_apriori_result.csv: It is almost the same with the file above, except that it excludes some stops that cannot be found in the lists of bus stops in order. It also looks prettier since we separate the stop_id and the direction.
- severity_ranking.csv: The ranking of all routes (with directions) according to every route's severity factor in 2022 fall
- boarding_ranking.csv: The ranking of all routes (with directions) according to every route's average boardings per day in 2022 fall
- pass-ups for each stop of different directions: this folder contains the csv files similar to the lists of bus stops in order, except that I add a new column "pass_up_support" for each entry (stop).
- boardings for each stop of different directions: this folder contains the csv files similar to the lists of bus stops in order, except that I add a new column "average_boardings" for each entry (stop).
- combinations for top15 of severity rankings: Since we have known the average_boardings and the pass-up support for each stop, we put the two columns together. So for each entry in the files of the foler, there are three values: pass_up_support, boardings and stop_id. Here we only care about the top 15 routes in the ranking of severity.
- figures for top15 of severity rankings: according to the files in the foler "combinations for top15 of severity rankings", we plot figures to visualize the pass-up support and avearge boardings of the top 15. So we can find the peaks easily.

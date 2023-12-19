This repository is broken up into 3 different directories, each serving a different purpose:

1. activity -
2. connect_passup_activity -
3. passup - perform frequent pattern mining on the pass-up data set
4. passup_anomaly -

### Pass-Ups

To execute frequent pattern mining operations on the pass-up data set and obtain the results, navigate to the "passup" directory. Then, run the command `python3 main.py`. Two text files and 3 CSV files will be generated as output in the same directory:

- fp_growth_result_1.txt: contains the frequent item sets from the pass-up data set with a minimum support set at 10%
- fp_growth_result_2.txt: contains the frequent singleton item sets related to times of the day (24-hour format) from the pass-up data set with a minimum support set at 0.5%
- total_passups_per_year.csv: the total number of pass-ups per year from 2017 to 2022
- total_passups_by_month.csv: the total number of pass-ups in each month for every year from 2017 to 2022
- total_passups_by_route.csv: the total number of pass-ups per route for every year from 2017 to 2022

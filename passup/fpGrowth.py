from aggregator import Aggregator
import dataCollector
import pandas
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth

def fpGrowth():
    # df = dataCollector.getPassupData()     # pass up data frame

    # aggregator = Aggregator(df)
    # df = aggregator.filterPassupsDataFrameByYear(2022)

    # df["time"] = df["time"].dt.round('H')       # round the time to the nearest hour
    # df["time"] = df["time"].astype(str)         # convert datetime values to strings
    # df = df.drop("pass_up_id", axis=1)          # drop id column
    # df = df.drop("pass_up_type", axis=1)        # drop pass-up type column
    # df = df.drop("location", axis=1)            # drop location column
    # df = df.fillna('NA')                        # filler string for NaN values should they appear

    df = pandas.read_csv("../Transit_Pass-ups.csv")

    df = df[df['Pass-Up Type'] == 'Full Bus Pass-Up']  # we care for only full pass up types
    
    # Convert the 'time' column values to a 24-hour format
    df['Time'] = pandas.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')

    # filter the data frame to include rows from a certain year
    target_year = 2022
    df = df[df['Time'].dt.year == target_year]

    # drop unneeded columns
    df = df.drop("Pass-Up ID", axis=1)          # drop id column
    df = df.drop("Pass-Up Type", axis=1)        # drop pass-up type column
    df = df.drop("Location", axis=1)            # drop location column

    df_str = df.astype(str)

    # turn into list of lists for transaction encoder
    transactions = df_str.values.tolist()

    # turn data frame into one-hot encoded format (binary representation of values)
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    one_hot_df = pandas.DataFrame(te_ary, columns=te.columns_)

    # perform FP growth analysis
    frequent_itemsets = fpgrowth(one_hot_df, min_support=0.1, use_colnames=True)

    # print frequent itemsets
    with open('fp_growth_result_1.txt', 'w') as file:
        file.write("These are the frequent item sets pertaining to routes, route names, and route destinations from the pass-up data set.\n")
        file.write("The minimum support is set at 10%.\n\n")
        for index, row in frequent_itemsets.iterrows():
            if 'nan' in row['itemsets']:
                pass
            else:
                file.write(f"Itemset: {set(row['itemsets'])}, Support: {row['support']}\n")

    df = df.drop('Route Number', axis=1)
    df = df.drop('Route Name', axis=1)
    df = df.drop('Route Destination', axis=1)

    # round date time values to nearest minute
    df['Time'] = df['Time'].dt.round('T')

    # keep only the hour and the minute for each datetime value
    df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

    df_str = df.astype(str)

    # turn into list of lists for transaction encoder
    transactions = df_str.values.tolist()

    # turn data frame into one-hot encoded format (binary representation of values)
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    one_hot_df = pandas.DataFrame(te_ary, columns=te.columns_)

    # perform FP growth analysis
    frequent_itemsets = fpgrowth(one_hot_df, min_support=0.005, use_colnames=True)

    with open('fp_growth_result_2.txt', 'w') as file:
        file.write("These are the frequent singletons pertaining to 24-hour time ranges from the pass-up data set.\n")
        file.write("The minimum support is set at 0.5%.\n\n")
        for index, row in frequent_itemsets.iterrows():
            file.write(f"Itemset: {set(row['itemsets'])}, Support: {row['support']}\n")




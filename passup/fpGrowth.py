from aggregator import Aggregator
import dataCollector
import pandas
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth

def fpGrowth():
    df = dataCollector.getPassupData()     # pass up data frame

    # years = ["2022", "2021", "2020", "2019", "2018"]

    # for year in years:
    #     pass

    aggregator = Aggregator(df)
    df_2022 = aggregator.filterPassupsDataFrameByYear(2022)
    df_2022["time"] = df_2022["time"].dt.round('H')

    # turn data frame into one-hot encoded format (binary representation of values)
    te = TransactionEncoder()
    te_ary = te.fit(df_2022).transform(df_2022)
    one_hot_df = pandas.DataFrame(te_ary, columns=te.columns_)

    # perform FP growth analysis
    frequent_itemsets = fpgrowth(one_hot_df, min_support=0.03, use_colnames=True)

    for index, row in frequent_itemsets.iterrows():
        print(f"Itemset: {set(row['itemsets'])}, Support: {row['support']}")

fpGrowth()




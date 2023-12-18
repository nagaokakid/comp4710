# the first part is to get the apriori result, which is similar to the implement_apriori.py
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from mlxtend.frequent_patterns import apriori

#convert the csv file to a dataset and then get the aptiori result
pass_up_df = pd.read_csv("2022_fall_pass-ups.csv")
pass_up_df["stop_id"] = pass_up_df["stop_id"].apply(str)
pass_up_df['stop_id'] = pass_up_df["Route Number"]+" "+pass_up_df["stop_id"]
print(len(pass_up_df['stop_id']))

for x in range(len(pass_up_df['stop_id'])):
    pass_up_df["stop_id"][x] = pass_up_df["stop_id"][x].split(',')         
                                                                                   
pass_up_sel_row = pass_up_df["stop_id"]
pass_up_sel_li = pass_up_sel_row.tolist()      
te = TransactionEncoder()
te_transform= te.fit(pass_up_sel_li).transform(pass_up_sel_li)
df = pd.DataFrame(te_transform, columns=te.columns_)
df = apriori(df, min_support=0.00002, use_colnames=True)      # min_support=0 means we will count every stop where paa-up happens
df['itemsets'] = df['itemsets'].apply(set)
for x in range(len(df['itemsets'])):
    df['itemsets'][x] = list(df['itemsets'][x])[0]
df = df.sort_values(by='support', ascending=False)
result = df.to_csv("pass_up_apriori_result.csv")



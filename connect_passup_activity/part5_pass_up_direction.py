# Similar to part4, in this part, I will get the pass-ups of each stop to a specific direction of a route and 
# output csv files containing the column "pass_up_support" for each direction

import pandas as pd
import os

os.makedirs("pass-ups for each stop of different directions",exist_ok=True)
pass_up_rank_df = pd.read_csv("pass_up_apriori_result.csv")
direct_names = []
df_li = []

not_found = 0       #this is used to count how many stops in the pass-up data cannot be found in the bus stops dataset

for index in range(len(pass_up_rank_df)):
    direction = pass_up_rank_df["direction"][index]
    direct_li = direction.split(' ', 1)
    route_id = direct_li[0]
    stop_id = str(pass_up_rank_df["stop_ID"][index])
    if direction not in direct_names:
        direct_names.append(direction)
        new_df = pd.DataFrame({}, columns=['stop_id', 'pass_up_support'])
        target_file = open("bus_stops_in_order/"+route_id+"/"+direct_li[1]+".txt","r")
        each_line = target_file.readline().strip()
        count = 0
        while(each_line!=''):
            stop_info_li2 = each_line.split()
            if(stop_id == stop_info_li2[0]):
                support = pass_up_rank_df["support"][index]
            else:
                support = 0
            new_df.loc[count] = {"stop_id":stop_info_li2[0], "pass_up_support":support}
            each_line = target_file.readline().strip()
            count = count + 1
        target_file.close()
        df_li.append(new_df)
        
    else:
        target_index = direct_names.index(direction)
        df_li[target_index].loc[df_li[target_index].stop_id ==stop_id, "pass_up_support"] = pass_up_rank_df["support"][index]
    
for x in range(len(df_li)):
    df_li[x].to_csv("pass-ups for each stop of different directions/"+direct_names[x]+".csv")           
print("There are "+str(not_found)+ " stops not found")






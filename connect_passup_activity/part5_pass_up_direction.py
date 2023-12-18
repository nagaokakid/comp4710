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
    stop_route_str = pass_up_rank_df["itemsets"][index]
    str_li = stop_route_str.strip().split()
    route_id = str_li[0]
    
    found = False   #this is to indicate whether we find the stop in the "bus_stops_in_order"
    
    directions_file = open("bus_stops_in_order/"+route_id+"/"+route_id+" directions.txt","r")
    direct_line = directions_file.readline().strip()
    while(direct_line!="" and found==False):
        route_direct_id = route_id + " " + direct_line
        stops_file = open("bus_stops_in_order/"+route_id+"/"+direct_line+".txt","r")
        stop_line = stops_file.readline().strip()
        while(stop_line!='' and found==False):
            stop_info_li = stop_line.split()
            stop_id = stop_info_li[0]
            if(str_li[1] == stop_id):
                found = True
            stop_line = stops_file.readline().strip()
        stops_file.close()
        if(found==False):
            direct_line = directions_file.readline().strip()
            
    if(found == False):
        not_found = not_found + 1
    directions_file.close()    
    if(found != False):
        if route_direct_id not in direct_names:
            direct_names.append(route_direct_id)
            new_df = pd.DataFrame({}, columns=['stop_id', 'pass_up_support'])
            target_file = open("bus_stops_in_order/"+route_id+"/"+direct_line+".txt","r")
            each_line = target_file.readline().strip()
            count = 0
            while(each_line!=''):
                stop_info_li2 = each_line.split()
                str_stop_id = stop_info_li2[0]
                if(str_li[1] == stop_info_li2[0]):
                    support = pass_up_rank_df["support"][index]
                else:
                    support = 0
                new_df.loc[count] = {"stop_id":str_stop_id, "pass_up_support":support}
                each_line = target_file.readline().strip()
                count = count + 1
            target_file.close()
            df_li.append(new_df)
            
        else:
            target_index = direct_names.index(route_direct_id)
            df_li[target_index].loc[df_li[target_index].stop_id ==str_li[1], "pass_up_support"] = pass_up_rank_df["support"][index]
    
for x in range(len(df_li)):
    df_li[x].to_csv("pass-ups for each stop of different directions/"+direct_names[x]+".csv")           
print("There are "+str(not_found)+ " stops not found")






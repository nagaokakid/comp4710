# here, I will get the boardings of each stop to a specific direction of a route and 
# output csv files containing the column "average_boardings" for each direction
import pandas as pd
import os

os.makedirs("boardings for each stop of different directions",exist_ok=True)
boarding_rank_df = pd.read_csv("boarding_ranking.csv")
direct_names = []
df_li = []

for index in range(len(boarding_rank_df)):
    stop_route_str = boarding_rank_df["stop_route_id"][index]
    str_li = stop_route_str.strip().split()
    route_id = str_li[1]
    
    found = False   #this is to indicate whether we find the stop in the "bus_stops_in_order"
    try:
        directions_file = open("bus_stops_in_order/"+route_id+"/"+route_id+" directions.txt","r")
        direct_line = directions_file.readline().strip()
        while(direct_line!="" and found==False):
            route_direct_id = route_id + " " + direct_line
            stops_file = open("bus_stops_in_order/"+route_id+"/"+direct_line+".txt","r")
            stop_line = stops_file.readline().strip()
            while(stop_line!='' and found==False):
                stop_info_li = stop_line.split()
                stop_id = stop_info_li[0]
                if(str_li[0] == stop_id):
                    found = True
                stop_line = stops_file.readline().strip()
            stops_file.close()
            if(found==False):
                direct_line = directions_file.readline().strip()
        directions_file.close()    
        if(found != False):
            if route_direct_id not in direct_names:
                direct_names.append(route_direct_id)
                new_df = pd.DataFrame({}, columns=['stop_id', 'average_boardings'])
                target_file = open("bus_stops_in_order/"+route_id+"/"+direct_line+".txt","r")
                each_line = target_file.readline().strip()
                count = 0
                while(each_line!=''):
                    stop_info_li2 = each_line.split()
                    str_stop_id = stop_info_li2[0]
                    if(str_li[0] == stop_info_li2[0]):
                        average_boarding = boarding_rank_df["average_boardings"][index]
                    else:
                        average_boarding = 0
                    new_df.loc[count] = {"stop_id":str_stop_id, "average_boardings":average_boarding}
                    each_line = target_file.readline().strip()
                    count = count + 1
                target_file.close()
                df_li.append(new_df)
                
            else:
                target_index = direct_names.index(route_direct_id)
                df_li[target_index].loc[df_li[target_index].stop_id ==str_li[0], "average_boardings"] = boarding_rank_df["average_boardings"][index]
    except:
            print("The "+route_id+" does not exist anymore")
    
for x in range(len(df_li)):
    df_li[x].to_csv("boardings for each stop of different directions/"+direct_names[x]+".csv")           
test_df = pd.read_csv("boardings for each stop of different directions/11 Polo Park.csv")
# the second part is to get the severity ranking for 2022 fall. The severity is calculated by summing up pass-ups and 
# then dividing the sum by the number of stops in one direction of a route. In other words, the severity factor is the
# average of pass-ups in each stop of a route in one direction
import pandas as pd
TOTAL_PASS_UPS = 3958      #there are 16425 pass-ups in total from 7/1/2022 to 11/17/2023
severity_dt = {}
severity_df = pd.DataFrame(severity_dt, columns=['route_direction', 'severity_factor'])

apriori_result = open("pass_up_apriori_result.csv", "r")
pass_up_info = apriori_result.readline()    #this should be the attribute names
pass_up_info = apriori_result.readline().strip()    #this is the first line
severity_df_size = 0
while(pass_up_info != ''):
    found = False       #this is to indiacte whether we find the stop in the bus_stops_in_order
    info_li = pass_up_info.split(',')       
    support = float(info_li[1])                    # get the support for this stop (with the route)
    route_stop = info_li[2].split()         # get the route and stop like "BLUE 61216"
    route_id = route_stop[0]                # here, the route id is the [0] while the stop id is the [1]
    
    route_directs = open("bus_stops_in_order/"+route_id+"/"+route_id+" directions.txt", "r")
    direct_line = route_directs.readline().strip()      #direct_line is the name of each direction
    while(direct_line!='' and found==False):            #when we find this stop id, stop the loop
        stops_file = open("bus_stops_in_order/"+route_id+"/"+direct_line+".txt", "r")
            
        stops_file2 = open("bus_stops_in_order/"+route_id+"/"+direct_line+".txt", "r")
        count = 1
        temp_line = stops_file2.readline().strip()
        while(temp_line != ''):
            count = count + 1
            temp_line = stops_file2.readline().strip()
        stops_file2.close()
        direct_stop_num = count                # this is the number of bus stops in this direction
            
        stop_line = stops_file.readline().strip()       # stop_line is the line containing the id of the stop and the name
        while(stop_line!='' and found==False):
            stop_li = stop_line.split()
            stop_id = stop_li[0]
            if(route_stop[1]==stop_id):
                found = True
                direction_name = route_id+" "+direct_line
                if direction_name not in severity_df["route_direction"].values:
                    new_row = {"route_direction":route_id+" "+direct_line, "severity_factor":0}
                    severity_df.loc[severity_df_size] = new_row     #append the new row to the severity_df
                    severity_df_size = severity_df_size + 1
                    severity_df.loc[severity_df.route_direction == direction_name, 'severity_factor'] = round(support*TOTAL_PASS_UPS/direct_stop_num, 4)
                else:
                    severity_df.loc[severity_df.route_direction == direction_name, 'severity_factor'] = round(severity_df.loc[severity_df.route_direction == direction_name, 'severity_factor'] + support*TOTAL_PASS_UPS/direct_stop_num, 4)
            stop_line = stops_file.readline().strip()
        direct_line = route_directs.readline().strip() 
    pass_up_info = apriori_result.readline().strip()
    
severity_df = severity_df.sort_values(by='severity_factor', ascending=False)
severity_df = severity_df.reset_index()
result = severity_df.to_csv("severity_ranking.csv")
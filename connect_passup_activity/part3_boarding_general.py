# First, I will process the passenger activity to get a dataframe containing route number, stop id and boardings.
# It means I need to create a datarame, go through the passenger activity data and store the processed data in
# the dataframe. In this process, when I find the same stop with the same route, the same day type (Weekday) and the same
# time period, I should multiply a weight factor and add them together. 
# For weekdays, the weight factors are: AM Peak-0.211, Mid-Day-0.342, PM Peak-0.158, Evening-0.211, Night-0.079
# For Sunday or Saturday, the weight factors are: Morning-0.316, Afternoon-0.421, Evening-0.184, Night-0.079

# after we get the dataframe, find the direction of each route-stopID by matching the dataframe with the data in the folder
# "bus_stops_in_order". For each direction of each route, there should be a list showing the average boarding of each stop.
# It's like the list in "bus_stops_in_order", with one more colum: average boarding
import pandas as pd
pasg_data_processed = {}
pasg_data_df = pd.DataFrame(pasg_data_processed, columns=['stop_route_id', 'average_boardings'])
pasg_data_size = 0

origin_pasg_df = pd.read_csv("passenger_activity_2022_fall.csv")   #this is the original dataframe

for index in range(len(origin_pasg_df)):
    origin_stop_number = origin_pasg_df["Stop Number"][index]
    origin_route_number = origin_pasg_df["Route Number"][index]
    origin_boarding = origin_pasg_df["Average Boardings"][index]
    
    stop_route_num = str(origin_stop_number) + " " + origin_route_number
    
    if (stop_route_num not in pasg_data_df["stop_route_id"].values):
        new_row = {"stop_route_id": stop_route_num, "average_boardings": float(0)}
        pasg_data_df.loc[pasg_data_size] = new_row
        
        if(origin_pasg_df["Day Type"][index] == "Weekday"):
                
            if(origin_pasg_df["Time Period"][index] == "Morning"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(5/7*0.211*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Mid-Day"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(5/7*0.342*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "PM Peak"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(5/7*0.158*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Evening"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(5/7*0.211*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Night"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(5/7*0.079*origin_boarding, 4)
        else:
            if(origin_pasg_df["Time Period"][index] == "Morning"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(2/7*0.316*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Afternoon"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(2/7*0.421*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Evening"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(2/7*0.184*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Night"):
                pasg_data_df["average_boardings"].values[pasg_data_size] = round(2/7*0.079*origin_boarding, 4)
        pasg_data_size = pasg_data_size + 1
    else:
        boarding_pre_modify_li = pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings']
        boarding_pre_modify = round(float(boarding_pre_modify_li.iloc[0]),4)
        if(origin_pasg_df["Day Type"][index] == "Weekday"):
            if(origin_pasg_df["Time Period"][index] == "AM Peak"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(5/7*0.211*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Mid-Day"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(5/7*0.342*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "PM Peak"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(5/7*0.158*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Evening"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(5/7*0.211*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Night"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(5/7*0.079*origin_boarding, 4)
        else:
            if(origin_pasg_df["Time Period"][index] == "Morning"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(2/7*0.316*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Afternoon"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(2/7*0.421*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Evening"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(2/7*0.184*origin_boarding, 4)
            if(origin_pasg_df["Time Period"][index] == "Night"):
                pasg_data_df.loc[(pasg_data_df.stop_route_id == stop_route_num), 'average_boardings'] = boarding_pre_modify + round(2/7*0.079*origin_boarding, 4)
pasg_data_df = pasg_data_df.sort_values(by='average_boardings', ascending=False)
result = pasg_data_df.to_csv("boarding_ranking.csv")

# After getting the result, I think probably the number of boarding is not divided by the number of buses
# It means this is the total number of the boarding during the time period (eg, 5am to 9am)
# But indeed the ranking about boarding is not that important because the capacity of buses may be different.
# What matters most is the ranking of boardings of differnt stops in one direction of a specific route

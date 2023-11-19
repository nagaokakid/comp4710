import requests
import os
# the function below is to fetch data from api.winnipegtransit.com to get the location for each stop.
# the output is a list of stops that a route passes with the latitude and longitude of each stop
def get_location():
    route = open("all-routes.csv","r")
    route_id = route.readline().strip()
    os.makedirs("stops_for_each_route", exist_ok=True)
    
    while(route_id):
        website = 'https://api.winnipegtransit.com/v3/stops.json?api-key=OFULnSbi5zm7ZRRKStKg&route='+route_id
        
        new_file = open("stops_for_each_route/"+route_id+".csv", "w")
        new_file.write("stop_id,latitude,longitude\n")
        
        response = requests.get(website)
        count = 0
        result = response.json()['stops'][count]
        while(count<len(response.json()['stops'])):
            stop_id = response.json()['stops'][count]['number']
            latitude = response.json()['stops'][count]['centre']['geographic']['latitude']
            longitude = response.json()['stops'][count]['centre']['geographic']['longitude']
            
            new_file.write(str(stop_id)+","+str(latitude)+","+str(longitude)+"\n")
            
            count = count + 1
            if(count<len(response.json()['stops'])):
                result = response.json()['stops'][count]
        
        new_file.close()
        route_id = route.readline().strip()
get_location()

# the next part is to do the mapping. It means linking each pass up to one (or more) bus stop according to the latitude and longitude
# Here the basic idea is to find the cloest stop according to the difference betweeen the pass-up location and the stop location
# of course we can also set a threshold to get more bus stops that are close "enough" and then filter by the direction. But for now 
# we do not have the list of bus stops in order. So maybe finding the cloest stop is the best we can do for now.
def passup_mapping_stops():
    pass_up = open("Transit_Pass-ups.csv","r")
    attribute_name = pass_up.readline().strip()     #this line is for attribute names (not splited yet)
    attribute_list = attribute_name.split(",")
    pass_up_with_id = open("pass_up_with_stopID.csv", "w")
    pass_up_with_id.write(attribute_list[0]+","+attribute_list[2]+","+attribute_list[3]+","+attribute_list[5]+",stop_id\n")
    line = pass_up.readline()
    while(line):
        line = line.strip()
        str_list = line.split(",")
        
        if((str_list[6].strip()!='') & (str_list[5].strip()!='') & (str_list[3].strip()!='')):
            str_list[6] = str_list[6][7:]   #remove the annoying "POINT (", 7 characters
            str_list[6] = str_list[6][:-1]     #remove the ")"
            
            passup_loc_list = str_list[6].split(" ")
            passup_longitude = float(passup_loc_list[0])  #convert string to float (longitude)
            passup_latitude = float(passup_loc_list[1])  #convert string to float (latitude)
            
            route_num = str_list[3]
            
            try:
                stop_list = open("stops_for_each_route/"+route_num+".csv", "r")
                stop_info = stop_list.readline()    #this line is for attribute names
                stop_info = stop_list.readline().strip()
                stop_info_list = stop_info.split(",")
                
                stop_latitude = float(stop_info_list[1])     #convert string to float (latitude)
                stop_longitude = float(stop_info_list[2])    #convert string to float (longitude)
                
                min_error = abs(stop_longitude-passup_longitude) + abs(stop_latitude-passup_latitude)   #make sure the difference is the smallest
                min_error_id = stop_info_list[0]
                
                stop_info = stop_list.readline()
                while(stop_info):
                    stop_info = stop_info.strip()
                    stop_info_list = stop_info.split(",")
                    stop_latitude = float(stop_info_list[1])
                    stop_longitude = float(stop_info_list[2]) 
                    if(abs(stop_longitude-passup_longitude) + abs(stop_latitude-passup_latitude)<min_error):
                        min_error = abs(stop_longitude-passup_longitude) + abs(stop_latitude-passup_latitude)
                        min_error_id = stop_info_list[0]
                    stop_info = stop_list.readline()
                pass_up_with_id.write(str_list[0]+","+str_list[2]+","+str_list[3]+","+str_list[5]+","+min_error_id+"\n")
            except:
                print("the route csv file is not found")
        line = pass_up.readline()
    pass_up_with_id.close()
    pass_up.close()
passup_mapping_stops()

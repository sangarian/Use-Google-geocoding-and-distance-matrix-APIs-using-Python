
# Now let's calculate the travel time & distance between the origin (school) & students home address
import pandas as pd
import googlemaps
import requests
import logging
import time

log = logging.getLogger("root")
log.setLevel(logging.DEBUG)
# create console handler
cons = logging.StreamHandler()
cons.setLevel(logging.DEBUG)
log.addHandler(cons)



api_key = 'your api key'
BACKOFF_TIME = 30

input_filename = "your csv file with geocoded addresses"
address_column_name = "address_edited"
RETURN_FULL_RESULTS = False

data = pd.read_csv(input_filename, encoding='utf8')
if address_column_name not in data.columns:
	raise ValueError("Missing Address column in input data")


data = pd.read_csv(input_filename, encoding='utf8')
gmaps=googlemaps.Client(api_key)

schools=data["school"].tolist()
destinations = (data["formatted_address"]+' ,Pakistan').tolist()
actual_distance=[]
actual_duration=[]
for destination in destinations:
    if destination is None:
        result= "NA"
        resulta= "NA"
        actual_distance.append(resulta)
        actual_duration.append(result)
        continue
    for school in schools:
        if school == 'SMB':
            origin= "SMB Fatima Jinnah Girls School Karachi Pakistan"
        #if you have a list of many schools you can add them to a list and loop through them. I have two schools in my data so I use if/else statement
        else:
            origin= "Khatoon-e-Pakistan Government Degree College For Women Karachi Pakistan"
    try:
        lala = gmaps.distance_matrix(origin, destination, mode='driving')
        status= lala["rows"][0]['elements'][0]['status']
        if status== 'OK':
            result=lala["rows"][0]['elements'][0]['duration']['value']
            result=result/3600
            resulta=lala["rows"][0]['elements'][0]['distance']['value']
            resulta=resulta/1000
            actual_duration.append(result)
            actual_distance.append(resulta)
            print('done')
        else:
            result= "NA"
            resulta= "NA"
            actual_distance.append(resulta)
            actual_duration.append(result)
    except:
        result= "NA"
        resulta= "NA"
        actual_distance.append(resulta)
        actual_duration.append(result)
data['duration']= actual_duration
data['distance']= actual_distance
df=pd.DataFrame(data)
df.to_csv('add_lst_kps.csv', index=False, encoding='utf-8')

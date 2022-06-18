#Import the required packages
import googlemaps
import pandas as pd
import requests
import logging
import time

#create a logger and add it to a console
log = logging.getLogger("chiran")
log.setLevel(logging.DEBUG)
cons = logging.StreamHandler()
cons.setLevel(logging.DEBUG)
log.addHandler(cons)

api_key = 'Insert the api key from your Google Developers account' 
backoff_time= 30

#name your output as a csv file
output_filename = 'geocoded.csv'
#set your input csv file with students information and addresses. 
input_filename= 'sampledata_1.csv'
#specify the column in the csv file that contains students' addresses
address_column= "address"
# if you have a large dataset returning full JSON results would be cumbersome so we set it to FALSE
RETURN_FULL_RESULTS = False

# Read the data using pandas
data = pd.read_csv(input_filename, encoding='utf8')
if address_column not in data.columns:
	raise ValueError("missing address column")
  
#making a big list of all the addresses to be geocoded
addresses = data[address_column_name].tolist()

# If your addresses has country information, add it so that Google knows where to look specifically. Increases the accuracy of the geocoded addresses
addresses = (data[address_column_name] + ',Pakistan').tolist()


def get_google_results(address, api_key=None, return_full_response=False):
  geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
    if api_key is not None:
        geocode_url = geocode_url + "&key={}".format(api_key)
     
    results = requests.get(geocode_url)
    results = results.json()
    
    
    if len(results['results']) == 0:
        output = {
            "address": address,
            "formatted_address" : None,
            "latitude": None,
            "longitude": None,
            "accuracy": None,
            "google_place_id": None,
            "type": None,
            "postcode": None
        }
    else:
        answer = results['results'][0]
        output = {
            "address": address,
            "formatted_address" : answer.get('formatted_address'),
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
            "accuracy": answer.get('geometry').get('location_type'),
            "google_place_id": answer.get("place_id"),
            "type": ",".join(answer.get('types')),
            "postcode": ",".join([x['long_name'] for x in answer.get('address_components')
                                  if 'postal_code' in x.get('types')])
        }
    
    #append some additonal information    
    output['input_string'] = address
    output['number_of_results'] = len(results['results'])
    output['status'] = results.get('status')
    if return_full_response is True:
        output['response'] = results

    return output

#lets test the code an api keys to confirm we all set to geocode, use your favourite city name to test. I use London. 

test_result = get_google_results("London, England", api_key, RETURN_FULL_RESULTS)
if (test_result['status'] != 'OK') or (test_result['formatted_address'] != 'London, UK'):
    log.warning("google geocoder error detected")
    raise ConnectionError('Error, please check your internent')

#if you are all set, lets dig in. First lets create an empty list to store the geocoded addresses as we harvest them using google api
results = []

#let create a loop, so that we sent request to google servers untill all addresses are geocoded
for address in addresses:
    
    geocoded = False
    while geocoded is not True:
        try:
            geocode_result = get_google_results(address, api_key, return_full_response=RETURN_FULL_RESULTS)
        except Exception as eh:
            log.exception(eh)
            log.error("error with {}".format(address))
            log.error("Skipping!")
            geocoded = True

        # If we're over the API limit, backoff for a while and try again later.
        if geocode_result['status'] == 'OVER_QUERY_LIMIT':
            log.info("Query limit reached! Lets rest for a while")
            time.sleep(backoff_time * 60) # sleep for 30 minutes
            geocoded = False
        else:
            # If we're ok with API use, save the results
            # Note that the results might be empty / non-ok - log this
            if geocode_result['status'] != 'OK':
                log.warning("Error geocoding {}: {}".format(address, geocode_result['status']))
            log.debug("Geocoded: {}: {}".format(address, geocode_result['status']))
            results.append(geocode_result)
            geocoded = True

    # check status every 100 addresses
    if len(results) % 100 == 0:
    	log.info("Completed {} of {} address".format(len(results), len(addresses)))

    # Every 500 addresses, save progress to file(in case of a failure so you have something!)
    if len(results) % 500 == 0:
        df=pd.DataFrame(results)
        df.to_csv('sampledata_1_backup.csv', index=False, encoding='utf-8')

# All done
log.info("Done geocoding")
# Write the full results to csv using the pandas library.
df=pd.DataFrame(results)
df.to_csv('geocoded.csv', index=False, encoding='utf-8')









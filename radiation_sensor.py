"""
    Dronesmith API
    Mock Radiation Sensors

    This script requires the Python packages requests and geopy.
    pip install requests
    pip install geopy

    This script iterates through a JSON file of user account info and for
    each user it gets the current position of the user's drone, calculates
    radiation intensity using this position data, and then posts this
    intensity value to the drone. This process loops continuously until
    script is terminated.

"""

import json
import requests
import string
import random
import time
import math
from geopy.distance import vincenty

RAD_SOURCE = (47.397703, 8.550597)

def calculateRadIntensity(lat, lon):
    # Use inverse square law to calculate radiation intensity
    # sensed by drone.

    drone_pos = (lat, lon)
    d1_intensity = 60000.546 #milliroentgen/hour
    d1 = 1.0 #meters
    d2 = vincenty(RAD_SOURCE, drone_pos).meters
    d2_intensity = d1_intensity * math.pow(d1,2) / math.pow(d2,2)

    print "Distance: %f" % (d2)
    print "Intensity: %f" % (d2_intensity)
    return d2_intensity

# Open file containing user account info
with open('user-account.json') as json_data:
    jsonInputText = json.load(json_data)
    json_data.close()

# Main loop
while True:

    # Iterate through users
    for i in jsonInputText:
        print "User: " + i['email']

        headers = {
            'user-email':       i['email'],
            'user-key':         i['api_key'],
            'Content-Type':     'application/json'
        }

        # Get position
        try:
            response = requests.get('http://api.dronesmith.io/api/drone/' + i['drone_name'] + '/position', headers=headers, timeout=1)
        except requests.exceptions.RequestException as e:
            print e
            continue

        obj = json.loads(response.text)

        if response.status_code == 200:

            print "Position recieved"

            #Calculate radiation intensity
            intensity = calculateRadIntensity(obj['Latitude'], obj['Longitude'])

            # Update radiation sensor intesity value
            try:
                response = requests.post('http://api.dronesmith.io/api/drone/' + i['drone_name'] + '/sensor/radiation_sensor', json={
                    "intensity": intensity
                    }, headers=headers, timeout=1)

            except requests.exceptions.RequestException as e:
                print e
                continue

            obj = json.loads(response.text)

            if response.status_code == 200 and obj["status"] == "OK":
                print "Sensor data posted"
            else:
                print "Sensor data not posted"
                continue
        else:
            print "Position not recieved"


        time.sleep(0.4)

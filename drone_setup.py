import requests
import json

# Open user-account.json and create a json object containing
# user credential fields.
with open('user-account.json', "r") as jsonFile:
   jsonUser = json.load(jsonFile)
   jsonFile.close()

# Assign user credentials to variables
USER_EMAIL = jsonUser[0]['email']
USER_API_KEY = jsonUser[0]['api_key']
DRONE_NAME = ""

# Create headers object for API requests
headers = {
   'user-email':       USER_EMAIL,
   'user-key':         USER_API_KEY,
   'Content-Type':     'application/json'
}

# This request will create a virtual drone on your account with a random
# name. The server should respond with a JSON formatted Drone
# object that contains the name of the new drone.
print "\nCreate new virtual drone...\n"

response = requests.post('http://api.dronesmith.io/api/drone', headers=headers)
obj = json.loads(response.text)
print json.dumps(obj, indent=2, sort_keys=True)

# Update DRONE_NAME
DRONE_NAME = obj['name']

# Update drone_name field in jsonUser object
jsonUser[0]["drone_name"] = DRONE_NAME

# Write jsonUser object to user-account.json
with open('user-account.json', "w") as jsonFile:
   jsonFile.write(json.dumps(jsonUser,indent=2, sort_keys=True))
   jsonFile.close()

# Add a sensor named radiation_sensor to drone and initialize its intensity field
print "\nAdd radiation sensor to drone...\n"
response = requests.post('http://api.dronesmith.io/api/drone/' + DRONE_NAME \
 + '/sensor/radiation_sensor', json={
    "intensity": 0
 }, headers=headers)
jsonText = json.loads(response.text)
print json.dumps(jsonText, indent=2, sort_keys=True)

# Get drone object to make sure radiation sensor was properly
# added. There should be a sensors field containing radiation_sensor object.
print "\nGet Drone object..\n"
response = requests.get('http://api.dronesmith.io/api/drone/' \
+ DRONE_NAME, headers=headers)
jsonText = json.loads(response.text)
print json.dumps(jsonText, indent=2, sort_keys=True)

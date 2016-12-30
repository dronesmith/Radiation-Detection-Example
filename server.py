"""
Copyright (c) 2016, Dronesmith Technologies Inc
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Dronesmith Technologies Inc  nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL DRONESMITH TECHNOLOGIES INC BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import SocketServer
import SimpleHTTPServer
import requests
import threading
import time
import math
import json
# Retrieve fields from user-account.json
with open('user-account.json') as json_data:
    jsonUser = json.load(json_data)
    json_data.close()

USER_EMAIL = jsonUser[0]['email']
USER_API_KEY = jsonUser[0]['api_key']
DRONE_NAME = jsonUser[0]['drone_name']

# Create headers object for API requests
headers = {
    'user-email':       USER_EMAIL,
    'user-key':         USER_API_KEY,
    'Content-Type':     'application/json'
}

# Define server port
PORT = 8080

# Waypoints
HOME = {'lat':47.397452, 'lon': 8.547774}
A = {'lat':47.399112, 'lon':8.549034}
B = {'lat':47.398670, 'lon':8.551243}
C = {'lat':47.396707, 'lon':8.550953}

# Previous values
last_position = (47.397452, 8.547774, 0)
server_last_pos = (47.397452, 8.547774, 0)
last_sensor = 0
point = 0

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def getPosition(self):
        global server_last_pos
        try:
            response = requests.get('http://api.dronesmith.io/api/drone/'\
            + DRONE_NAME + '/position', headers=headers, timeout=5)
        except requests.exceptions.RequestException as e:
            print e
            print "Position exception"
            # if request fails return last position
            return (server_last_pos[0], server_last_pos[1], server_last_pos[2])

        obj = json.loads(response.text)
        server_last_pos = obj['Latitude'], obj['Longitude'], obj['Altitude']

        # print json.dumps(obj, indent=2, sort_keys=True)
        return (obj['Latitude'], obj['Longitude'], obj['Altitude'])

    def getRadIntensity(self):
        global last_sensor
        try:
            response = requests.get('http://api.dronesmith.io/api/drone/' \
            + DRONE_NAME + '/sensor/radiation_sensor', headers=headers)
        except requests.exceptions.RequestException as e:
            print e
            print "Sensor exception"
            return (last_sensor)

        obj = json.loads(response.text)
        last_sensor = obj['intensity']
        return obj['intensity']

    def do_GET(self):
        global point
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type','text/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            lat, lon, alt = self.getPosition()
            time.sleep(0.5)
            intensity = self.getRadIntensity()
            point += 1
            r = {
             'lat': lat,
             'lon': lon,
             'altitude': alt,
             'intensity': intensity,
             'point': point
            }

            self.wfile.write(json.dumps(r))
            time.sleep(1)
            return
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


# Drone commands
def start(latitude, longitude):

    #Altitude is relative
    try:
        response = requests.post('http://api.dronesmith.io/api/drone/'\
        + DRONE_NAME + '/start', json={
                "lat": latitude,
	            "lon": longitude
            }, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print e
        print "Start exception"
        return False
    obj = json.loads(response.text)
    if response.status_code == 200 :
        print "Start command worked"
        return True
    else:
        return False
def stop():

    i = 0
    while True:
        try:
            response = requests.post('http://api.dronesmith.io/api/drone/'\
            + DRONE_NAME + '/stop', headers=headers, timeout=5)
            obj = json.loads(response.text)
            if response.status_code == 200 :
                print "Stop command worked"
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print e
            print "Stop exception. Retrying command..."
            if i<3:
                i += 1
                continue
            else:
                return False
def get_position():
    global last_position
    try:
        response = requests.get('http://api.dronesmith.io/api/drone/'\
        + DRONE_NAME + '/position', headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        return (last_position[0], last_position[1], last_position[2])
        print "Position exception"
        print e

    obj = json.loads(response.text)
    last_position = obj['Latitude'], obj['Longitude'], obj['Altitude']

    print json.dumps(obj, indent=2, sort_keys=True)
    return (obj['Latitude'], obj['Longitude'], obj['Altitude'])

def takeoff(altitude):
    try:
        response = requests.post('http://api.dronesmith.io/api/drone/'\
        + DRONE_NAME + '/takeoff', json={
                "altitude": altitude
            }, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print "Takeoff exception"
        print e
        return False
    obj = json.loads(response.text)
    if response.status_code == 200 and obj["Command"] == 22 \
    and obj["Status"] == "Command accepted.":
        print "Takeoff command worked"
        return True
    else:
        return False
def goto(latitude, longitude, altitude):
    #Altitude is relative
    try:
        response = requests.post('http://api.dronesmith.io/api/drone/'\
        + DRONE_NAME + '/goto', json={
                "lat": latitude,
	            "lon": longitude,
                "altitude": altitude
            }, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print e
        print "Goto exception"
        return False
    obj = json.loads(response.text)
    if response.status_code == 200 and obj["Command"] == 192 \
    and obj["Status"] == "Command accepted.":
        print "Goto command worked"
        return True
    else:
        return False

def land():
    try:
        response = requests.post('http://api.dronesmith.io/api/drone/'\
        + DRONE_NAME + '/land', headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print "Land exception"
        print e
        return False
    obj = json.loads(response.text)
    if response.status_code == 200 and obj["Command"] == 21 \
    and obj["Status"] == "Command accepted.":
        print "Land command worked"
        return True
    else:
        return False

def abort():
     i = 0
     while True:
        try:
            response = requests.post('http://api.dronesmith.io/api/drone/'\
            + DRONE_NAME + '/mode', json={
                    "mode": "RTL"
                }, headers=headers, timeout=5)

            obj = json.loads(response.text)
            if response.status_code == 200 and obj["Command"] == 176 \
            and obj["Status"] == "Command accepted.":
                print "Abort command worked"
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print e
            print "Abort exception. Retrying command..."
            if i<3:
                i += 1
                continue
            else:
                return False
def constrainSync(target, typeVal, threshold, timeout):
    attempts = timeout
    while True:
        lat, lon, alt = get_position()
        attempts -= 1
        if typeVal == 'alt':
            #print abs(pos.altitude - target)
            print alt
            if abs(alt - target) < threshold:
                print "Hovering at proper altitude"
                return True
        if typeVal == 'land':
            #print abs(pos.altitude - target)
            print alt
            if abs(alt - 0) < threshold:
                print "Drone has landed"
                return True
        elif typeVal == 'loc':
            targetLat = target[0]
            targetLon = target[1]
            if abs(lat - targetLat) < threshold \
            and abs(lon - targetLon) < threshold:
                print "Arrived at waypoint"
                return True
        if attempts <= 0:
            return False
        time.sleep(1)



# MAIN
# Start drone, takeoff, follow a path, land, and stop drone.
def droneWorker():
    # Wait for HTTP server to start displaying data
    time.sleep(3)

    #Start drone
    if not start(HOME['lat'], HOME['lon']):
        "Something went wrong"
        raise SystemExit
        return

    # Give virtual drone time to start
    time.sleep(20)

    #Takeoff
    if not takeoff(20):
        "Something went wrong"
        stop()
        return

    if not constrainSync(20, 'alt', 1, 200):
        "Something went wrong"
        stop()
        print 'Could not takeoff'
        return

    time.sleep(1)
    # Go to A
    if not goto(A['lat'], A['lon'], 0):
        "Something went wrong"
        stop()
        print

    if not constrainSync((A['lat'], A['lon']), 'loc', .00005, 200):
        "Something went wrong"
        stop()
        print 'Could not goto'
        return

    time.sleep(1)

    #Go to B
    if not goto(B['lat'], B['lon'], 0):
        "Something went wrong"
        stop()
        print

    if not constrainSync((B['lat'], B['lon']), 'loc', .00005, 200):
        "Something went wrong"
        stop()
        print 'Could not goto'
        return

    time.sleep(1)

    #Go to C
    if not goto(C['lat'], C['lon'], 0):
        "Something went wrong"
        stop()
        print

    if not constrainSync((C['lat'], C['lon']), 'loc', .00005, 200):
        "Something went wrong"
        stop()
        print 'Could not goto'
        return

    time.sleep(1)
    #Go to HOME
    if not goto(HOME['lat'], HOME['lon'], 0):
        "Something went wrong"
        stop()
        print

    if not constrainSync((HOME['lat'], HOME['lon']), 'loc', .00005, 200):
        "Something went wrong"
        stop()
        print 'Could not goto'
        return

    time.sleep(1)

    #Land
    if not land():
        "Something went wrong"
        stop()
        return

    if not constrainSync(0, 'land', 1, 200):
        "Something went wrong"
        stop()
        print 'Could not land'
        return

    time.sleep(1)

    #Stop drone
    stop()

worker = threading.Thread(target=droneWorker)
worker.start()

httpd = SocketServer.ThreadingTCPServer(('localhost', PORT), CustomHandler)

print 'Listening on', PORT
httpd.serve_forever()

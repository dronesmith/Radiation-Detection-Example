import SocketServer
import SimpleHTTPServer
import json
import threading
import time
import math
import requests

PORT = 8080

with open('user-account.json') as json_data:
    jsonUser = json.load(json_data)
    json_data.close()

USER_EMAIL = jsonUser[0]['email']
USER_API_KEY = jsonUser[0]['api_key']
DRONE_NAME = jsonUser[0]['drone_name']

headers = {
    'user-email':       USER_EMAIL,
    'user-key':         USER_API_KEY,
    'Content-Type':     'application/json'
}

# Waypoints
HOME = {'lat':47.39774, 'lon': 8.545594}
A = {'lat':47.399091, 'lon':8.549200}
B = {'lat':47.398670, 'lon':8.551243}
C = {'lat':47.396707, 'lon':8.550953}

# Previous values
last_position = (47.39774, 8.545593, 0)
server_last_pos = (47.39774, 8.545593, 0)
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

            return (server_last_pos[0], server_last_pos[1], server_last_pos[2])

        obj = json.loads(response.text)
        server_last_pos = obj['Latitude'], obj['Longitude'], obj['Altitude']

        # print json.dumps(obj, indent=2, sort_keys=True)
        return (obj['Latitude'], obj['Longitude'], obj['Altitude'])

    def getRadIntensity(self):
        global last_sensor
        try:
            response = requests.get('http://api.dronesmith.io/api/drone/' + DRONE_NAME + '/sensor/radiation_sensor', headers=headers)
        except requests.exceptions.RequestException as e:
            print e
            print "Sensor exception"
            return (last_sensor)

        obj = json.loads(response.text)
        last_sensor = obj['intensity']
        return obj['intensity']

    def do_GET(self):
        global point
        if self.path == '/gps':
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
# Takeoff, follow a path, and land.
def droneWorker():
    # Wait for HTTP server to start displaying data
    time.sleep(1)

    if not takeoff(20):
        abort()
        return

    if not constrainSync(20, 'alt', 1, 200):
        abort()
        print 'Could not takeoff'
        return

    time.sleep(1)
    # Go to A
    if not goto(A['lat'], A['lon'], 0):
        abort()
        print

    if not constrainSync((A['lat'], A['lon']), 'loc', .00005, 200):
        abort()
        print 'Could not goto'
        return

    time.sleep(1)

    #Go to B
    if not goto(B['lat'], B['lon'], 0):
        abort()
        print

    if not constrainSync((B['lat'], B['lon']), 'loc', .00005, 200):
        abort()
        print 'Could not goto'
        return

    time.sleep(1)

    #Go to C
    if not goto(C['lat'], C['lon'], 0):
        abort()
        print

    if not constrainSync((C['lat'], C['lon']), 'loc', .00005, 200):
        abort()
        print 'Could not goto'
        return

    time.sleep(1)
    #Go to HOME
    if not goto(HOME['lat'], HOME['lon'], 0):
        abort()
        print

    if not constrainSync((HOME['lat'], HOME['lon']), 'loc', .00005, 200):
        abort()
        print 'Could not goto'
        return

    time.sleep(1)

    if not land():
        abort()
        return

    if not constrainSync(0, 'land', 1, 200):
        abort()
        print 'Could not land'
        return


worker = threading.Thread(target=droneWorker)
worker.start()

httpd = SocketServer.ThreadingTCPServer(('localhost', PORT), CustomHandler)

print 'Listening on', PORT
httpd.serve_forever()

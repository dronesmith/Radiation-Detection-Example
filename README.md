# Radiation-Sensor-Example-App
Sample Python app that uses the Dronesmith API to find a radiation source in a defined area. 

#Instructions

1. Create a virtual drone on your account. **POST** api.dronesmith.io/api/drone/drone-name

2. Add a radiation sensor to your newly created or existing virtual drone. **POST** api.dronesmith.io/api/drone/drone-name/radiation_sensor **BODY** {"intensity": 0}

3. Add your account info to user-account.json
4. Run radiation_sensor.py
5. Run server.py in seperate terminal
6. Go to http://localhost:8080

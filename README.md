<div>
  <a href="http://community.dronesmith.io" target="_blank">
    <img src="https://dl.dropboxusercontent.com/u/348929/slack.jpg" alt="" width="100%">
  </a>
</div>

# Radiation Detection Example
This sample Python app uses the Dronesmith API to find a radiation source in a defined area.

This app has two parts - a server and a web interface. The server (`server.py`) gets position and sensor data from your drone and pushes this info to the web interface. The web interface takes this data, plots the drone position and displays drone data using Google Maps, along with the value of the radiation source using a heatmap.

The radiation app `radiation_sensor.py` represents a mock radiation sensor source and runs as a seperate Python app. As both python scripts take advantage of the Dronesmith API, they need not be ran together.

## Tools
* https://www.nde-ed.org/GeneralResources/Formula/RTFormula/InverseSquare/InverseSquareLaw.htm
* https://geopy.readthedocs.io/en/1.10.0/#data

## Dronesmith API
[Sign up here](http://api.dronesmith.io/) to get a Dronesmith API account if you don't have one already. You will get an email within a couple of business days with your key. Contact [our support](http://community.dronesmith.io) if you don't receive your key within 5 business days

## Prerequisites
All that is needed for this tutorial is Python, python-pip, a Google API key, and a Dronesmith API account. This can be done on Mac, Windows, or Linux.

**Installing Python:** https://www.python.org/downloads/release/python-2712/

**Note:** Make sure you are using Python 2.7, *not* Python 3. Type `python --version` in the command line to verify your version.

**Getting a Google API Key:** https://developers.google.com/maps/documentation/javascript/get-api-key

#### Install python pip module
**Installing Python-pip**: https://pip.pypa.io/en/stable/installing/

Install python requests module
`pip install requests`
If you're on windows, you may need to run `python -m pip` instead of just pip.

## How to Run

  1. Dronesmith API: Create a virtual drone on your account. Use the following REST request: `POST api.dronesmith.io/api/drone/<drone-name>`

  2. Add a radiation sensor to your newly created or existing virtual drone. Use the following REST request: `POST api.dronesmith.io/api/drone/drone-name/radiation_sensor BODY {"intensity": 0}`

  3. Add your account info to `user-account.json`.

  4. Run `python radiation_sensor.py`.

  5. Run `python server.py` in seperate terminal.

  6. Go to http://localhost:8080 in your browser.

## Full Tutorial

If you'd like a more comprehensive tutorial on how to use this, see our [Radiation App Tutorial](http://readme.dronesmith.io/docs/radiation-sensor-drone).

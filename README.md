<div>
  <a href="http://community.dronesmith.io" target="_blank">
    <img src="https://dl.dropboxusercontent.com/u/348929/slack.jpg" alt="" width="100%">
  </a>
</div>
This is an example project for the Dronesmith API from Dronesmith Technologies. The Dronesmith API is an HTTP requests based API that enables software first drone development.

# Radiation Detection Example
This sample Python app uses the Dronesmith API to find a radiation source in a defined area.


The file `radiation_sensor.py` represents a mock radiation sensor and runs as a seperate Python app. As both python scripts take advantage of the Dronesmith API, they need not be ran together.

## Tools
* https://www.nde-ed.org/GeneralResources/Formula/RTFormula/InverseSquare/InverseSquareLaw.htm
* https://geopy.readthedocs.io/en/1.10.0/#data

## Dronesmith API
[Sign up here](http://api.dronesmith.io/) to get a Dronesmith API account if you don't have one already. You will get an email within a couple of business days with your key. Contact [our support](http://community.dronesmith.io) if you don't receive your key within 5 business days.

## Prerequisites
All that is needed for this tutorial is Python, a Google API key, and a Dronesmith API account. This can be done on Mac, Windows, or Linux.

**Installing Python:** https://www.python.org/downloads/release/python-2712/

**Note:** Make sure you are using Python 2.7, *not* Python 3. Type `python --version` in the command line to verify your version.

**Getting a Google API Key:** https://developers.google.com/maps/documentation/javascript/get-api-key

#### Install python pip module
**Installing Python-pip**: https://pip.pypa.io/en/stable/installing/

Install python requests module
`pip install requests`
If you're on windows, you may need to run `python -m pip` instead of just pip.

## How to Run
1. **Download or clone the Github project.**

  https://github.com/dronesmith/Radiation-Detection-Example

2. **Add your email and Dronesmith API key to user.json.**

  Leave drone_name field blank. 

3. **Add your Google Developers API key to index.html.**

  Find the script with the map.googleapis.com source in the HTML body and add your key to the key field in the URL.
  ```
  <script src="https://maps.googleapis.com/maps/api/js?key=ADD-KEY-HERE&v=3.exp&libraries=visualization&callback=onGoogleReady" async defer></script>
  ```
4. **Run drone_setup.py script.**

  This will create a new virtual drone on your account and add a radiation sensor to it.

5. **Start radiation_sensor.py and leave it running.**

6. **In another terminal run server.py.**

7. **Go to http://localhost:8080**

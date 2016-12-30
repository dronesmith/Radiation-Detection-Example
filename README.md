



# Radiation Detection Example

This is an example app for the Dronesmith API from Dronesmith Technologies. The Dronesmith API is an HTTP requests based API that enables software first drone development. With the Dronesmith API you can test code on virtual drones that are built into the API and then deploy the same code on a real drone. This app uses a virtual drone to accomplish a task in a made up scenario.

## The Scenario
A deranged physics professor at Zurich University has been performing experiments in various buildings on the North side of the campus. Last night one of his experiments with radioactive materials went terribly wrong and the campus has become radioactive. Now it is up to you and your team to find the location of the failed experiment using a drone equipped with a radiation sensor.

## The App

The app commands a virtual drone to fly in a path around the Zurich University campus while plotting the path on a map.  It also displays the value of radiation intensity at each point along the flight path.

## Prerequisites
To run this app you need a Dronesmith API key. Go to [api.dronesmith.io](http://api.dronesmith.io/) to request an API key. In a few minutes you will receive an email with your key.

You also need a Google Developers API key.
https://developers.google.com/maps/documentation/javascript/get-api-key



## Setup Python

Make sure you are using Python 2.7, not Python 3. Type python --version in the command line to verify your version.

If you're new to using Python, go through these two getting started exercises to set up your developer environment:

http://learnpythonthehardway.org/book/ex0.html

http://learnpythonthehardway.org/book/ex1.html

**Install Python pip module:** https://pip.pypa.io/en/stable/installing/

This should be included by default in latest Python version.

**Install Python requests module:** `pip install requests`

**Install Python geopy module:** `pip install geopy`

If you're on windows, you may need to run python -m pip instead of just pip.


## Running the App
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

<br/>

<div>
  <a href="http://community.dronesmith.io" target="_blank">
    <img src="https://dl.dropboxusercontent.com/u/348929/slack.jpg" alt="" width="100%">
  </a>
</div>

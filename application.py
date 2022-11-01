from flask import Flask

# Python reportMissingModuleSource error from "import requests" below
# is caused by the fact that the virtual environment (virt)
# is using python rather than python3 as the python interpreter
import requests

import json

OPENWEATHER_APP_ID = '75ee49c19c9fac22f81ffcac43b80552'

LAT = 41.9
LON = -87.6

# OpenWeatherMap API Key: 75ee49c19c9fac22f81ffcac43b80552

# Main calls, first below is lat/long in imperial units
# r = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=41.9&lon=-87.6&units=imperial&appid=75ee49c19c9fac22f81ffcac43b80552')
# for cities in the US: https://api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}
# for cities in the world: https://api.openweathermap.org/data/2.5/weather?q={city name},{country code}&appid={API key}

# requests.get(
#         'https://api.openweathermap.org/data/2.5/weather?' + 
#         username +
#         '&units=imperial&appid=75ee49c19c9fac22f81ffcac43b80552').json()

# print the temperature
# def print_temp(w):
#     return '<p>The temperature is %s degrees Fahrenheit.' % (w['main']['temp']) + '</p>\n'


# this method is for tabulating together and then averaging
# out the temperatures a single latitudinal or longitudinal
# degree shift (equivalent to ~111 km) away to the North,
# South, East, and West from the input of supplied latitudinal
# and longitudinal coordinates

def tabulate_temps(a=None, b=None):
    temp_center = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(LAT) + '&lon=' + str(LON) + '&units=imperial&' + 'appid=' + OPENWEATHER_APP_ID).json()['main']['temp']

    temp_kilometer_away_north = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(LAT + 1) + '&lon=' + str(LON) + '&units=imperial&' + 'appid=' + OPENWEATHER_APP_ID).json()['main']['temp']
    temp_kilometer_away_south = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(LAT - 1) + '&lon=' + str(LON) + '&units=imperial&' + 'appid=' + OPENWEATHER_APP_ID).json()['main']['temp']
    temp_kilometer_away_east = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(LAT) + '&lon=' + str(LON + 1) + '&units=imperial&' + 'appid=' + OPENWEATHER_APP_ID).json()['main']['temp']
    temp_kilometer_away_west = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=' + str(LAT - 1) + '&lon=' + str(LON - 1) + '&units=imperial&' + 'appid=' + OPENWEATHER_APP_ID).json()['main']['temp']

    # a simple graphical compass display using a 3x3 HTML table
    row_top = '<tr><td>\</td><td>%s°F</td><td>/</td>' % temp_kilometer_away_north
    row_middle = '<tr><td>%s°F</td><td>%s°F</td><td>%s°F</td>' % (temp_kilometer_away_west, temp_center, temp_kilometer_away_east)
    row_bottom = '<tr><td>/</td><td>%s°F</td><td>\</td>' % temp_kilometer_away_south

    compass_table = '<table class="dead_center">' + row_top + row_middle + row_bottom + '</table>'

    return compass_table

# looks for an 'application' callable by default
application = Flask(__name__)

# some bits of text for the page
header_text = tabulate_temps(LAT,LON) + '''
    <html>
        <head>
            <link rel="stylesheet" href="static/styles.css">
                <title>WeatherView</title>
        </head>
    <body>'''

footer_text = '</body>\n</html>'

# add a rule for the index page
application.add_url_rule('/', 'index', (lambda: header_text + footer_text))

if __name__ == "__main__":
    # It is best to reset the below variable to false for a production deployment
   application.debug = True
   application.run(host="0.0.0.0", port=8080, threaded=True)
   
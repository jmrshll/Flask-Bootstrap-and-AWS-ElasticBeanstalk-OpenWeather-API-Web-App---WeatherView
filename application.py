from flask import Flask

# Python reportMissingModuleSource error from "import requests" below
# is caused by the fact that the virtual environment (virt)
# is using python rather than python3 as the python interpreter
import requests

import json

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
def print_temp(w):
    return '<p>The temperature is %s degrees Fahrenheit.' % (w['main']['temp']) + '</p>\n'


# this method is for tabulating together the temperatures
# a kilometer to the North, South, East, and West from
# the input of the latitudinal and longitudinal coordinates
#
# tabulate_temps
def tabulate_temps(a=None, b=None):
    #Scratch:
    # tabulate_temps(w['main]['temp'])

    # return '<p>The temperature is %s degrees Fahrenheit.</p>\n' % (w['main']['temp'])
    print("Value of a : " + str(a))
    print("Value of b : " + str(b))

    return '<p>Latitude: ' + str(a) + '; Longitude: ' + str(b) + '<p>'

# looks for an 'application' callable by default
application = Flask(__name__)

# some bits of text for the page
header_text = tabulate_temps(1,2) + '''
    <html>\n<head> <title>WeatherView</title> </head>\n<body>'''
footer_text = '</body>\n</html>'

# add a rule for the index page
application.add_url_rule('/', 'index', (lambda: header_text +
         print_temp(requests.get(
         'https://api.openweathermap.org/data/2.5/weather?lat=41.9&lon=-87.6&units=imperial&appid=75ee49c19c9fac22f81ffcac43b80552').json()) + footer_text))

if __name__ == "__main__":
    # It is best to reset the below variable to false for a production deployment
   application.debug = True
   application.run()
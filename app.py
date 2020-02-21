import datetime
from flask import Flask, flash, redirect, render_template, request, session, make_response
from werkzeug.exceptions import default_exceptions
from tempfile import mkdtemp
import os
import json
from math import sqrt
from yelpAPIQuery import yelpAPIQuery
from geopy.geocoders import Nominatim

# Set testing True/ False for testing or production
testing = False

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

stars = ["i-stars--regular-1__373c0__1HqiV, i-stars--regular-1-half__373c0__1Ght9",
    "i-stars--regular-2__373c0__3LFi9", "i-stars--regular-2-half__373c0__3LuvJ",
    "i-stars--regular-3__373c0__Xlhbn", "i-stars--regular-3-half__373c0__dpRnb",
    "i-stars--regular-4__373c0__2YrSK", "i-stars--regular-4-half__373c0__1YrPo",
    "i-stars--regular-5__373c0__N5JxY"]

@app.route('/', methods=['GET', 'POST'])
def index(result=None):
    # if request.args.get('businessType', None) and request.args.get('gps1', None) and request.args.get('gps2', None):
    if request.args.get('gps2'):

        businessType, gps1, gps2 = str(request.args['businessType']), request.args['gps1'], request.args['gps2']
        
        def convertAddressToLatLong(gps):
            geolocator = Nominatim(user_agent="YelpER")
            location = geolocator.geocode(gps)
            return (location.latitude, location.longitude)

        gps1, gps2 = convertAddressToLatLong(gps1), convertAddressToLatLong(gps2)
        print(f"Start: {gps1}, End: {gps2}")

        # print(request.args.get('gps2'))
        
        
        # gps1 = [float(e) for e in gps1.split(',')]
        # gps2 = [float(e) for e in gps2.split(',')]
        # zoom = sqrt((gps1[0] - gps2[0]) ** 2 + (gps1[1] - gps2[1]) ** 2) * 140
        # zoom = min([(gps1[0] - gps2[0]) * 140, (gps1[1] - gps2[1]) * 140])
        zoom = max([abs(gps1[0] - gps2[0]) * 19.6, abs(gps1[1] - gps2[1]) * 142])
        print(f"Zoom - {zoom}")
        
        if testing == False:
            businesses = yelpAPIQuery(businessType, gps1, gps2)
        else:
            with open('restaurantsShort.json') as json_file:
                businesses = json.load(json_file)

        businesses = businesses[:25] if len(businesses) > 25 else businesses

        # print(gps1, gps2)
        # print(type(gps1), type(gps2))
        # print(type(gps1[0]), type(gps2[0]))
        # print(gps1[0], gps2[0])
        # print(gps1[0] - gps2[0])
        # print((gps1[0] - gps2[0]) ** 2)
        # print(sqrt((gps1[0] - gps2[0]) ** 2 + (gps1[1] - gps2[1]) ** 2))
        # print(sqrt((gps1[0] - gps2[0]) ** 2 + (gps1[1] - gps2[1]) ** 2) * 47)
        # print(zoom)

        return render_template('index.html', businesses = businesses, stars = stars, zoom = zoom, gps1 = gps1, gps2 = gps2)
    print("outside the loop")
    return render_template('index.html')

if __name__ == '__main__':
    app.run


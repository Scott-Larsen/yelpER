import datetime
from flask import Flask, flash, redirect, render_template, request, session, make_response
from werkzeug.exceptions import default_exceptions
from tempfile import mkdtemp
import os
import json
from math import sqrt

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

with open('restaurantsShort.json') as json_file:
    restaurants = json.load(json_file)

stars = ["i-stars--regular-1__373c0__1HqiV, i-stars--regular-1-half__373c0__1Ght9",
    "i-stars--regular-2__373c0__3LFi9", "i-stars--regular-2-half__373c0__3LuvJ",
    "i-stars--regular-3__373c0__Xlhbn", "i-stars--regular-3-half__373c0__dpRnb",
    "i-stars--regular-4__373c0__2YrSK", "i-stars--regular-4-half__373c0__1YrPo",
    "i-stars--regular-5__373c0__N5JxY"]

def make_reservation(event, lot, number):
    l = lots_to_rows[lot]
    worksheet(event).update_cell(l,4, number)


@app.route('/', methods=['GET', 'POST'])
def index(result=None):
    if request.args.get('businessType', None) and request.args.get('gps1', None) and request.args.get('gps2', None):
    # if request.args.get('gps1', None):
        # result = type(request.args['gps1'])
        gps1, gps2 = request.args['gps1'], request.args['gps2']
        gps1 = [float(e) for e in gps1.split(',')]
        gps2 = [float(e) for e in gps2.split(',')]
        print(gps1, gps2)
        print(type(gps1), type(gps2))
        print(type(gps1[0]), type(gps2[0]))
        print(gps1[0], gps2[0])
        print(gps1[0] - gps2[0])
        print((gps1[0] - gps2[0]) ** 2)
        print(sqrt((gps1[0] - gps2[0]) ** 2 + (gps1[1] - gps2[1]) ** 2))
        print(sqrt((gps1[0] - gps2[0]) ** 2 + (gps1[1] - gps2[1]) ** 2) * 47)
        
        zoom = sqrt((gps1[0] - gps2[0]) ** 2 + (gps1[1] - gps2[1]) ** 2) * 160
        
        print(zoom)

        return render_template('index.html', restaurants = restaurants, stars = stars, zoom = zoom, gps1 = gps1, gps2 = gps2)

    return render_template('index.html')

if __name__ == '__main__':
    app.run


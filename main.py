"""
Flask game based after Sim City Buildit
saved in json file
features:
Allows for building and upgrading homes
"""
from flask import *
import json # saving user info
import random # select home style
import datetime # for time related tasks
import refs # constants to refer to
import os# paths

app = Flask("city builder") # create an app object for flask

assets_folder = "assets"
home_count = 1 # number of home styles (max 2nd number in assets/home) ie. home2-1.png the 1 is important

@app.route("/")
def index():
    money=0
    grid=[[]]
    resources={
            1:4,
            2:5,
            3:1}
    return render_template("index.html",money=money,grid=grid,resources=resources.items()) # render main page 

if __name__ == "__main__":
    app.run("0.0.0.0",8080,debug=True) # if run from file, debug mode
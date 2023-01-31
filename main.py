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
city_file="my_city.json"
f=open(city_file)
b=json.loads(f.read())
f.close()
assets_folder = "assets"

@app.route("/")
def index():
    money=b["money"]
    grid=b["grid"]
    resources=b["resources"]
    tpm=b["tax"]
    dt=b["datetime"]
    home_id=random.randint(1,refs.home_count)
    return render_template("index.html",money=money,grid=grid,resources=resources.items(),tpm=tpm,shop=refs.SHOP,dt=dt,hid=home_id) # render main page 
@app.route("/collect_tax")
def collect_tax():
    tpm=b["tax"]
    time_since=b["datetime"]["tax"]
    b["money"] += round(refs.minutes_since(time_since).total_seconds()*tpm/60)
    b["datetime"]["tax"]=refs.time_in_future(0)
    f=open(city_file,"w+")
    f.write(json.dumps(b))
    f.close()
    return redirect("/")
@app.route("/build/<building>/<x>/<y>/<price>")
def build(building,x,y,price):
    if int(price) > b["money"]:
        return redirect("/")
    x=int(x)
    y=int(y)
    b["money"]-=int(price)
    b["grid"][x][y]=building
    b["tax"]+=round(int(price)/1000)
    b=refs.apply_factory(b)
    f=open(city_file,"w+")
    f.write(json.dumps(b))
    f.close()
    
    return jsonify({"building":building,"x":x,"y":y})
@app.route("/expand")
def expand():
    size=len(b["grid"])
    for i in range(0,len(b["grid"])):
        b["grid"][i].append("")
    b["grid"].append(["" for i in range(0,size+1)])
    b["money"]-=((size+1)*2)*10000
    return redirect("/")
app.jinja_env.globals.update(round=round) # pass functions jinga
app.jinja_env.globals.update(get_type=refs.get_type) # pass functions jinga
app.jinja_env.globals.update(enumerate=enumerate)
app.jinja_env.globals.update(home_type=refs.home_type)
if __name__ == "__main__":
    app.run("0.0.0.0",8080,debug=True) # if run from file, debug mode
    f.close()
from datetime import datetime, timedelta
import json
import hashlib
import time
home_count = 1 # number of home styles (max 2nd number in assets/home) ie. home2-1.png the 1 is important

PRODUCTION_ITEMS=["","Wood","Steel","Plastic","Seeds","Sand","Ore"] # list of producable materials
FACTORY_PRICES  =["", 2500,  5000,   7500,     10000,  15000, 20000]

SHOP = [
    {"name":"homes","items":[
        {"name":"house","id":"home-1-{}","price":1000},
        {"name":"apartment","id":"home-2-{}","price":2500},
        {"name":"skyscraper","id":"home-3-{}","price":10000}
        ]},
    {"name":"factories","items":
        [{"name":PRODUCTION_ITEMS[i]+" Factory","id":"factory-"+str(i),"price":FACTORY_PRICES[i]} for i in range(1,len(PRODUCTION_ITEMS))]
    }
]
def time_in_future(mins) -> float:
    return (datetime.now() + timedelta(minutes=mins)).timestamp() # given x minutes in future, return epoch time for that future time
def minutes_since(time) -> float:
    return datetime.now() - datetime.fromtimestamp(time)
def add_comma(num) -> str:
    return "{:,}".format(num)
def home_type(house,hid) -> str:
    return house.format(hid)
def get_type(string) -> str:
    if "home" in string:
        return "home"
    elif "factory" in string:
        return "factory"
    elif "production" in string:
        return "production"

def create_file(name,pin):
    file=open(name+".json","w+")
    m = hashlib.sha256()
    m.update(bytes(str(pin),"utf-8"))
    grid=[eval("['' for i in range(1,5)]") for x in range(1,5)]
    thing={
        "name":name,
        "money":5000,
        "hash":m.hexdigest(),
        "tax":1,
        "grid":grid,
        "resources": {},
        "datetime":{
            "tax":time_in_future(0),
            "factory":{}
        }
    }
    json.dump(thing,file)
    file.close()
def apply_factory(b) -> dict:
    for x,i in enumerate(b):
        for y,j in enumerate(i):
            if "factory" in j:
                if x+"-"+y in b["datetime"]:
                    pass
                else:
                    b["datetime"][x+"-"+y]=time_in_future(0)
    return b
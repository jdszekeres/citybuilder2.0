from datetime import datetime, timedelta
import json
import hashlib
import time
home_count = 1 # number of home styles (max 2nd number in assets/home) ie. home2-1.png the 1 is important

PRODUCTION_ITEMS=["","Wood","Steel","Plastic","Seeds","Sand","Ore"] # list of producable materials
FACTORY_PRICES  =["", 2500,  5000,   7500,     10000,  15000, 20000]
MATERIAL_PRICES = ["",2,   5,    10,    20,    50,     100,   150  ]
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
    for x,i in enumerate(b["grid"]):
        for y,j in enumerate(i):
            if "factory" in j:
                if str(x)+"-"+str(y) in b["datetime"]["factory"]:
                    pass
                else:
                    b["datetime"]["factory"][str(x)+"-"+str(y)]=time_in_future(0)
    return b
def collect_factory(b):
    for i in b["datetime"]["factory"].items():
        coord=i[0].split("-")
        factory=int(b["grid"][int(coord[0])][int(coord[1])].replace("factory-",""))
        print((minutes_since(i[1]).total_seconds()/3600))
        items=round((minutes_since(i[1]).total_seconds()/3600)/factory)
        try:
            b["resources"][str(factory)]+=items
        except KeyError:
            b["resources"][str(factory)]=items
        b["datetime"]["factory"][i[0]]=time_in_future(0)
    return b    


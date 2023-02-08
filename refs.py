from datetime import datetime, timedelta
import json
import hashlib
import time
home_count = 2 # number of home styles (max 2nd number in assets/home) ie. home2-1.png the 1 is important

PRODUCTION_ITEMS=["","Wood","Steel","Plastic","Seeds","Sand","Ore","Chemicals","ice"] # list of producable materials
FACTORY_PRICES  =["", 2500,  5000,   7500,     10000,  15000, 20000, 30000,50000]
MATERIAL_PRICES = ["",2,   5,    10,    20,    50,     100,   150   , 300, 1000]
CRAFTSMAN_ITEMS = ["","Planks","Scrap Metal", "Bag","Sapling","Clay","Minerals","","Water"]
HOUSING_POP=["",7,150,1000]
SHOP = [
    {"name":"homes","items":[
        {"name":"house","id":"home-1-{}","price":1000},
        {"name":"apartment","id":"home-2-{}","price":2500},
        {"name":"skyscraper","id":"home-3-{}","price":10000}
        ]},
    {"name":"factories","items":
        [{"name":PRODUCTION_ITEMS[i]+" Factory","id":"factory-"+str(i),"price":FACTORY_PRICES[i]} for i in range(1,len(PRODUCTION_ITEMS))]
    },
    {"name":"park","items":
    [
        {"name":"playground", "id":"park-1","price":500,"materials":{"2":1,"3":1,"5":1}},
        {"name":"forest","id":"park-2","price":1000,"materials":{"4":4}},
        {"name":"small park", "id":"park-3","price":250,"materials":{"4":1}},
        {"name":"waterpark", "id":"park-4","price":500,"materials":{"2":5,"7":1,"c8":1}},
        {"name":"Ferris Wheel","id":"park-5","price":1500,"materials":{"2":5,"c2":5}}
        ]
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
    elif "park" in string:
        return "park"

def create_file(name,pin):
    file=open(name+".json","w+")
    m = hashlib.sha256()
    m.update(bytes(str(pin),"utf-8"))
    grid=[eval("['' for i in range(1,5)]") for x in range(1,5)]
    thing={
        "name":name,
        "money":5000,
        "population":0,
        "hash":m.hexdigest(),
        "tax":1,
        "grid":grid,
        "resources": {"1":1,"2":2},
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
        items=(minutes_since(i[1]).total_seconds()/3600)/factory
        try:
            b["resources"][str(factory)]+=items
        except KeyError:
            b["resources"][str(factory)]=items
        b["datetime"]["factory"][i[0]]=time_in_future(0)
    return b    
def req_mat(string) -> bool:
    """see if thing requires materials to craft"""
    return get_type(string) in ["park"]
def has_mat(b,mats):
    for i in mats:
        if b["resources"][i[0]] < i[1]:
            return False
    return True
def get_adjacent_cells(grid, x_coord, y_coord ):
    result = []
    for x,y in [(x_coord+i,y_coord+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:        
        result.append(grid[x][y])
    return [i for i in result if i != ""]
def census(b):
    cnt=0
    for x, i in enumerate(b["grid"]):
        for y, j in enumerate(i):
            if "home" in j:
                pop=HOUSING_POP[int(j.split("-")[1])]
                cells=[i for i in get_adjacent_cells(b["grid"],x,y) if "park" in i]
                for i in cells:
                    pop+=round(pop*(int(i.split("-")[1])/100))
                cnt+=pop
    b["population"]=cnt
    return b
                
def convert_raw(b,i):
    if i in b["resources"] and CRAFTSMAN_ITEMS[int(i)]!="":
        if b["resources"][i] > 0:
            b["resources"][i]-=1
            if str("c"+i) in b["resources"]:
                b["resources"]["c"+i]+=1
            else:
                b["resources"]["c"+i]=1
            b["money"]-=100
    return b
import json

def writejson_moisture(dictionary: dict = {"field 1": 2000, "field 2": 2000}, time: str = "False", day:str = "False"):

    with open("data/field_data.json", "w") as file:
        data = {
            "field moisture": dictionary,
            "timestamp": time,
            "day": day
        }

        json.dump(data, file, indent=2, sort_keys=True)
    return

def readjson_moisture():
    check = False 
    fields_moisture = dict()
    timestamp = ""
    day = ""
    
    try:
        with open("data/field_data.json", "r") as file:
            check = True 
            data = json.load(file)
            fields_moisture = data["field moisture"]
            timestamp = data["timestamp"]
            day = data["day"]
    except:
        print("Can not retrieve data")
    
    return check, fields_moisture, timestamp, day

# writejson_moisture({"field 1": 200, "field 2": 500})
# mylist = readjson_moisture()
# print(mylist[0])

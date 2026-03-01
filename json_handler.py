import json

def writejson_moisture(dictionary: dict = {"field 1": 2000, "field 2": 2000}, time: str = "false", day:str = "false"):

    with open("data/field_data.json", "w") as file:
        data = {
            "field moisture": dictionary,
            "timestamp": time,
            "day": day
        }

        json.dump(data, file, indent=2, sort_keys=True)
    return

def readjson_moisture():
    dictionary = dict()
    timestamp = ""
    day = ""
    try:
        with open("data/field_data.json", "r") as file:
            data = json.load(file)
            dictionary = data["field moisture"]
            timestamp = data["timestamp"]
            day = data["day"]
    except:
        print("Can not retrieve data")
        return
    
    return dictionary, timestamp, day

# writejson_moisture({"field 1": 100, "field 2": 200, "field 3": 300})
# a,b,c = readjson_moisture()
# print(b)

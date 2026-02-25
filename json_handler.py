import json

def writejson_moisture(dictionary: dict = {"field 1": 100, "field 2": 100}, time: str = "00:00:01"):

    with open("data/field_data.json", "w") as file:
        data = {
            "field moisture": dictionary,
            "timestamp": time
        }

        json.dump(data, file, indent=2, sort_keys=True)
    return

def readjson_moisture():
    dictionary = dict()
    with open("data/field_data.json", "r") as file:
        data = json.load(file)
        dictionary = data["field moisture"]
        
    return dictionary

# writejson_moisture({"field 1": 100, "field 2": 200, "field 3": 300})

# print(readjson_moisture())

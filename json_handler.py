import json

def writejson_moisture(field_1: int, field_2:int):
    with open("data/field_data.json", "w") as file:
        data = {
            "field moisture": 
                {
                "field 1": field_1,
                "field 2": field_2
                }
        }

        json.dump(data, file, indent=2)
    return

def readjson():
    with open("data/field_data.json", "r") as file:
        data = json.load(file)
    return data

writejson_moisture(600,700)
getdata = readjson()
print(getdata["field moisture"]["field 1"])
# getdata = readjson()

# print(getdata["field moisture"][0])
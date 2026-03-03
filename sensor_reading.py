import time
import board
import busio
import json_handler #Own written library
import datetime
from adafruit_ads1x15 import ads1115, AnalogIn, ads1x15


#Create i2c configuration
i2c = busio.I2C(scl= board.SCL, sda= board.SDA)

#config adc
adc = ads1115.ADS1115(i2c, address=0x48)
adc.gain = 1 #gain = 1 for voltage range of 4.096V by document

#create soil sensor
moist_sens1 = AnalogIn(adc, ads1x15.Pin.A0)
moist_sens2 = AnalogIn(adc, ads1x15.Pin.A1)

# Output voltage signal: 0~4.2v
# 0 ~300 : dry soil
# 300~700 : humid soil
# 700~950 : in water
#This sensor was made for arduino built in adc with 10 bits resolution, so we have to convert 16 bits reading to 10 bits
scaledown = 1023/65535

#Dictionary of moisture data
moist_dict: dict()

while True:
    moist_dict = {"field 1": round(moist_sens1.value*scaledown,1), "field 2": round(moist_sens2.value*scaledown,1)}
#     moist_dict = {"field 1": 500, "field 2": 200}

    
    #Get current day and time
    current_day = str(datetime.datetime.now().day)
    current_time = str(datetime.datetime.now().time())
    
    json_handler.writejson_moisture(dictionary= moist_dict, time=current_time, day=current_day)
    
    check, field_data, timestamp, day = json_handler.readjson_moisture()
    print(field_data)
    time.sleep(5)
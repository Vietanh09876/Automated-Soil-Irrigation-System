import time
import board
import json_handler
import datetime
from adafruit_ads1x15 import ads1115, AnalogIn, ads1x15


#Create i2c configuration
i2c = board.I2C()

#config adc
adc = ads1115.ADS1115(i2c)
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
    moist_dict = {"field 1": moist_sens1.value*scaledown, "field 2": moist_sens2.value*scaledown}
    
    #Get current day and time
    current_day = str(datetime.datetime.now().day)
    current_time = str(datetime.datetime.now().time())
    
    json_handler.writejson_moisture(dictionary= moist_dict, time=current_time, day=current_day)
    data,ctime,day = json_handler.readjson_moisture()
    print(day)
    time.sleep(2)
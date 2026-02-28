import time
import board
import busio
from adafruit_ads1x15 import ads1x15
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn

#Create i2c congiguration
i2c = busio.I2C(board.SCL, board.SDA)

# Output voltage signal: 0~4.2v
# 0 ~500 : dry soil
# 500~700 : humid soil
# 700~950 : in water

volt_to_value = 950/4.2

#config adc
adc = ADC.ADS1115(i2c)
adc.gain = 1 #gain = 1 for voltage range of 4.096V

#create soil sensor
moist_sens1 = AnalogIn(adc, ads1x15.Pin.A0)
moist_sens2 = AnalogIn(adc, ads1x15.Pin.A1)

while True:
    a = moist_sens2.voltage
    print(round(a*volt_to_value, ndigits=2))
    time.sleep(2)
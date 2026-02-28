import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn

#Create i2c congiguration
i2c = busio.I2C(board.SCL, board.SDA)


# 0 ~300 : dry soil
# 300~700 : humid soil
# 700~950 : in water

#config adc
adc = ADC.ADS1115(i2c)
adc.gain = 1

#create soil sensor
moist_sens1 = AnalogIn(adc, ADC.
moist_sens2 = AnalogIn(adc, ADC.P1)

while True:
    a = moist_sens1.voltage
    print(a)
    time.sleep(2)
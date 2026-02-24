import RPi.GPIO as GPIO
from gpiozero import Motor
import spidev
import time
import datetime

#Motor config
motor_1 = Motor(forward=2, backward=3)

#SPI config
spi= spidev.SpiDev()
spi.open(bus=0,device=0)
spi.max_speed_hz = 500000 #refer to minimum clock high duration
spi.mode = 0
leds = 0b0000 #LEDS setting read from right to left
leds_off = 0b0000 #Turn off all leds

print(format(leds, "04b"))

spi.xfer2([leds])
# time.sleep(2)
# leds = leds_off
# spi.xfer2([leds_off])
# 
# time.sleep(2)
# leds |= (1 << 3)
# spi.xfer([leds])
# 
# time.sleep(2)
# leds ^= (1 << 3)
# spi.xfer2([leds])


# while True:
#     motor_1.forward(speed=1)
#     time.sleep(2)
#     motor_1.stop()
#     print("ok")
    
import tkinter as tk
from tkinter import ttk
from tkinter import *
from gpiozero import Motor
import spidev
import time
import datetime
import json_handler

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

def checkmoisture():
    return

def configHMI():
    #Create plain gui
    gui = tk.Tk()
    gui.title("Gui demo")

    #Config window size and bg colour
    tools_frame = tk.Frame(gui, width=200, height=400, bg="skyblue")
    tools_frame.grid(row=0, column=0)
    
    
# while True:
#     motor_1.forward(speed=1)
#     time.sleep(2)
#     motor_1.stop()
#     print("ok")

    
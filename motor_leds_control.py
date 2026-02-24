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

#Create plain gui
gui = tk.Tk()
gui.title("Gui demo")

def checkmoisture():
    return

def configHMI():
    
    
    #Add image
    image = tk.PhotoImage(file="ATU-Logo.png")

    #Config window size and bg colour
    tools_frame = tk.Frame(gui, width=200, height=400, bg="skyblue")
    tools_frame.grid(row=0, column=0)
    
    #Display image
    tk.Label(tools_frame, bg="skyblue").grid(row=0, column=0)
    thumbnail_image = image.subsample(5,5) #resize image
    tk.Label(tools_frame, image=thumbnail_image).grid(row=0, column=0)

    #Create tab layout
    notebook = ttk.Notebook(tools_frame)
    notebook.grid(row=1, column=0)

    #Create tab 1
    tools_tab = tk.Frame(notebook, bg="skyblue")
    #Add button to tab 1
    green_button = Button(tools_tab, text="Green LED", bg="lightgrey", height=10, width=60, command=checkmoisture)
    green_button.grid(row=0, column=0)
    red_button = Button(tools_tab, text="Red LED", bg="lightgrey", height=10, width=60, command=checkmoisture)
    red_button.grid(row=1, column=0)

    #Create tab 2
    status_tab = tk.Frame(notebook, bg="skyblue")

    #Add button to tab 2
    distance_button = Button(status_tab, text="Read Distance", bg="lightgrey", height=10, width=60, command=checkmoisture)
    distance_button.grid(row=0, column=0)
    text_box = Text(status_tab, height=10, width=50)
    text_box.grid(row=1, column=0,padx=3,pady=3)

    #Display tab
    notebook.add(tools_tab, text="Command")
    notebook.add(status_tab, text="Status")
    

configHMI()
gui.mainloop()

# while True:
#     motor_1.forward(speed=1)
#     time.sleep(2)
#     motor_1.stop()
#     print("ok")

    
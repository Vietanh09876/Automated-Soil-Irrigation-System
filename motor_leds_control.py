import tkinter as tk
from tkinter import ttk
from tkinter import *
from gpiozero import Motor
import spidev
import time
import datetime
import json_handler

#Get current day and time
current_day = datetime.datetime
current_time = datetime.datetime

#Motor config
motor_1 = Motor(forward=5, backward=6)
motor_2 = Motor(forward=13, backward=26)
motor_on_num = [0, 0] #number of time a motor is turned on in the day, reset each day
motor_list = [motor_1, motor_2]

#SPI config
spi= spidev.SpiDev()
spi.open(bus=0,device=0)
spi.max_speed_hz = 500000 #refer to minimum clock high duration
spi.mode = 0

#LEDS settings
leds = 0b0000 #LEDS setting read from right to left
leds_off = 0b0000 #Turn off all leds
spi.xfer2([leds_off])

#Create plain gui
gui = tk.Tk()
gui.title("Automate Soil Irrigation")
window_width = 400
window_height = 800

# def leds_on(led_no: int):
#     global leds, spi
#     leds |= (1 << led_no)
#     print(format(leds, "04b"))
#     spi.xfer2([leds])
#     return

def turnled_on(field_no: int, led_no: int):
    global leds, spi
    #each field has 2 leds, red = 0, green = 1
    bit_no = field_no*2 + led_no 
    leds |= (1 << bit_no)
    print(format(leds, "04b"))
    spi.xfer2([leds])
    return

def turnled_off(field_no: int, led_no: int):
    global leds, spi
    #each field has 2 leds, red = 0, green = 1
    bit_no = field_no*2 + led_no
    leds &= ~(1 << bit_no)
    print(format(leds, "04b"))
    spi.xfer2([leds])
    return

def motor_on(motor_no: int):
    global motor_on_num ,motor_list
    motor_list[motor_no].forward(speed=0.25)
    motor_on_num[motor_no] += 1
    return

def motor_off(motor_no: int):
    global motor_list
    motor_list[motor_no].stop()
    return


def checkmoisture():
    global motor_list
    field_data, timestamp, day = json_handler.readjson_moisture()
    list_of_moist = []

    for i in range(len(field_data)):
        dictkey = f"field {i+1}"
        list_of_moist.append(field_data[dictkey])
    
    for moist in range(len(list_of_moist)):
        if list_of_moist[moist] < 300:
            turnled_on(moist, 1)
            turnled_off(moist, 0)
        else:
            turnled_on(moist, 0)
            turnled_off(moist, 1)
    return

def configHMI():
    
    #Add image
    myimage = tk.PhotoImage(file="ATU-Logo.png")

    #Config window size and bg colour
    tools_frame = tk.Frame(gui, width=window_width, height=window_height, bg="skyblue")
    tools_frame.grid(row=0, column=0)
    
    #Picture frame
    pictures_frame = tk.Frame(tools_frame, width=window_width, height=window_height/2, bg="skyblue")
    pictures_frame.grid(row=0, column=0)

    #Display image to picture frame
    tk.Label(pictures_frame, bg="skyblue").grid(row=0, column=0)
    thumbnail_image = myimage.subsample(5,5) #resize image
    tk.Label(pictures_frame, image=thumbnail_image).grid(row=0, column=0)
    tk.Label(pictures_frame, image=thumbnail_image).grid(row=0, column=1)

    
    
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
    

# configHMI()
# gui.mainloop()


while True:
    checkmoisture()

    time.sleep(3)

    
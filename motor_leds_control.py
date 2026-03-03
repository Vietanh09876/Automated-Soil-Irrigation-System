import tkinter as tk
from tkinter import ttk
from tkinter import *
from gpiozero import Motor
import spidev
import time
import datetime
import json_handler #Own written library



#Motor config
motor_1 = Motor(forward=5, backward=6)
motor_2 = Motor(forward=13, backward=26)
motor_list = [motor_1, motor_2]
motor_on_num = [0] * len(motor_list) #number of time a motor is turned on in the day, reset each day
motor_start_time = [0] * len(motor_list) #Record start time of motors
motor_runtime = 10 #Allowed continous motor runtime in Secs, maybe set it 4 hours
motor_state = [True] * len(motor_list) #Activation motor for future use

#SPI config
spi= spidev.SpiDev()
#default spi gpio pins
spi.open(bus=0,device=0)
spi.max_speed_hz = 500000 
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

#data varible
data_check: bool = bool()
fields_moisture = dict()
timestamp = str()
day = str()


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

def turnmotor_on(motor_no: int):
    global motor_on_num ,motor_list, motor_start_time, 
    motor_list[motor_no].forward(speed=0.25)
    motor_on_num[motor_no] += 1
    motor_start_time[motor_no] = time.time()
    print(f"Turn on motor {motor_no}")
    return

def turnmotor_off(motor_no: int):
    global motor_list, motor_start_time
    motor_list[motor_no].stop()
    motor_start_time[motor_no] = 0
    print(f"Turn off motor {motor_no}")
    return

def datahandling():
    global data_check, fields_moisture, timestamp, day, motor_on_num, motor_list
    
    check, moistdata, stamp, dday = json_handler.readjson_moisture()
    
    #check if data fetch successfully and if this is the same old data
    if check and stamp != timestamp: 
        
        #reset "number of motor on" counter when next day pass
        if dday != day:
            motor_on_num = [0] * len(motor_list) 
            
        data_check = check
        fields_moisture = moistdata
        timestamp = stamp
        day = dday
        return True
    else:
        return False

def check_motor_runtime():
    global motor_list
    for motor_no in range(len(motor_list)):
        #How long a pump has been on
        time_period = time.time() - motor_start_time[motor_no]
        if time_period > motor_runtime and motor_list[motor_no].is_active:
            turnmotor_off(motor_no)
            motor_state[motor_no] = False
            print(f"Inactivate motor {motor_no]")

def activate_motor(motor_no: int):
    motor_state[motor_no] = True

def main_controller():
    global motor_list, fields_moisture, motor_start_time, motor_runtime, motor_state
    
    
    #End function if fail to fetch data
    if datahandling() == False:
        spi.xfer2(leds_off)
        for i in motor_list:
            i.stop()
        print("Halt everything")
        return
    
    check_motor_runtime()
    
    #Add all moisture levels to a list
    list_of_moist = []
    for i in range(len(fields_moisture)):
        dictkey = f"field {i+1}"
        list_of_moist.append(fields_moisture[dictkey])
    
    #Control motor and leds based on moisture level    
    for field_no in range(len(list_of_moist)):
        if list_of_moist[field_no] < 300:
            turnled_on(field_no, 1)
            turnled_off(field_no, 0)
            
            #if pump is already on or it is shutdown by out of runtime, dont call turnmotor_on 
            if motor_state[field_no] == False or motor_list[field_no].is_active:
                print(f"keep field {field_no} the way it is") 
                continue 
            else:
                turnmotor_on(field_no)
        else:
            turnled_on(field_no, 0)
            turnled_off(field_no, 1)
            turnmotor_off(field_no)
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
#     main_controller()
    time.sleep(5)

    
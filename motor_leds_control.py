import tkinter as tk
from tkinter import ttk
from tkinter import *
from gpiozero import Motor
from gpiozero import Button as gpiobutton
import spidev
import time
import subprocess
import sys
import threading
import json_handler #Own written library

#Button config
system_state = True 
shutdownbutton = gpiobutton(4, pull_up=True)
shutdownbutton.hold_time = 5

#rsync config
rsync_command = ["rsync", "-avz", "-e", "ssh", "g00438053@florian.local:/home/g00438053/Desktop/Automated-Soil-Irrigation-System/data/field_data.json", "/home/vietanh09876/Documents/Programs/Automated Soil Irrigation System/data"]


#Motor config
motor_1 = Motor(forward=5, backward=6)
motor_2 = Motor(forward=13, backward=26)
motor_list = [motor_1, motor_2]
motor_on_num = [0] * len(motor_list) #number of time a motor is turned on in the day, reset each day
motor_start_time = [0] * len(motor_list) #Record start time of motors
motor_runtime = 300 #Allowed continous motor runtime in Secs, maybe set it 4 hours
motor_state = [True] * len(motor_list) #Activation motor for future use

#SPI config
spi= spidev.SpiDev()
spi.open(bus=0,device=0) #default spi gpio pins
spi.max_speed_hz = 500000 
spi.mode = 0

#LEDS settings
leds = 0b0000 #leds setting read from right to left
leds_off = 0b0000 #leds setting for all leds off
spi.xfer2([leds_off])

#Create plain gui
gui = tk.Tk()
gui.title("Irrigation System")
gui.geometry("1000x800")

#data varible
data_check: bool = bool()
fields_moisture = dict()
timestamp = str()
day = str()
list_of_moist_out = []

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
    global motor_on_num ,motor_list, motor_start_time 
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

def change_system_state():
    global system_state, motor_state, motor_list, leds
    if system_state == True:
        system_state = False

        for motor_no in range(len(motor_list)):
                turnmotor_off(motor_no)
        leds = leds_off
        spi.xfer2([leds])
    else:
        motor_state = [True] * len(motor_list)
        system_state = True
    return 


def datahandling():
    global data_check, fields_moisture, timestamp, day, motor_on_num, motor_list,rsync_command
    
    #If running with only 1 rasperry pi, comment out the subprocess block below, and run both this script and sensor_reading.py at the same time on 1 pi
    try:
        subprocess.run(rsync_command,timeout= 5,check=True)
        print("rsync successfully")
    except subprocess.CalledProcessError:
        print("rsync failed")
        return False
    except subprocess.TimeoutExpired:
        print("rsync timed out")
        return False
    
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
        print("New data")
        return True
    else:
        print("Old data")
        return False

def check_motor_runtime():
    global motor_list
    for motor_no in range(len(motor_list)):
        #How long a pump has been on
        time_period = time.time() - motor_start_time[motor_no]
        if time_period > motor_runtime and motor_list[motor_no].is_active:
            turnmotor_off(motor_no)
            motor_state[motor_no] = False
            turnled_on(motor_no, 0)
            turnled_off(motor_no, 1)
            print(f"Inactivate motor {motor_no}")



def main_controller():
    global motor_list, fields_moisture, motor_start_time, motor_runtime, motor_state, list_of_moist_out
    
    check_motor_runtime()

    #End function if fail to fetch data or old data
    if datahandling() == False:
        return    
    
    #Add all moisture levels to a list
    list_of_moist = []
    for i in range(len(fields_moisture)):
        dictkey = f"field {i+1}"
        list_of_moist.append(fields_moisture[dictkey])
        
    list_of_moist_out = list_of_moist
    #Control motor and leds based on moisture level    
    for field_no in range(len(list_of_moist)):
        print(f"Moist level {list_of_moist[field_no]}")
        
        if list_of_moist[field_no] < 400:
            #if pump is already on or it is shutdown by out of runtime, dont call turnmotor_on 
            if motor_state[field_no] == False or motor_list[field_no].is_active:
                print(f"Motor state {motor_state[field_no]}")
                print(f"Motor is active ? {motor_list[field_no].is_active}")
                print(f"keep field {field_no} the way it is") 
                
            else:
                turnmotor_on(field_no)
                
            if motor_list[field_no].is_active:
                turnled_on(field_no, 1)
                turnled_off(field_no, 0)
            else:
                turnled_on(field_no, 0)
                turnled_off(field_no, 1)
            
            
        else:
            turnmotor_off(field_no)
            turnled_on(field_no, 0)
            turnled_off(field_no, 1)
            
    return

def configHMI():
    global system_state, motor_list, timestamp, day, list_of_moist_out
    field1_img = tk.PhotoImage(file="pictures/cornfield2.png").subsample(2, 2)
    field2_img = tk.PhotoImage(file="pictures/download2.png").subsample(1, 1)
    atulogo = tk.PhotoImage(file="pictures/atulogo.png").subsample(5, 5)
    irrigationimg= tk.PhotoImage(file="pictures/irrigationimg.png").subsample(3, 3)

    mainframe = tk.Frame(gui, bg="green")
    mainframe.pack(fill="both", expand=True)

    notebook_frame = tk.Frame(mainframe, bg="green")
    notebook_frame.pack(fill="both", expand=True, pady=10)

    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(fill="both", expand=True)
    pump1_state = tk.BooleanVar(value=False)
    pump2_state = tk.BooleanVar(value=False)
    pump_state = ""
    pump_color = ""
    pump_text = ""

    if system_state == False:
        pump_state = "normal"
        pump_text = "Manual Override Pump OFF"
        pump_color = "red"
    else:
        pump_state = "disabled"
        pump_text = "Manual Override Unavailable"
        pump_color = "grey"
        

    def toggle_pump1():
        if pump1_state.get():
            pump_button1.config(text="Manual Override Pump ON", bg="green")
            turnmotor_on(0)
            turnled_on(field_no=0, led_no=1)    
            turnled_off(field_no=0, led_no=0)
            print("Field 1 Pump ON")
        else:
            pump_button1.config(text="Manual Override Pump OFF", bg="red")
            turnmotor_off(0)
            turnled_on(field_no=0, led_no=0)
            turnled_off(field_no=0, led_no=1)
            print("Field 1 Pump OFF")

    def toggle_pump2():
        if pump2_state.get():
            pump_button2.config(text="Manual Override Pump ON", bg="green")
            turnmotor_on(1)
            turnled_on(field_no=1, led_no=1)
            turnled_off(field_no=1, led_no=0)
            print("Field 2 Pump ON")
        else:
            pump_button2.config(text="Manual Override Pump OFF", bg="red")
            turnmotor_off(1)
            turnled_on(field_no=1, led_no=0)
            turnled_off(field_no=1, led_no=1)
            print("Field 2 Pump OFF")
            
            
            


    hometab = tk.Frame(notebook, bg="lightgreen")
    notebook.add(hometab, text="Home")
    hometext = tk.Text(hometab, height=3, width=55, font=("Arial", 18), bg="lightgreen")
    hometext.pack(pady=5)
    hometext.insert(tk.END, f"Welcome to the Automated Irrigation Sytem Interface")                         
    hometext.config(state="disabled")
    
    smalltext = tk.Text(hometab, height=3, width=65, font=("Arial", 18), bg="lightgreen")
    smalltext.pack(pady=5)
    smalltext.insert(tk.END, f"Field 1 tab will show you the soil moisture in field 1 along with the controls for a manual override pump, Field 2 tab will show you the soil moisture in field 2 along with the controls for a manual override pump")                         
    smalltext.config(state="disabled")
    
    label3 = tk.Label(hometab, image=atulogo, bg="lightgreen")
    label3.image = atulogo
    label3.pack(pady=10)
    label4 = tk.Label(hometab, image=irrigationimg, bg="lightgreen")
    label4.image = irrigationimg
    label4.pack(pady=15)
          
     
    f1_tab = tk.Frame(notebook, bg="lightgreen")
    notebook.add(f1_tab, text="Field 1")

    label1 = tk.Label(f1_tab, image=field1_img, bg="lightgreen")
    label1.image = field1_img
    label1.pack(pady=10)

    soil_text1 = tk.Text(f1_tab, height=3, width=40, font=("Arial", 14), bg="lightgreen")
    soil_text1.pack(pady=5)
    soil_text1.config(state="disabled")

    timestamp1 = tk.Text(f1_tab, height=1, width=40, font=("Arial", 12), bg="lightgreen")
    timestamp1.pack(pady=5)
    timestamp1.config(state="disabled")
    
    pump_button1 = tk.Checkbutton(
    f1_tab,
    text=pump_text,
    font=("Arial",14,"bold"),
    bg=pump_color,
    fg="white",
    width=22,
    height=4,
    variable=pump1_state,
    command=toggle_pump1,
    state=pump_state
    )
    pump_button1.pack(pady=15)

    f2_tab = tk.Frame(notebook, bg="lightgreen")
    notebook.add(f2_tab, text="Field 2")
 
    label2 = tk.Label(f2_tab, image=field2_img, bg="lightgreen")
    label2.image = field2_img
    label2.pack(pady=10)

    soil_text2 = tk.Text(f2_tab, height=3, width=40, font=("Arial", 14), bg="lightgreen")
    soil_text2.pack(pady=5)
    soil_text2.config(state="disabled")

   
    timestamp2 = tk.Text(f2_tab, height=1, width=40, font=("Arial", 12), bg="lightgreen")
    timestamp2.pack(pady=5)
    timestamp2.config(state="disabled")
    pump_button2 = tk.Checkbutton(
    f2_tab,
    text=pump_text,
    font=("Arial",14,"bold"),
    bg=pump_color,
    fg="white",
    width=22,
    height=4,
    variable=pump2_state,
    command=toggle_pump2,
    state=pump_state
    )
    pump_button2.pack(pady=15)

    
    def update_readings():
        global pump_state, pump_text, pump_color
        print("Update readings")
        hmitimestamp = f"day: {day}, time: {timestamp}"
        
        soil_text1.config(state="normal")
        soil_text1.delete("1.0", tk.END)
        soil_text1.insert(tk.END, f"Soil Moisture: {list_of_moist_out[0]}")
        soil_text1.config(state="disabled")

        timestamp1.config(state="normal")
        timestamp1.delete("1.0", tk.END)
        timestamp1.insert(tk.END, f"Timestamp: {hmitimestamp}")
        timestamp1.config(state="disabled")

        
        soil_text2.config(state="normal")
        soil_text2.delete("1.0", tk.END)
        soil_text2.insert(tk.END, f"Soil Moisture: {list_of_moist_out[1]}")
        soil_text2.config(state="disabled")

        timestamp2.config(state="normal")
        timestamp2.delete("1.0", tk.END)
        timestamp2.insert(tk.END, f"Timestamp: {hmitimestamp}")
        timestamp2.config(state="disabled")
        
        if system_state == False and pump_state == "disabled":
            pump_state = "normal"
            pump_text = "Manual Override Pump OFF"
            pump_color = "red"
            
            pump_button1.config(
            text=pump_text,
            bg=pump_color,
            variable=pump1_state,
            state=pump_state
            )
            
            pump_button2.config(
            text=pump_text,
            bg=pump_color,
            variable=pump2_state,
            state=pump_state
            )
            
        elif system_state == True:
            pump_state = "disabled"
            pump_text = "Manual Override Unavailable"
            pump_color = "grey"
            pump_button1.config(
            text=pump_text,
            bg=pump_color,
            variable=pump1_state,
            state=pump_state
            )
            
            pump_button2.config(
            text=pump_text,
            bg=pump_color,
            variable=pump2_state,
            state=pump_state
            )
        gui.after(1000, update_readings)

    
    update_readings()

def checkbutton():
    #Shutdown or turn on whole system when button is hold for 5 secs
    while True:
        shutdownbutton.when_held = change_system_state

def loop_maincontroller():
    global system_state, motor_list
    while True:
        print(f"System state: {system_state}")
        if system_state: 
            main_controller()
            
        time.sleep(2)


        
#Use threading to update data in the background of GUI
thread_0 = threading.Thread(target=checkbutton, daemon=True) #daemon allows for a thread to be shutdown whether or not is it still running
thread_1 = threading.Thread(target=loop_maincontroller, daemon=True) 
thread_0.start()
thread_1.start()

time.sleep(2)
configHMI()
gui.mainloop()

spi.xfer2([leds_off])
#shutdown all threads when gui is closed
sys.exit()


    
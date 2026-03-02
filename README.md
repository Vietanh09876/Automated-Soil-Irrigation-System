# Automated Soil Irrigation System
## Use pip to install requiremnt.txt
## Components:
- Moisture sensor: 2
- ADS1115 analog to digital converter: 1
- Leds: 2 red, 2 green
- SN74HC595N shift register: 1
- L293D motor controller: 1
- motors pumps 6v: 2
- PVC pipes: 4
- Non-polarized capacitor: 3
- 220 ohms resistors: 4


## Sensor Functions:
- Control LEDS through shift register (Done)
- Control pump motor through L293D H-bridge (Done)
- Check moist using moist sensor, write data to a json file (Done)
- Handle data to check if there is any data or data is new or old (Done)
- Create number of pump is turned on counter, to check for sensor error (Done)
- After pump is on, create timelapse to prevent pump running forever
- transfer json data through rsync

## UI functions:
- Start, shutdown and timelapse of pump working
- Ez to look at ??
- Zone visual showing different area



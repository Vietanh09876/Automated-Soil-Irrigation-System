# Automated Soil Irrigation System
##Use pip to install requiremnt.txt
##Components:Sprinkler
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
- Control LEDS through shift register
- Control pump motor through L293D H-bridge
- Check every ? minutes
- After pump is on, if after 3 checks with no significant changes from sensors, flag pump failure or sensor failure ???
- Fail safe if sensor fail, have a timelapse for pump and counter of number of pump on
- transfer json data through rsync

## UI functions:
- Start, shutdown and timelapse of pump working
- Ez to look at ??
- Zone visual showing different area



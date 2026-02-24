# Automated Soil Irrigation System
Components:Sprinkler
- Moisture sensor, adc converter: 2
- Leds, independent Control of different zone (use chips to expand io ports)
- Relays: 2
- motors pumps (5v or 12v): 2
- pipes: 3


## Sensor Functions:
- Control LEDS through shift register
- Control pump through L293D H-bridge
- Check every ? minutes
- After pump is on, if after 3 checks with no significant changes, flag pump failure or sensor failure ???
- Fail safe if sensor fail ?? infinite pumping time ??
- transfer json data through rsync

## UI functions:
- Start, shutdown and timelapse of pump working
- Ez to look at ??
- Zone visual showing different area



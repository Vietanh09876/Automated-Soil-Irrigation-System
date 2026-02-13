# Automated Soil Irrigation System
Function:Sprinkler
- Moisture sensor, adc converter: 2
- Leds, independent Control of different zone (use chips to expand io ports)
- Relays: 2
- motors pumps (5v or 12v): 2
- pipes: 3
- Zone visual showing different area
- maybe use esp32 as adc and wireless communication

## Sensor Functions:
- Check every 5 minutes
- 30 Latest datas are logged
- After pump is on, if after 3 checks with no significant changes, flag pump failure

## UI functions:
- Start, shutdown and timelapse of pump working
- Ez to look at


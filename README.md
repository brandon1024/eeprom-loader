# EEPROM Loader
A simple python-based CLI for manipulating data on an [AT28C64B parallel EEPROM](http://ww1.microchip.com/downloads/en/DeviceDoc/doc0270.pdf) using a Raspberry Pi. This tool can be used to write data, inspect data, and test the READ/WRITE capabilities of the EEPROM.

Currently, this script is only able to read and write from addresses 0 to 255 (A0-A7), since these are the only addresses I needed to manipulate. I encourage anyone extend this script to fully address all 13 address lines :heart_eyes:

## Raspberry Pi Wiring
The table below represents the wiring configuration. Be sure to double check this wiring; wiring the EEPROM incorrectly could damage the chip. This pin configuration was chosen to simplify wiring, but you can easily adjust this to your needs by modifying the script.

| GPIO Pin Number | AT28C64B Pin Number | Pin Description                  |
|-----------------|---------------------|----------------------------------|
| 31              | A0                  | Address pin 0.                   |
| 29              | A1                  | Address pin 1.                   |
| 23              | A2                  | Address pin 2.                   |
| 21              | A3                  | Address pin 3.                   |
| 7               | A4                  | Address pin 4.                   |
| 15              | A5                  | Address pin 5.                   |
| 13              | A6                  | Address pin 6.                   |
| 11              | A7                  | Address pin 7.                   |
| 33              | IO0                 | Input/Output pin 0.              |
| 35              | IO1                 | Input/Output pin 1.              |
| 37              | IO2                 | Input/Output pin 2.              |
| 40              | IO3                 | Input/Output pin 3.              |
| 16              | IO4                 | Input/Output pin 4.              |
| 36              | IO5                 | Input/Output pin 5.              |
| 32              | IO6                 | Input/Output pin 6.              |
| 26              | IO7                 | Input/Output pin 7.              |
| 18              | WE                  | Active LOW write enable signal.  |
| 22              | OE                  | Active LOW output enable signal. |
| 24              | CE                  | Active LOW chip enable signal.   |

Be sure to connect `Vcc` and `GND` pins, too.

## Usage
### Basic Usage
```
Usage: eeprom-loader.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dump  Inspect binary data from addresses 0 to 255.
  load  Write 256 bytes of data to the EEPROM.
  test  Perform a self test to ensure that the EEPROM can be written to and...
```

### Loading
```
Usage: eeprom-loader.py load [OPTIONS]

  Write 256 bytes of data to the EEPROM.

Options:
  -f, --file FILENAME  read from a file (default: -)
  --help               Show this message and exit.
```

### Inspecting
```
Usage: eeprom-loader.py dump [OPTIONS]

  Inspect binary data from addresses 0 to 255.

Options:
  -f, --file FILENAME             write to a file (default: -)
  -b, --binary / -B, --no-binary  write binary data (no pretty print)
  --help                          Show this message and exit.
```

### Testing
```
Usage: eeprom-loader.py test [OPTIONS]

  Perform a self test to ensure that the EEPROM can be written to and read
  from.

Options:
  --help  Show this message and exit.
```

## Improvement Ideas
If you're looking for something to work on, here are some ideas:
- There's no easy way to modify pin configuration (without modifying the code, of course). It would be great if there was some kind of external configuration file that could define this mapping.
- Only A0-A7 are used. We should extend this to the full A0-A12.



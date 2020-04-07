import time
import random
import click
import RPi.GPIO as GPIO

# Address Pins
PIN_A0 = 31
PIN_A1 = 29
PIN_A2 = 23
PIN_A3 = 21
PIN_A4 = 7
PIN_A5 = 15
PIN_A6 = 13
PIN_A7 = 11

# Input Pins
PIN_IO0 = 33
PIN_IO1 = 35
PIN_IO2 = 37
PIN_IO3 = 40
PIN_IO4 = 16
PIN_IO5 = 36
PIN_IO6 = 32
PIN_IO7 = 26

# Control Pins
PIN_WE_L = 18
PIN_OE_L = 22
PIN_CE_L = 24


address_channels = [PIN_A0, PIN_A1, PIN_A2, PIN_A3, PIN_A4, PIN_A5, PIN_A6, PIN_A7]
io_channels = [PIN_IO0, PIN_IO1, PIN_IO2, PIN_IO3, PIN_IO4, PIN_IO5, PIN_IO6, PIN_IO7]
control_channels = [PIN_WE_L, PIN_OE_L, PIN_CE_L]

GPIO.setmode(GPIO.BOARD)

def configure_address_channels():
    """configure address pins"""   
    GPIO.setup(address_channels, GPIO.OUT, initial=GPIO.LOW)

def configure_io_channels(dir):
    """configure IO pins as OUTPUT"""
    if dir == GPIO.OUT:
        GPIO.setup(io_channels, dir, initial=GPIO.LOW)
    else:
        GPIO.setup(io_channels, dir, pull_up_down=GPIO.PUD_UP)

def configure_control_channels():
    """configure control signals as OUTPUT"""
    GPIO.setup(control_channels, GPIO.OUT, initial=GPIO.HIGH)

def set_address_lines(address):
    """set address lines"""
    for i in range(0, 8):
        GPIO.output(address_channels[i], address & (1 << i))

def set_data_lines(data):
    """set data lines"""
    for i in range(0, 8):
        GPIO.output(io_channels[i], data & (1 << i))

def read_data_lines():
    """read byte from data lines"""
    data = 0
    data += GPIO.input(PIN_IO0) << 0
    data += GPIO.input(PIN_IO1) << 1
    data += GPIO.input(PIN_IO2) << 2
    data += GPIO.input(PIN_IO3) << 3
    data += GPIO.input(PIN_IO4) << 4
    data += GPIO.input(PIN_IO5) << 5
    data += GPIO.input(PIN_IO6) << 6
    data += GPIO.input(PIN_IO7) << 7

    return data


@click.group()
def cli():
    try:
        pass
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        GPIO.setwarnings(False)
        GPIO.cleanup()

@click.command(name="test")
def self_test():
    """Perform a self test to ensure that the EEPROM can be written to and read from."""

    click.confirm('Warning: this will overwrite any data on the EEPROM. Do you still wish to continue?', abort=True)

    print('Running test to verify READ/WRITE cycle...')
    
    # generate random offset
    offset = random.randint(0, 255)
    print('Using randomly generated offset of {}'.format(offset))

    # configure channels
    configure_address_channels()
    configure_io_channels(GPIO.OUT)
    configure_control_channels()

    GPIO.output(PIN_OE_L, GPIO.HIGH)
    GPIO.output(PIN_WE_L, GPIO.HIGH)
    GPIO.output(PIN_CE_L, GPIO.LOW)

    print('Starting EEPROM write (addr 0 to 255)')

    # write into each address the value of the address
    for addr in range(0, 256):
        set_address_lines(addr)
        set_data_lines((addr + offset) % 256)

        time.sleep(0.01)
        GPIO.output(PIN_WE_L, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(PIN_WE_L, GPIO.HIGH)
        time.sleep(0.01)
    
    print('EEPROM write complete.')
    
    configure_io_channels(GPIO.IN)
    GPIO.output(PIN_WE_L, GPIO.HIGH)
    GPIO.output(PIN_OE_L, GPIO.LOW)
    
    print('Starting EEPROM read (addr 0 to 255)')
    
    success = True
    for addr in range(0, 256):
        set_address_lines(addr)
        time.sleep(0.01)

        data_in = read_data_lines()
        expected = (addr + offset) % 256;
        if data_in != expected:
            print('mismatch: expected {} but was {}'.format(expected, data_in))
            success = False
        else:
            print('ok: addr {} had expected value of {}'.format(addr, expected))
    
    print('EEPROM read complete.')
    if success:
        print('READ/WRITE completed successfully.')
    else:
        print('One or more READ/WRITE operations did not complete successfully.')

@click.command(name="load")
@click.option('-f', '--file', 'input', type=click.File('rb'), default='-', help='read from a file (default: -)')
def load_eeprom(input):
    """Write 256 bytes of data to the EEPROM."""
    return 1

@click.command(name="dump")
@click.option('-f', '--file', 'output', type=click.File('wb'), default='-', help='write to a file (default: -)')
@click.option('-b/-B', '--binary/--no-binary', 'binary', default=False, help='write binary data (no pretty print)')
def read_eeprom(output, binary):
    """Inspect binary data from addresses 0 to 255."""
    configure_address_channels()
    configure_io_channels(GPIO.IN)
    configure_control_channels()

    GPIO.output(PIN_CE_L, GPIO.LOW)
    GPIO.output(PIN_WE_L, GPIO.HIGH)
    GPIO.output(PIN_OE_L, GPIO.LOW)
    
    for addr in range(0, 256):
        set_address_lines(addr)
        time.sleep(0.01)

        data_in = read_data_lines()
        if binary:
            output.write(bytearray([data_in]))
        else:
            output.write('{0:#x}: {1:#x} ({1:d}) ({1:b})\n'.format(addr, data_in))

cli.add_command(self_test)
cli.add_command(load_eeprom)
cli.add_command(read_eeprom)

if __name__ == '__main__':
    cli()


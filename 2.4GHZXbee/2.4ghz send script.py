##Python script to transmit data with the xbee 2.4Ghz chips

from digi.xbee.devices import XBeeDevice
import time
from digi.xbee.io import IOLine, IOMode

# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/tty.usbserial-AC00JBJ9"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 115200

#TODO: Replace with the node id of the recieving xbee
REMOTE_NODE_ID = "Main"


def main():
    print(" +--------------------------------------+")
    print(" | XBee Python Library Send Data Sample |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        # send data to the remote node id
        while True:
            raw_val = device.get_adc_value(IOLine.DIO0_AD0)
            voltage = (raw_val/1024) *3.3
            p = ((voltage - .33)/1.32) - 1
            string = str(p)
            device.send_data(remote_device, string)

       
    #device will close if there is a error
    finally:
        if device is not None and device.is_open():
            device.close()


while True:
    main()

##Python script to send data from a connected xbee module
##and a analog sensor connected directly to the module

from digi.xbee.devices import XBeeDevice
import time
from digi.xbee.io import IOLine, IOMode


# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/tty.usbserial-AK06VTFE"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 230400

# TODO: Replace with the node id of the receiving device
REMOTE_NODE_ID = "Sender"


def main():
    
    #Define your xbee device with the defined port and baudrate
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        #open the xbee device
        device.open()
        #set the io pins on the xbee board itself
        #in this example, we are using the DIO_AD0 pin on the board
        #refrence the datasheet for other availible pins
        device.set_io_configuration(IOLine.DIO0_AD0, IOMode.ADC)
        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        # a simple while loop to read the adc sample, convert it and send to the main reciever
        while True:
            raw_val = device.get_adc_value(IOLine.DIO0_AD0)
            voltage = ((raw_val/1024))*2.5
            p = ((voltage - .3333)/1.32000) - 1.00
            string = str(p)
            print(string)
            time.sleep(0.05)
            device.send_data(remote_device, string)

        
    # close the device if any error occurs 
    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()

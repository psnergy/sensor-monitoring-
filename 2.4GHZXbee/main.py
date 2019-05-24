##Micropython script that can be flashed to an xbee module that supports
##micropython
##Requirments:
    #Mac address of receiving Xbee
import xbee
import time
import machine

# TODO: replace with the 64-bit address of your target device.
dest = b'\x00\x13\xa2\x00A\x8d\x03='
#specific to xbee, at command to change vref to 3.3v
#and to set AD0 pi  to adc mode
x = xbee.XBee()
x.atcmd('AV',2)
apin= machine.ADC('D0')

while True:
   #read the value of the pin
    raw_val = apin.read()
    voltage = (raw_val/4095) *3.3
    p = ((voltage - .33)/1.32) - 1
    string = str(p)
    #transmit the message
    try:
        xbee.transmit(dest, string)
        time.sleep(0.01)
        print("Data sent successfully")
    except Exception as e:
        print("Tranmit failure: %s" % str(e))

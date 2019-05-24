##Python script to upload the receiving the sensor data from the configured xbee chips
##to graphana
##This code should be run on the raspberry pi that will be recieving the data
##Currently configured to poll data from two xbee chips
##Requirements:
    #pi must have influx install
    #the correct databases must be added prior to running the code
    #Must know the Mac address of the sending xbee devices
    #can be found on xctu or on the physical chip 


import time
import os
import sys
from influxdb import InfluxDBClient
from digi.xbee.devices import XBeeDevice
#TODO: change Influxport if configured differenly
client = InfluxDBClient(host='localhost', port=8086)
#TODO: change to the database that you would like to use
client.switch_database('service')
#TODO: configure with the port using
    #if the xbeedevice is connected without usb PI should be ttyAMA0, or ttySerial0
device = XBeeDevice("/dev/ttyUSB0",230400)
device.open()

device.flush_queues()
p1 = 0.00
p2 = 0.00
#main will recieve the data from the sending xbees and split it based on the MAC addresses
#of the xbee chips
def main():
  
    global p1,p2
    #read the incoming messages         
    xbee_message = device.read_data()
    if xbee_message is not None:
        #the variable x will pull the MAC address of the data that it recieved 
        x=str(xbee_message.remote_device.get_64bit_addr())
        #the variable mes will be the actual data that was sent
        #in this example the data coming in was formated X.XX so a float was used 
        mes = float(xbee_message.data.decode())
        #print("From %s >> %s" % (x,
         #                              xbee_message.data.decode()))
        #IMPORTANT TODO: change to theappropriate MAC addresses of the incoming data     
        if x == '0013A2004198A862':
           #print('pi1 %s' % mes)
            p1 = mes
                    
        if x == '0013A200418B647':
              # print('pi2 %s' % mes)
            p2 = mes
                    
  #global variables will take the message recieved and place where applicable 

def get_points():
    
    global p1
    global p2
    json_body = [
        {
            "measurement":"o2",
            "tags": {
                "furnace": "service-unit-1",
                "side": "drive",
                "tube": "1",
                "zone": "1"
                },
                "fields":{
                    "adcval100": float(p1)
                    }
            },
        {
        
            "measurement":"o2",
            "tags": {
                "furnace": "service-unit-2",
                "side": "front",
                "tube": "1",
                "zone": "1"
                },
                "fields":{
                    "adcval112": float(p2)
                    }
            }
        ]
    return(json_body)


while True:
    main()
    data = get_points()
    client.write_points(data)
  






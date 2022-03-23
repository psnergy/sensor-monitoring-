#If someone toggles the relay, the xbee tells the godbee and the godbee sends a reset signal to turn off the relay

from machine import Pin
import time, xbee
from sys import stdin, stdout

relayPower = Pin("D12", Pin.OUT, value=0)
buttonPress = Pin("D4", Pin.IN, Pin.PULL_UP)
relayPower.off()

def netcheck():
    while True:
        status = xbee.atcmd('AI')
        if status == 0x00:
            break
        xbee.atcmd('CB', 0x01)
        time.sleep_ms(1000)

def netcheck():
    while True:
        status = xbee.atcmd('AI')
        if status == 0x00:
            break
        xbee.atcmd('CB', 0x01)
        time.sleep_ms(1000)

COUNT = 0
THEN = time.ticks_ms()
while True:
    netcheck()

    if buttonPress.value() == 0:
        relayPower.toggle()
        try:
            xbee.transmit(xbee.ADDR_COORDINATOR, "Someone toggled the relay!")
        except Exception as e:
            print("xbee Transmit failure: %s" % str(e))
        time.sleep(1)
        
    p = xbee.receive()
    if p is not None:
        payload = p['payload'].decode()
        if payload == "RESET":
            relayPower.toggle() 
            time.sleep(1)
    
    #do testing things
    now = time.ticks_ms()
    if time.ticks_diff(now, THEN) > 10000:
        COUNT +=1
        temp = xbee.atcmd('TP')
        rssi = xbee.atcmd('DB')
        remaining_children = xbee.atcmd('NC')
        supply_voltage = xbee.atcmd('%V')

        all = str(COUNT) + ' ' + str(temp) + ' ' + str(rssi) + ' ' + str(remaining_children) + ' ' + str(supply_voltage)
        print(all)
        try:
            xbee.transmit(xbee.ADDR_COORDINATOR, all)
        except Exception as e:
            print("xbee Transmit failure: %s" % str(e))
        THEN = time.ticks_ms()
    


#timer loop
#import time
#THEN = time.ticks_ms()
#while True:
#    now = time.ticks_ms()
#    if time.ticks_diff(now, THEN) > 10000:
#        print(1)
#        THEN = time.ticks_ms()





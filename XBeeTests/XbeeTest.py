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

while True:
    netcheck()

    if buttonPress.value() == 0:
        relayPower.toggle()
        time.sleep(1)
        try:
            xbee.transmit(b'\x00\x13\xa2\x00\x41\x82\xbb\xf1', "Someone toggled the relay!")
        except Exception as e:
            print("xbee Transmit failure: %s" % str(e))
    p = xbee.receive()
    if p is not None:
        payload = p['payload'].decode()
        if payload == "RESET":
            time.sleep(1)
            relayPower.toggle() 



#Communication between XBees


##########################################################################################
# GODBEE CODE
# MICROPYTHON AUTOSTART

import xbee, time
from machine import Pin
from sys import stdin, stdout

def netcheck():
    while True:
        status = xbee.atcmd('AI')
        if status == 0x00:
            break
        xbee.atcmd('CB', 0x01)
        time.sleep_ms(1000)


while True:
    #might need to put this in a try except???
    netcheck()
    #start = time.ticks_ms()
    msg = "RESET"

    p = xbee.receive()
    if p is not None:
        #print(p)
        payload = p['payload'].decode()
        print(payload)
        if payload == "Someone toggled the relay!":
            try:
                xbee.transmit(b'\x00\x13\xa2\x00\x41\xbd\x62\x74', msg)
            except Exception as e:
                print("xbee Transmit failure: %s" % str(e))

    #time.sleep(1)

    ##########################################################################################

# PS1 CODE
# MICROPYTHON AUTOSTART

import xbee, time
from machine import Pin
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


while True:
    #might need to put this in a try except???
    netcheck()
    #start = time.ticks_ms()
    msg = "I toggled the relay!"

    if buttonPress.value() == 0:
        relayPower.toggle()
        time.sleep(1)

    p = xbee.receive()
    if p is not None:
        payload = p['payload'].decode()
        print(payload)
        if payload == "RESET":
            relayPower.toggle()
            try:
                xbee.transmit(b'\x00\x13\xa2\x00\x41\x82\xbb\xf1', msg)
            except Exception as e:
                print("xbee Transmit failure: %s" % str(e))

        

#PS1 Mac: 0013A20041BD6274   b'\x00\x13\xa2\x00\x41\xbd\x62\x74'
#GOD Mac: 0013A2004182BBF1   b'\x00\x13\xa2\x00\x41\x82\xbb\xf1'
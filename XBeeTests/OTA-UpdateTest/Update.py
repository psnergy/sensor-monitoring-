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

    p = xbee.receive()
    if p is not None:
        #print(p)
        payload = p['payload'].decode()
        print(payload)
        continue

    msg = "RESET"

    if msg is not None:
        try:
            xbee.transmit(b'\x00\x13\xa2\x00\x41\xbd\x62\x74', msg)
            print("xbee Data sent successfully")
        except Exception as e:
            print("xbee Transmit failure: %s" % str(e))

    time.sleep(0.25)
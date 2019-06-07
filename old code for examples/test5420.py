import threading
import serial
import time
import sys
from influxdb import InfluxDBClient
import threading
import pyaudio
import numpy as np
from numpy import zeros,linspace,short,fromstring,hstack,transpose,log, ndarray
from scipy import fft
import piplates.DAQC2plate as DAQC2
import struct
import scipy.fftpack
import piplates.RELAYplate as RELAY
#from digi.xbee.devices import XBeeDevice
#from digi.xbee.io import IOLine, IOMode
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('insert_testing')
global button_pressed
button_pressed=0
global flag
flag = 0
global insert
insert = 1


NUM_SAMPLES = 6144#12288 #24576 #previously 6144
SAMPLING_RATE = 48000
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)


def background():
    
    global insert
    print("PSNERGY INSERT TESTING")
    print("Enter Insert Number")
    g = input()
    s = int(g)
    while True:
        global flag
        if s != 0:
            insert = str(g)
            print("Insert Number "+g+"")
            print("Type PING to run ping test")
            print("Type Break to run break test")
            print("To test next Insert type FUCK")
            c =input()
            if c == 'FUCK' :
                print("Insert Number:")
                flag = 0
                s =input()
            if c == 'PING':
                print("Ping test Selected")
                flag = 2
                c=input()
            if c == 'Break':
                print("Break test selected")
                flag = 3
                c=input()
                
threading1 = threading.Thread(target=background)
threading1.daemon = True
threading1.start()

def relay():
    global button_pressed
    
    
    if button_pressed ==1:
        RELAY.getID(1)
        'Pi-Plate RELAY'
        RELAY.relayON(1,1)
        time.sleep(0.02)
        RELAY.relayOFF(1,1)
        return()
    
def get_audio(): #Initiates audio stream and stores top 3 frequencies to top[]
    global freqy
    for i in range (0,5):
        while _stream.get_read_available()< NUM_SAMPLES: pass # sleep(0.005)
        audio_data  = fromstring(_stream.read(
             _stream.get_read_available(),exception_on_overflow=False), dtype=short)[-NUM_SAMPLES:]

        data = np.array(audio_data)

        w = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(w))
       
        # Find the peak in the coefficients
        idx = np.argmax(np.abs(w))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * SAMPLING_RATE)
        #print(int(freq_in_hertz))
        freqy =int(freq_in_hertz)
    return

def button():
    global flag
    if flag == 2:
        global button_pressed
        button_pressed = 1
        DAQC2.setDOUTbit(0,0)
        time.sleep(0.02)
        DAQC2.clrDOUTbit(0,0)
        time.sleep(0.015)
        relay()
        time.sleep(0.01)
        get_audio()
        button_pressed = 0
threading2 = threading.Thread(target=button)
threading2.daemon = True
threading2.start()
def connect():
    connected = False
    curr_dev = 0 # ttyACM* dev number
    dev_addr = "/dev/ttyUSB"
    curr_dev_addr = ""
    while not connected:
        curr_dev_addr = dev_addr + str(curr_dev)
        try:
            device = serial.Serial(curr_dev_addr, 115200, timeout=2)
            connected = True
        except (serial.SerialException, FileNotFoundError) as e:
            curr_dev += 1
            curr_dev %= 10
    return device

def initData(device):
    epoch = time.time()
    curr_time = time.time()
    while curr_time - epoch <= 2:
        getData(device)
        curr_time = time.time()
        
def getData(device):
    vals = []
    try:
        curr_time = time.time()
        line = device.readline()
        vals = line.decode('utf-8').rsplit()
        curr_time = str(curr_time)
        curr_time = curr_time[:curr_time.find('.')+3] # truncate to 2 decimal points
        #vals.insert(0, curr_time)
        return vals;
    except (serial.SerialTimeoutException, UnicodeDecodeError):
        return vals

def handleTimeout(device):
    print("TIMEOUT") #this should perhaps be logged
    device.close()
    device.open()
    return device

def printData(values):
    output = ""
    try:
        for value in values:
            output += value
            output += " "
        print(output)
    except IndexError:
        pass
    return output
def get_points(values):
    global insert
    json_body = [
        {
            "measurement":"break-force",
            "tags": {
                "Machine": "test-unit-1",
                "Insert #": insert
                },
                "fields":{
                    "Pounds-force3": float(values[0])
                    }
      
            }
        ]
    client.write_points(json_body)
        
def main():

    global flag
    device = connect()
    initData(device)
   
    
    
    while True:
        
        if flag == 2:
            values = getData(device)
            get_points(values)
        if flag == 3:
            button()



while True:
    try:
        
        main()
    except KeyboardInterrupt:
        print("Exiting.. \n")
        sys.exit()
    except serial.SerialException:
        continue
    except:
        continue

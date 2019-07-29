from influxdb import InfluxDBClient
import serial
import time

BAUD = 115200

def connect():
    connected = False
    curr_dev = 0 # ttyACM* dev number
    dev_addr = '/dev/ttyUSB'
    curr_dev_addr = ""
    while not connected:
        curr_dev_addr = dev_addr + str(curr_dev)
        try:
            device = serial.Serial(curr_dev_addr, BAUD, timeout=2)
            connected = True
        except (serial.SerialException, FileNotFoundError) as e:
            curr_dev += 1
            curr_dev %= 10
        time.sleep(2)
    return device

def get_points(pressure):
    json_body = [
        {
            "measurement":"manometer",
            "tags": {
                "box": "xbee",
                "channel": "pressure"
                },
                "fields":{
                    "pressure": pressure
                    }
            }
        ]
    return(json_body)

def main():    
    device = connect()
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('service')
    
    while True:
        line = device.readline()
        values = line.decode('utf-8').rsplit()
        pressure = (float(values[0]))
        json_body=get_points(pressure)
        client.write_points(json_body)
        
while True:
    try:
        main()
    except:
        continue

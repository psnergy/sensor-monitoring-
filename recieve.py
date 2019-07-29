from influxdb import InfluxDBClient
import serial
client = InfluxDBClient(host='localhost', port=8086)
#TODO: change to the database that you would like to use
client.switch_database('service')

# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 115200

pressure = 0

def main():
    global pressure
    device = serial.Serial("/dev/ttyUSB0", 115200, timeout=2)
    
    line = device.readline()
    values = line.decode('utf-8').rsplit()
    pressure = (float(values[0]))
def get_points():
   # print(jason)
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
while True:
    try:
        main()
        data = get_points()
        client.write_points(data)
    except:
        continue

This folder will be the code to send and recieve data from the 2.4Ghz xbee chips. On notion, go into xbee Digimesh to correctly set up the xbee chips with xctu. Once the chips are ready to go, run the script with the appropriate changes.

The 2.4Ghz Xbees are very similar to the 900Mhz xbees, you will notice that there is no recieve data for the 2.4Ghz,
This is becuase it is the same code for the 900Mhz. Please use the 900MhzRecieve script and make the appropriate changes

Requirments: Python3
             Xbee python library
             pyserial
             
IMPORTANT: main.py is used specificaly to upload directly on the xbee chip, it will start a script to transmit data

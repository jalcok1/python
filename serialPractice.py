import serial
import time

ser = serial.Serial('/dev/cu.usbmodemfa131', 9600)

print ser.name
ser.write('info\r')

count = 0

#Display Marionette info
while True:
    print ser.readline()
    count += 1
    if count == 10:
        break






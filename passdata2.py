import time
import serial
from vpython import *
arddata=serial.Serial('com3',9600)
time.sleep(1)
tube=cylinder(color=color.blue,radius=1,Length=5)
while True:
    while(arddata.in_waiting==0):
        pass
    data=arddata.readline()
    data=str(data,'utf-8')
    data=data.strip('\r\n')
    potval = float(data)
    vol=(5./1023.)*potval
    tube.length=vol
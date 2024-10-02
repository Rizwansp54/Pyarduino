import time
import serial
from vpython import *
arddata=serial.Serial('com3',9600)
time.sleep(.5)
digval=label(text='50',height=20,box=False,pos=vector(0,-2.5,2))
bulb=sphere(radius=1,color=color.red)
cyl=cylinder(radius=0.6,color=color.red,axis=vector(0,1,0),length=6)
bulbglass=sphere(radius=1.2,color=color.white,opacity=.25)
cylglass=cylinder(radius=0.8,color=color.white,axis=vector(0,1,0),opacity=0.25,length=6)
while True:
    while(arddata.in_waiting==0):
        pass
    data=arddata.readline()
    data=str(data,'utf-8')
    data=data.strip('\r\n')
    data=data.split(',')
    print(data)
    temp=float(data[0])
    hum=float(data[1])
    print(f"Temperature: {temp}, Humidity: {hum}")
    len=((4.5/115)*temp)+1.5
    cyl.len=len
    digval.text=str(temp)


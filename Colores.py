#!/usr/bin/env python
"""
    Creador de luz de fondo para arduino
"""
import time
import serial
from PIL import ImageGrab


__author__ = "Sebastian Falconaro"
__version__ = "1.0"
__email__ = "seba.falconaro@gmail.com"

connected = False
usbport = 'COM3'
com = serial.Serial(usbport,9600,timeout=1)
while not connected:
    serin = com.read()
    connected= True


def intToBin(color):
    Ret3,Ret2,Ret1,Ret0 = 0,0,0,0
    if color/128 == 1:
        Ret3 = 1
    if (color - 128*Ret3)/64 == 1:
        Ret2 = 1
    if (color - 128*Ret3 - 64*Ret2 )/32 == 1:
        Ret1 = 1
    if (color - 128*Ret3 - 64*Ret2 - 32*Ret1 )/16 == 1:
        Ret0 = 1

    return Ret3, Ret2 , Ret1, Ret0;

def getAverageScreenColor():
    """
        Revisa pixels, devuelve el promedio como 3 float RGB.
        Elegis cantidad con Calidad ( 1 son todos los pixeles, 10 un decimo)
    """
    calidad = 8
    screen = ImageGrab.grab()
    left, top, width, height = screen.getbbox()
    red, green, blue = 0.0, 0.0, 0.0
    for y in range(0, height, calidad):
        for x in range(0, width, calidad):
            color = screen.getpixel((x, y))
            red += color[0]
            green += color[1]
            blue += color[2]
    total = y/calidad * x/calidad
    if red != 0:
        red /= total
    if blue != 0:
        blue /= total
    if green != 0:
        green /= total
    return red, green, blue



if __name__ == '__main__':

    start_time = time.time()
    interval = 0.2  # Cada cuantos segs. se refresca
    i=0
    #while True:
    #    for x in range(0, 255,1):
    #        i+=1
    #        time.sleep(start_time + i * interval - time.time())
    #        R3,R2,R1,R0 = intToBin(x)
    #        print('color: %s , binario: %s%s%s%s' %(x,R3,R2,R1,R0))
    while True:
        i+=1
        time.sleep(start_time + i * interval - time.time())
        r, g, b = getAverageScreenColor()
        R3,R2,R1,R0 = intToBin(r)
        G3,G2,G1,G0 = intToBin(g)
        B3,B2,B1,B0 = intToBin(b)
        
        if R3:
            com.write('0')
        if R2:
            com.write('1')
        if R1:
            com.write('2')
        if R0:
            com.write('3')
            
        if G3:
            com.write('4')
        if G2:
            com.write('5')
        if G1:
            com.write('6')
        if G0:
            com.write('7')
        
        if B3:
            com.write('8')
        if B2:
            com.write('9')
        if B1:
            com.write('10')
        if B0:
            com.write('11')
            
            
        #print('color: red:%s green:%s blue:%s' %(r,g,b))
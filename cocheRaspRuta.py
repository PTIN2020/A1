
#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
##########################################
#Codi adaptat per l'equip A1
##########################################

from collections import deque, namedtuple

import requests
#import urllib.request

from random import random
import time
import serial
import RPi.GPIO as GPIO
# generate random integer values
from random import seed
from random import randint
# seed random number generator
seed(1)

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

in2 = 23
in1 = 24
en1 = 25
in3 = 17
in4 = 22
en2 = 27

GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.setup(18, GPIO.IN)
GPIO.setup(16, GPIO.IN)

def forward():
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(en1,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(en2,GPIO.HIGH)

def backward():
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(en1,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(en2,GPIO.HIGH)

def left():
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(en1,GPIO.HIGH)

def right():
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(en2,GPIO.HIGH)

def stop():
    GPIO.output(en1,GPIO.HIGH)
    GPIO.output(en2,GPIO.HIGH)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.HIGH)

pwm_right = GPIO.PWM(en2, 1000)
pwm_left = GPIO.PWM(en1, 1000)

if __name__== '__main__':
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.flush()
        try:
            numCotxe = "Batmovil"
            #Procesan los resultados de consultar un API
            while True: #emulació d'un do...while
                sensor=GPIO.input(18)
                sensor2=GPIO.input(16)
                peticioCotxe = requests.get('http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCotxe)) 
                item = peticioCotxe.json()
                if str(item) != "[]":
                    pasajero = item['id_pasajero']
                while peticioCotxe.status_code != 200:
                    peticioCotxe = requests.get('http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCotxe))
                itemCotxe = peticioCotxe.json();
                strRuta_pasajero = itemCotxe['ruta_pasajero']
                strRuta_desti = itemCotxe['ruta_desti']
                ruta_pasajero = []
                ruta_desti = []
                if strRuta_pasajero != " " and strRuta_desti != " ":
                    ruta_pasajero = strRuta_pasajero.split(", ")
                    ruta_desti = strRuta_desti.split(", ")
                    pasajero = itemCotxe['id_pasajero']
                    longrp = len(ruta_pasajero)
                    i = 0
                    print("Vaig cap al passatger...")
                    while i < (longrp-1):
                         if sensor==1 and sensor2==1:
                             #print("Linia negra")
                             forward()
                             speed = 4 * 11
                             pwm_left.start(speed)
                             pwm_right.start(speed)
                         elif sensor==0 and sensor2==0:
                             #print("Linia blanca")
                             stop()
                         if ser.in_waiting > 0:
                             line = ser.readline().decode('utf-8').rstrip()
                             if(line=='Obstacle davant'):
                                 print(line)
                                 stop()
                             if(line=='Obstacle darrere'):
                                 print(line)
                                 stop()
                         p = ruta_pasajero.pop(0)
                         print(ruta_pasajero)
                         actualitzapuntactual = {'puntActual': p}
                         x = requests.put('http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCotxe), json = actualitzapuntactual)
                         i += 1
                         time.sleep(2)
                    stop()
                    print("Recullo passatger...")
                    time.sleep(5)
                    peticioenconchar = requests.get('http://craaxcloud.epsevg.upc.edu:36302/encochar/'+str(numCotxe)+'/'+str(pasajero))
                    puntrd = ruta_desti[len(ruta_desti)-2]
                    longrd = len(ruta_desti)
                    j = 0
                    print("Vaig cap al destí...")
                    while j < (longrd-1):
                         if sensor==1 and sensor2==1:
                             #print("Linia negra")
                             forward()
                             speed = 4 * 11
                             pwm_left.start(speed)
                             pwm_right.start(speed)
                         elif sensor==0 and sensor2==0:
                             #print("Linia blanca")
                             stop()
                         if ser.in_waiting > 0:
                             line = ser.readline().decode('utf-8').rstrip()
                             if(line=='Obstacle davant'):
                                 print(line)
                                 stop()
                             if(line=='Obstacle darrere'):
                                 print(line)
                                 stop()
                         p = ruta_desti.pop(0)
                         print(ruta_desti)
                         actualitzapuntactual = {'puntActual': p}
                         x = requests.put('http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCotxe), json = actualitzapuntactual)
                         j += 1
                         time.sleep(2)
                    stop()
                    peticiodesencochar = requests.get('http://craaxcloud.epsevg.upc.edu:36302/desencochar/'+str(numCotxe)+'/'+str(pasajero))
                    print("Ha arribat al seu destí")
                    actualitzaCotxe = {'puntOrigen':ruta_desti[len(ruta_desti)-1], 'puntDesti':ruta_desti[len(ruta_desti)-1], 'ruta_pasajero':" ", 'ruta_desti':" "}
                    x = requests.put('http://craaxcloud.epsevg.upc.edu:36302/coches/'+str(numCotxe), json = actualitzaCotxe)
                    while x.status_code != 200 and x.status_code != 204:
                        x = requests.put('http://192.168.1.37:3000/coches/'+str(numCotxe), json = actualitzaCotxe)
                        print("adeu2")
                else:
                    time.sleep(5) #Esperem 5 segons entre peticions.
                #print("acaba")
                time.sleep(randint(3, 5))
                stop()
                #GPIO.cleanup()
        except:
                #print("Error ;-)")
                stop()
                GPIO.cleanup()
        finally:
            exit()

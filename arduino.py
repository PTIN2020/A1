#!/usr/bin/env python3
import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#motor esquerre
in2 = 23    
in1 = 24   
en1 = 25    

#motor dret
in3 = 17    
in4 = 22    
en2 = 27  

#iniciar motors 
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

#endavant
def forward():
	GPIO.output(in2,GPIO.HIGH)
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(en1,GPIO.HIGH)

	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	GPIO.output(en2,GPIO.HIGH)

#marxa enrere
def backward():
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(en1,GPIO.HIGH)

	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	GPIO.output(en2,GPIO.HIGH)

#esquerra
def left():
	GPIO.output(in2, GPIO.LOW)
	GPIO.output(in1, GPIO.LOW)
	GPIO.output(en1, GPIO.LOW)

#dreta
def right():
	GPIO.output(in3, GPIO.LOW)
	GPIO.output(in4, GPIO.LOW)
	GPIO.output(en2, GPIO.LOW)

#parada
def stop():
	GPIO.output(en1,GPIO.LOW)
	GPIO.output(en2,GPIO.LOW)
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.LOW)

#inciar pwm
pwm_right = GPIO.PWM(en2, 1000)
pwm_left = GPIO.PWM(en1, 1000)

if __name__== '__main__':
	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
	ser.flush()
	while True:
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			print(line)
			if line=='Via lliure':
				print(line)
				forward()
				speed = 8 * 11
				pwm_left.start(speed)
				pwm_right.start(speed)
			elif line=='Linia blanca':
				print(line)
				stop()
			elif line=='Obstacle darrere':
				print(line)
				stop()
			elif line=='Obstacle davant':
				print(line)
				stop()
			elif line=='Linia blanca esquerre':
				print(line)
				left()
				speed = 8 * 11
				pwm_left.start(speed)
				pwm_right.start(speed)
			elif line=='Linia blanca dreta':
				print(line)
				right()
				speed = 8 * 11
				pwm_left.start(speed)
				pwm_right.start(speed)
	GPIO.cleanup()

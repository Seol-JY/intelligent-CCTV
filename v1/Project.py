# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from grovepi import *
import time
import os
import subprocess
import requests
import urllib
import json

f = open('data.txt','w')

allow_range = 50 # cm, allow range

global cnt # sensor sensitivity
global dure # for data insertion cycle
cnt = 0
dure = 0

# ------ led ------
led = 5
pinMode(led,"OUTPUT")

# ----- light sensor -----
light_sensor = 2
pinMode(light_sensor,"INPUT")

# ------ servo ------
servo_pin = 18 # PWM servo_pin num 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50) # 50Hz
servo.start(7)

# # ------ Ultrasonic Ranger  ------
ultrasonic_ranger = 6

subprocess.Popen("python server.py".split(" "))  # Web server start

def sendText(text):     # Line Messenger Send
	url = 'https://notify-api.line.me/api/notify'
	payload = 'message=' + text.encode("utf-8")+''
	headers = {
		'Content-Type' : "application/x-www-form-urlencoded",
		'Cache-Control' : "no-cache",
		'Authorization' : "Bearer " + 'EsjKQ5Y7OOcsPO8NYdFi58egHh1EzdaEWgUdzGBDIfN'
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	responseJson = json.loads(((response.text).encode('utf-8')))



def rader(angle):  # Radar operating function arg: angle
    distance = ultrasonicRead(ultrasonic_ranger)
    
    if distance != -1 and distance <= allow_range: # lower than allow_range
        global cnt
        cnt += 1
        if cnt > 15:
            cnt = -25
            digitalWrite(led, 1)
            subprocess.Popen("espeak -s 160 -p 50 -a 200 -v +m4 'warning'".split(" "))
            sendText("Detected!!  "+"Angle: "+str(angle)+" + Distance: "+str(distance)+"cm")
    else:
        cnt = 0
        digitalWrite(led, 0)

    angle = 180 - angle
    dc = 1.0 / 18.0 * angle + 2
    servo.ChangeDutyCycle(dc)
    time.sleep(0.01)

    night = "day"
    if analogRead(light_sensor) < 100:
        night = "night"

    global dure
    dure +=1
    if dure%10 == 1: # data insertion cycle 0.01*10, -0.1
        f.write(str(angle)+" "+str(distance)+" "+ night +"\n")
        f.flush()  

try:
    while True:
        # rotate from 0 to 180
        for angle in range(0, 180):
            rader(angle)
        # rotate from 180 to 0
        for angle in range(180, 0, -1):
            rader(angle)

except KeyboardInterrupt:
    servo.stop()
    digitalWrite(led,0)

GPIO.cleanup()


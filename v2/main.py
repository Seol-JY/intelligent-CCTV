import pigpio
from time import sleep
import subprocess

pi = pigpio.pi()

subprocess.Popen("python server.py".split(" "))  # Web server start
subprocess.Popen("python streamingServer.py".split(" "))  # Streaming Server

def rader(angle):
    pi.set_servo_pulsewidth(18, 600+10*angle) # position anti-clockwise
    sleep(0.02)
    
while True:
# rotate from 0 to 180
    for angle in range(0, 180):
        rader(angle)
# rotate from 180 to 0
    for angle in range(180, 0, -1):
        rader(angle)
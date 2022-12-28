# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from time import sleep
import RPi.GPIO as GPIO
import subprocess
import requests
import json
from gtts import gTTS
import os
from urllib import unquote_plus

GPIO.setmode(GPIO.BCM)
app = Flask(__name__)

def sendText(text):     
	TARGET_URL = 'https://notify-api.line.me/api/notify'
	TOKEN = 'MPrYqP8OgYpSrPGt2C6VoFr4l6ThszjnoNoPzIUBd15'

	with open('/home/pi/Desktop/Programs/Final/success.jpg', 'rb') as file:		
		response = requests.post(
			TARGET_URL,
			headers={
			'Authorization': 'Bearer ' + TOKEN
			},
			data={
			'message': u"사람이 감지됨!!, 확률: "+text+"%",
			},
			files= {
			'imageFile': file
			}
		)

def Alert(ment):
	tts = gTTS(text=unquote_plus(ment), lang='ko')
	tts.save("tts.mp3")
	subprocess.Popen("mpg321 tts.mp3".split(" "))

@app.route("/")
def main():
	return render_template('index.html')
	
@app.route("/detect/<score>/<ment>")
def detect(score, ment):
	Alert(ment)
	sendText(score)
	return 1

app.run(host='0.0.0.0', port=8080, debug=True)
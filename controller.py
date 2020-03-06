#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import http.server
from phue import Bridge, Group
import threading
import random
import time, datetime
from queue import Queue
from collections import deque
import sys

b = Bridge('10.0.0.80')
b.connect() #Comment out after first run
group = Group(b, "Office")
if(len(sys.argv) > 1 and sys.argv[1]=="LR"):
	group = Group(b, "Living room")
lights = group.lights
print(lights)
print(lights[0].hue)

passive = ""
default_state = None

def lightning_effect(sound=False):
	print("lightning_effect - sound={}".format(sound))
	start_state = {
		"hue": lights[0].hue,
		"saturation": lights[0].saturation,
		"brightness":lights[0].brightness,
		"on": lights[0].on
	}
	# Fade "moonlight"
	group.on = True
	group.transitiontime = 4
	group.brightness = 1
	group.hue = 45000
	group.saturation = 100
	time.sleep(4)
	if(sound): thunder_noise()
	light = lights[random.randint(0, len(lights)-1)]
	light.transitiontime = 0.01
	light.saturation = 100
	light.brightness = 255
	time.sleep(0.05+random.random()*0.1)
	light.brightness = 1
	light.saturation = 100
	light = lights[random.randint(0, len(lights)-1)]
	light.transitiontime = 0.01
	light.saturation = 100
	light.brightness = 200
	time.sleep(0.05+random.random()*0.1)
	light.brightness = 1
	light.saturation = 100
	group.transitiontime = 2
	time.sleep(2)
	group.hue = start_state["hue"]
	group.saturation = start_state["saturation"]
	group.brightness = start_state["brightness"]
	group.on = start_state["on"]

def cold_effect(sound=False):
	print("cold_effect")
	global passive
	global default_state
	if(passive != "cold"):
		passive = "cold"
		start_state = {
			"hue": lights[0].hue,
			"saturation": lights[0].saturation,
			"brightness":lights[0].brightness,
			"on": lights[0].on
		}
		print(default_state)
		print(start_state)
		if(default_state==None): default_state = start_state
		# Fade "moonlight"
		group.on = True
		group.transitiontime = 4
		group.brightness = 200
		group.hue = 42807
		group.saturation = 195
	else:
		print("return to def")
		print(default_state)
		passive=""
		group.hue = default_state["hue"]
		group.saturation = default_state["saturation"]
		group.brightness = default_state["brightness"]
		group.on = default_state["on"]
		default_state = None

def passive_fire_effect(sound=False):
	print("passive_fire_effect")
	global passive
	global default_state
	if(passive != "cold"):
		passive = "cold"
		start_state = {
			"hue": lights[0].hue,
			"saturation": lights[0].saturation,
			"brightness":lights[0].brightness,
			"on": lights[0].on
		}
		print(default_state)
		print(start_state)
		if(default_state==None): default_state = start_state
		# Fade "moonlight"
		group.on = True
		group.transitiontime = 4
		group.brightness = 200
		group.hue = 42807
		group.saturation = 195
	else:
		print("return to def")
		print(default_state)
		passive=""
		group.hue = default_state["hue"]
		group.saturation = default_state["saturation"]
		group.brightness = default_state["brightness"]
		group.on = default_state["on"]
		default_state = None

def explosion_effect(sound=False):
	print("explosion_effect - sound={}".format(sound))
	start_state = {
		"hue": lights[0].hue,
		"saturation": lights[0].saturation,
		"brightness":lights[0].brightness,
		"on": lights[0].on
	}
	# Fade "moonlight"
	group.on = True
	group.transitiontime = 4
	group.brightness = 1
	group.hue = 45000
	group.saturation = 100
	light_queue = lights.copy()
	random.shuffle(light_queue)
	light_queue = deque(light_queue)
	time.sleep(1)

	def explode(light):
		time.sleep(0.05+random.random()*0.1)
		light.transitiontime = 1
		light.hue = 10000
		light.saturation = 50
		light.brightness = 255
		time.sleep(0.05)
		light.transitiontime = 7
		light.hue = 0
		light.brightness = 50
		light.saturation = 200
		time.sleep(0.7)
		# flicker
		light.transitiontime = 3
		light.hue = 5000
		light.brightness = int(random.random()*100)
		light.saturation = 200
		time.sleep(0.3)
		light.brightness = int(random.random()*200)
		time.sleep(0.3)
		light.brightness = int(random.random()*255)
		time.sleep(0.3)
		light.brightness = int(random.random()*255)
		time.sleep(0.3)
		light.brightness = int(random.random()*255)
		time.sleep(0.3)
		light.brightness = int(random.random()*200)
		time.sleep(0.3)
		light.brightness = int(random.random()*50)
		time.sleep(0.3)
	threadlist = []
	for x in range(len(light_queue)):
		light = light_queue.pop()
		light_queue.appendleft(light)
		t = threading.Thread(target=explode, args=(light,))
		t.start()
		threadlist.append(t);
		if(len(threadlist)==len(light_queue)):
			[tj.join() for tj in threadlist]
			threadlist = []
	[tj.join() for tj in threadlist]

	group.hue = start_state["hue"]
	group.saturation = start_state["saturation"]
	group.brightness = start_state["brightness"]
	group.on = start_state["on"]

def magic_missile_effect(count=3):
	print("magic_missile_effect x {}".format(count))
	start_state = {
		"hue": lights[0].hue,
		"saturation": lights[0].saturation,
		"brightness":lights[0].brightness,
		"on": lights[0].on
	}
	light_queue = lights.copy()
	random.shuffle(light_queue)
	light_queue = deque(light_queue)
	group.on = True
	group.transitiontime = 4
	group.brightness = 1
	group.hue = 45000
	group.saturation = 100
	time.sleep(1)
	threadlist = [];
	for x in range(count):
		light = light_queue.pop()
		light_queue.appendleft(light)
		def mm(light):
			time.sleep(random.randint(1, 10)/10)
			# magic_noise() #This doesn't "stack" well across multiple calls
			light.transitiontime = 1
			light.brightness = 255
			light.hue = 55000
			light.saturation = 255
			light.transitiontime = 4
			light.brightness = 1
			time.sleep(0.4)
			light.hue = 45000
			light.saturation = 100
			return
		t = threading.Thread(target=mm, args=(light,))
		t.start()
		threadlist.append(t);
		if(len(threadlist)==len(light_queue)):
			[tj.join() for tj in threadlist]
			threadlist = []
	[tj.join() for tj in threadlist]
	time.sleep(1)
	group.hue = start_state["hue"]
	group.saturation = start_state["saturation"]
	group.brightness = start_state["brightness"]
	group.on = start_state["on"]


reader = SimpleMFRC522.SimpleMFRC522()

print("Hold a tag near the reader")

try:
	while True:
		id, text = reader.read()
		print(id)
		print(text.strip())
		if(text.strip() == "lightning"):lightning_effect()
		elif(text.strip() == "cold"):cold_effect()
		elif(text.strip() == "passive_fire"):passive_fire_effect()
		elif(text.strip() == "explosion"):explosion_effect()
		elif(text.strip().startswith("magic_missile")):magic_missile_effect(int(text.split(":")[-1]) if (":" in text) else 3)
		time.sleep(1) #Avoid double tap

finally:
	print("cleaning up")
	GPIO.cleanup()

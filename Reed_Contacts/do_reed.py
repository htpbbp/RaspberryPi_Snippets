#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
from threading import Timer

GPIO.setmode(GPIO.BCM) 

MAGNET_GPIO = 17
GPIO.setup(MAGNET_GPIO, GPIO.IN) 

MAGNET_GPIO2 = 18
GPIO.setup(MAGNET_GPIO2, GPIO.IN)

counter = 0


publish.single("/sensor/garden/house", "loaded", hostname="192.168.x.x", port=1883, auth={"username":"xxx", "password":"xxx"})

def mqtt_send():
    tuer_r = GPIO.input(MAGNET_GPIO)
    tuer_l = GPIO.input(MAGNET_GPIO2)
    tuer_rVal = GPIO.input(MAGNET_GPIO)
    tuer_lVal = GPIO.input(MAGNET_GPIO2)
    
    print("##### MQTT timer ");
 
    publish.single("/sensor/garden/house/door_right", tuer_rVal, hostname="192.168.x.x", port=1883, auth={"username":"xxx", "password":"xxx"})
    publish.single("/sensor/garden/house/door_left", tuer_lVal, hostname="192.168.x.x", port=1883, auth={"username":"xxx", "password":"xxx"})

t = Timer(10.0, mqtt_send)
t.start()

def my_callback(input):
    global counter, MAGNET_GPIO, MAGNET_GPIO2
    counter += 1
    print("##### my_callback: ");
    print("GPIO: %d , count: %d" % (input, counter));
    print GPIO.input(input)
    print("##### my_callback: ");

    if(input == MAGNET_GPIO):
        subs = "/sensor/garden/house/door_right"
    else:
		subs = "/sensor/garden/house/door_left"

    publish.single(subs, GPIO.input(input), hostname="192.168.x.x", port=1883, auth={"username":"xxx", "password":"xxx"})
    #time.sleep(5)

GPIO.add_event_detect(MAGNET_GPIO, GPIO.FALLING, callback=my_callback, bouncetime=1000)
GPIO.add_event_detect(MAGNET_GPIO2, GPIO.FALLING, callback=my_callback, bouncetime=1000)


try: 
    while True:
        print("WHILE");
        print GPIO.input(MAGNET_GPIO)
        print GPIO.input(MAGNET_GPIO2)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    t.cancel()
    print "\n\t ##### Bye #####\n"

 

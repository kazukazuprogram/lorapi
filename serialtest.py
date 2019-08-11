#!/usr/bin/env python3

from serial import Serial
import RPi.GPIO as GPIO

s = Serial('/dev/serial0', 9600)

fp = open("./console_log", "w")

while True:
    r = s.readline()
    print(r)
    fp.write(r)

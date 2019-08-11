#!/usr/bin/env python3

from serial import Serial
import RPi.GPIO as GPIO

s = Serial('/dev/serial1', 115200)

while True:
    print(s.readline())

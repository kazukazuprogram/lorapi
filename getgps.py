#!/usr/bin/env python3
#coding: utf-8
#
from serial import Serial
from micropyGPS import MicropyGPS
import time
import threading
from json import dumps
from os.path import join

interval = 60*5

s = Serial('/dev/serial0', 9600, timeout=10)

gps = MicropyGPS(9, 'dd')

def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)

gpsthread = threading.Thread(target=rungps, args=())
gpsthread.daemon = True
gpsthread.start() # スレッドを起動

while True:
    if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
        data = {
            "lat" : "{:.7f}".format(gps.latitude[0]),
            "long" : "{:.7f}".format(gps.longitude[0])
        }
        try:
            data["alt"] = "{:.7f}".format(gps.altitude)
        except TypeError:
            data["alt"] = gps.altitude
        print('緯度経度:  lat:{}, long:{}, alt:{}'.format(data["lat"], data["long"], data["alt"]))
        data = "lat:{} long:{} alt:{}\n".format(data["lat"], data["long"], data["alt"])
        with open(join(".", "gps.txt"), "a") as fp:
            fp.write(data)
    else:
        print("Data not sufficient.")
    time.sleep(interval)

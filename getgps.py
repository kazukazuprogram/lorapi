#!/usr/bin/env python3
#coding: utf-8

from serial import Serial
from micropyGPS import MicropyGPS
import time
import threading
from json import dumps

interval = 1

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
        # print('%2d:%02d:%04.1f' % (h, gps.timestamp[1], gps.timestamp[2]))
        # print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        # print('海抜: %f' % gps.altitude)
        # print(gps.satellites_used)
        # print('衛星番号: (仰角, 方位角, SN比)')
        # for k, v in gps.satellite_data.items():
        #     print('%d: %s' % (k, v))
        # print('')
        data = {
            "lat" : "{:.7f}".format(gps.latitude[0]),
            "long" : "{:.7f}".format(gps.longitude[0])
        }
        print('緯度経度:   lat:{}, long:{}'.format(data["lat"], data["long"]))
        # dumps(data)
        data = "lat:{} long:{}\n".format(data["lat"], data["long"])
        print(data)
        with open(join(".", "gps.txt"), "a") as fp:
            fp.write(data)
    else:
        print("Data not sufficient.")
    time.sleep(interval)

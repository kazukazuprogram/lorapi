# ソフトシリアル経由でLoRaモジュールを読む

from serial import Serial
import RPi.GPIO as GPIO
import struct
import time

ResetPin = 12

class LoRa():
    def __init__(self):
        print("Setup __init__()")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(ResetPin, GPIO.OUT)
        GPIO.output(ResetPin, 1)
        self.s = Serial('/dev/serial1', 115200) # シリアルポートを115200kbps, 8bit, Non parity, 1 stop-bitでオープン

    def reset(self):
        print("Reset")
        GPIO.output(ResetPin, 0)
        time.sleep(0.1)
        GPIO.output(ResetPin, 1)

    def open(self):
        print("Serial Open", end="")
        self.s.open()
        print("ed")

    def close(self):
        print("Serial Close", end="")
        self.s.close()
        print("d")

    def readline(self, timeout = None):
        if timeout != None:
            self.close()
            self.s.timeout = timeout
            self.open()
        line = self.s.readline()
        if timeout != None:
            self.close()
            self.s.timeout = None
            self.open()
        return line

    def write(self, msg):
        self.s.write(msg.encode('utf-8'))

    def parse(self, line):
        fmt = '4s4s4s' + str(len(line) - 14) + 'sxx'
        data = struct.unpack(fmt, line)
        # hex2i = lambda x: int(x, 16) if int(x, 16) <= 0x7fff else ~ (0xffff - int(x, 16)) + 1
        def hex2i(x):
            if int(x, 16) <= 0x7fff:
                return int(x, 16)
            else:
                return ~ (0xffff - int(x, 16)) + 1
        rssi = hex2i(data[0])
        panid = hex2i(data[1])
        srcid = hex2i(data[2])
        msg = data[3].decode('utf-8')
        return (rssi, panid, srcid, msg)

if __name__ == "__main__":
    lr = LoRa()
    while True:
        data = lr.parse(lr.readline())
        print(data)

import socket
import time
from SunS import SunS
from TestStand import *

MOCK = False
start_x = 0
stop_x = 900
step_x = 100

start_y = 0
stop_y = 3600
step_y = 450

itime = 38
gain = 0

if __name__ == '__main__':
    log = open("SunS-log-" + str(int(time.time())) + ".csv", 'w')

    if MOCK is False:
        import serial
        serialStand = serial.Serial(
            port='COM6',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
    else:
        serialStand = Serial("stand")

    stand = Stand(serialStand)
    #'192.168.1.106'
    suns = SunS(2, 0, '192.168.1.106', 23)
    rcv = suns.connect()
    print(rcv)

    print("Init! \r")
    time.sleep(1)
    stand.enableMotors()
    time.sleep(1)

    #stand.disableMotors()
    #time.sleep(100)

    stand.setXYReferencePosition()
    #stand.goToAPosition(0, -step_y)

    for x in range(start_x, stop_x+step_x, step_x):
        for y in range(start_y, stop_y+step_y, step_y):
            print("Setting angle: " + str(x/10.0) + " " + str(y/10.0) + "\r")

            if y == 0:
                stand.goToAPosition(x, 0)
            else:
                stand.goToAPosition(x, step_y)

            stand.setYReferencePosition()
            print("Done \r")
            time.sleep(0.1)

            SunS_result = suns.measure()
            #print(SunS_result)
            log.writelines(str(time.strftime("%H:%M:%S")) + ";" + str(x) + ";" + str(y) + ";" + SunS_result.strip() + "\r")
            log.flush()
    log.close()

    stand.goToAPosition(0, 0)
    #stand.disableMotors()
    print("All done!\r")
    suns.close()
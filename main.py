import socket
import time
from SunS import SunS
from TestStand import *

MOCK = False
start_x = 0
stop_x = 600
step_x = 150

start_y = 1800
stop_y = 3600
step_y = 10

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
    time.sleep(1)
    print("Going back a little bit angle: " + str(-step_x/10.0) + " " + str(-step_y/10.0) + "\r")
    stand.goToAPosition(-5, -5)

    for x in range(start_x, stop_x+step_x, step_x):
        for y in range(start_y, stop_y+step_y, step_y):
            print("Setting angle: " + str(x/10.0) + " " + str(y/10.0) + "\r")

            if y == 0:
                stand.goToAPosition(x, 0)
            else:
                stand.goToAPosition(x, step_y)

            stand.setYReferencePosition()
            print("Done setting angle " + str(x/10.0) + " " + str(y/10.0) + "\r")
            time.sleep(0.1)

            SunS_result = suns.measure()
            print(SunS_result.strip())
            log.writelines(str(time.strftime("%H:%M:%S")) + ";" + str(x) + ";" + str(y) + ";" + SunS_result.strip() + "\r")
            log.flush()
    log.close()

    print("Moving back to start position!\r")
    stand.goToAPosition(0, 0)

    print("All done!\r")
    suns.close()
import socket
import time
from SunS import SunS
from TestStand import *

# Mock devices
MOCK_SUNS = False
MOCK_STAND = False

# 360 degrees = 128000 microsteps
# 1 degree = ~ 355.56 microsteps

# X-axis angle sweep settings in microsteps of motors
START_X = 22044
STOP_X = 24180
STEP_X = 178

# Y-axis angle sweep settings in microsteps of motors up to 360 degrees => 128000
START_Y = 0
STOP_Y = 128000
STEP_Y = 160

ITIME = 38
GAIN = 0

if __name__ == '__main__':
    log = open("SunS-log-" + str(int(time.time())) + ".csv", 'w')

    if MOCK_STAND is False:
        import serial
        serialStand = serial.Serial(
            port='COM6',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1
        )
    else:
        serialStand = Serial("stand")

    if MOCK_SUNS is True:
        ip = 'localhost'
    else:
        ip = '192.168.1.107'

    stand = Stand(serialStand)
    suns = SunS(ITIME, GAIN, ip, 23)
    rcv_hello = suns.connect()
    print(rcv_hello)

    print("Init! \r")
    time.sleep(1)
    stand.enableMotors()
    time.sleep(1)

    #stand.disableMotors()
    #time.sleep(100)

    stand.setXYReferencePosition()
    time.sleep(1)

    print("Going back a little bit angle: " + str(-STEP_X) + " " + str(-STEP_Y) + "\r")
    stand.goToAPosition(-5000, -5000)

    #stand.goToAPosition(24888, 0)
    #time.sleep(100)

    for x in range(START_X, STOP_X+STEP_X, STEP_X):
        print("Setting angle: " + str(stand.microstepsToDegrees(x)) + "\r")
        stand.goToAPosition(x, 0)
        for y in range(START_Y, STOP_Y+STEP_Y, STEP_Y):
            print("Setting angle: " + str(stand.microstepsToDegrees(x)) + " " + str(stand.microstepsToDegrees(y)) + "\r")
            stand.goToAPosition(x, y)
            print("Done setting angle " + str(stand.microstepsToDegrees(x)) + " " + str(stand.microstepsToDegrees(y)) + "\r")
            time.sleep(0.01)

            # Trigger and receive value from the SunS
            SunS_result = suns.measure()
            print(SunS_result.strip())
            log.writelines(str(time.strftime("%H:%M:%S")) + ";" + str(x) + ";" + str(y) + ";" + str(stand.microstepsToDegrees(x)) + ";" + str(stand.microstepsToDegrees(y)) + ";" + SunS_result.strip() + "\r")
            log.flush()
        stand.setYReferencePosition()
    log.close()
    suns.close()

    print("Moving back to start position!\r")
    stand.goToAPosition(0, 0)

    print("All done!\r")

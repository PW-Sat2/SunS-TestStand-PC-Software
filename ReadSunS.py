# Purpose: read values form SunS with WiFi EGSE

import time
from SunS import SunS

ITIME = 38
GAIN = 0
IP = '192.168.1.107'
PORT = 23
LOG = False

if __name__ == '__main__':

    # Create log if desired
    if LOG:
        log = open("SunS-log-" + str(int(time.time())) + ".csv", 'w')
        print("Log started \r")

    # Init connection
    suns = SunS(ITIME, GAIN, IP, PORT)
    rcv_hello = suns.connect()
    print(rcv_hello)
    print("Init! \r")

    # Read values from the SunS
    for i in range(1000):
        SunS_result = suns.measure()
        print(SunS_result.strip())
        if LOG:
            log.writelines(rcv_hello.strip() + "\r")

    # Close connection with the SunS
    suns.close()
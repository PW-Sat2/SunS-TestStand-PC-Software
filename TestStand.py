import time

MOCK = True

if MOCK is True:
    class Serial:
        def __init__(self, com):
            self.com = com

        def write(self, data):
            print("write data!") #print(self.com + ": " + str(data) + "\r")

        def readline(self):
            data = self.com + ": " + "read data!" + "\r"
            return data.encode()

        def flushInput(self):
            return "ok"
else:
    import serial


class Stand:
    def __init__(self, com_stand, verbose=False):
        self.com_stand = com_stand
        self.verbose = verbose

        command_file = open('commands.txt', 'r', encoding='latin-1')

        self.commands = []
        for line in command_file:
            self.commands.append(line.strip())

        command_file.close()

    def enableMotors(self):
        text = self.commands[0] + "\r"
        self.com_stand.write(text.encode())
        time.sleep(0.1)

    def disableMotors(self):
        text = self.commands[1] + "\r"
        self.com_stand.write(text.encode())
        time.sleep(0.1)

    def degreesToMicroSteps(self, x):
        return x/((1.8/32.0)/20.0)

    def microstepsToDegrees(self, x):
        return x*((1.8/32.0)/20.0)

    def goToAPosition(self, x, y):
        if MOCK is False:
            text = self.commands[2] + " " + str(x) + " " + str(y) + self.commands[3] + "\r"
            self.com_stand.flushInput()
            self.com_stand.write(text.encode())
            cnt = 0
            while True:
                cnt += 1
                res = self.com_stand.readline().strip()
                if self.verbose:
                    print(res.strip())
                if cnt > 500:
                    print("Cannot find ACK from the stand \r")
                    time.sleep(5)
                    self.goToAPosition(self, x, y)

                if res.find('command_done'.encode()) != -1:
                    break
        else:
            pass
        time.sleep(0.1)

    def setXReferencePosition(self):
        text = self.commands[5] + "\r"
        self.com_stand.write(text.encode())

    def setYReferencePosition(self):
        text = self.commands[4] + "\r"
        self.com_stand.write(text.encode())

    def setXYReferencePosition(self):
        text = self.commands[6] + "\r"
        self.com_stand.write(text.encode())

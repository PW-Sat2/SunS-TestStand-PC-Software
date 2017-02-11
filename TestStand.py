import time

MOCK = True

if MOCK is True:
    class Serial:
        def __init__(self, com):
            self.com = com

        def write(self, data):
            print(self.com + ": " + data + "\r")

        def readline(self):
            return self.com + ": " + "read data!" + "\r"
else:
    import serial


class Stand:
    def __init__(self, com_stand):
        self.com_stand = com_stand

        command_file = open('commands.txt', 'r')

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

    def goToAPosition(self, x, y):
        text = self.commands[2] + " " + str(x*10000) + " " + str(y*10000) + self.commands[3] + "\r"
        self.com_stand.write(text.encode())
        self.com_stand.readline()
        self.com_stand.readline()
        time.sleep(0.1)

    def goToXPosition(self, x):
        text = self.commands[7] + " " + str(x*10000) + self.commands[3] + "\r"
        self.com_stand.write(text.encode())
        self.com_stand.readline()
        self.com_stand.readline()
        time.sleep(0.1)

    def goToYPosition(self, y):
        text = self.commands[8] + " " + str(y*10000) + self.commands[3] + "\r"
        self.com_stand.write(text.encode())
        self.com_stand.readline()
        self.com_stand.readline()
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

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
        self.com_stand.write(self.commands[0] + "\r")
        time.sleep(0.1)

    def disableMotors(self):
        self.com_stand.write(self.commands[1] + "\r")
        time.sleep(0.1)

    def goToAPosition(self, x, y):
        self.com_stand.write(self.commands[2] + " " + str(x*10000) + " " + str(y*10000) + self.commands[3] + "\r")
        print(self.com_stand.readline())
        print(self.com_stand.readline())
        time.sleep(0.1)

    def setXReferencePosition(self):
        self.com_stand.write(self.commands[5] + "\r")

    def setYReferencePosition(self):
        self.com_stand.write(self.commands[4] + "\r")

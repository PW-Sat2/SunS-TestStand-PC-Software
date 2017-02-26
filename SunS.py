import socket


class SunS:
    def __init__(self, itime, gain, ip, port):
        self.itime = itime
        self.gain = gain
        self.ip = ip
        self.port = port
        self.esp_socket = socket.socket()

    def connect(self):
        self.esp_socket.connect((self.ip, self.port))
        rcv_data = self.esp_socket.makefile().readline()
        return rcv_data

    def close(self):
        self.esp_socket.close()

    def measure(self):
        data_to_send = "meas {} {}\n".format(self.itime, self.gain)
        self.esp_socket.send(data_to_send.encode())
        rcv_data = self.esp_socket.makefile().readline().strip()
        return rcv_data

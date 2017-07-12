import socket
import time


class SunS:
    def __init__(self, itime, gain, ip, port):
        self.itime = itime
        self.gain = gain
        self.ip = ip
        self.port = port
        self.esp_socket = socket.socket()
        self.esp_socket.settimeout(1)

    def connect(self):
        self.esp_socket.connect((self.ip, self.port))
        rcv_data = self.esp_socket.makefile().readline()
        return rcv_data

    def close(self):
        self.esp_socket.close()

    def measure(self):
        data_to_send = "meas {} {}\n".format(self.itime, self.gain)
        self.esp_socket.send(data_to_send.encode())
        try:
            rcv_data = self.esp_socket.makefile().readline().strip()
        except:
            rcv_data = "timeout"
        return rcv_data

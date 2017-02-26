import socket
import time

esp = socket.socket()
esp.bind(('localhost', 23))

while True:
    esp.listen(1)
    conn, addr = esp.accept()
    print("Connection from: " + str(addr))
    try:
        conn.send("HI\r\n".encode())
    except:
        break

    while True:
        try:
            data = conn.makefile().readline()
        except:
            break
        #time.sleep(0.001)
        data_to_send = '2;2;140;4;5;6;7;8;9;10;11;12;13;14;15;16;17;137;19;20;21;22;23;24;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50;51\r\n'
        conn.send(data_to_send.encode())

esp.close()





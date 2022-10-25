import socket
ip = '10.214.160.13'
port = 32871
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

s.send('get start\n'.encode('utf8'))

for _ in range(100):
    data = s.recv(1024).decode('utf8')
    next = data.split("\n")[1]
    print(next)
    s.send(('get ' + next + '\n').encode('utf8'))

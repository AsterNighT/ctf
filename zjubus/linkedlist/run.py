import socket
import re
import hashlib

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.214.160.13',11004))
question = s.recv(1024).decode('utf8')

string = re.findall(r"(?<=md5\().+?(?=\))", question)[0]

print(string)

s.send((hashlib.md5(string.encode('utf8')).hexdigest() + '\n').encode('utf8'))

question = s.recv(1024).decode('utf8')

print(question)

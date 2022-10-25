import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.214.160.13', 11002))
s.recv(1024) # rubbish
for _ in range(10):
    question = s.recv(1024).decode('utf8')
    print(question)
    answer = str(eval(question.split('=')[0])) + '\n'
    answer = answer.encode('utf8')
    print(answer)
    s.send(answer)
    s.recv(1024)  # rubbish
flag = s.recv(1024).decode('utf8')
print(flag)

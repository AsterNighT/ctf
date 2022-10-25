from pwn import *
import re
# from LibcSearcher import LibcSearcher
##context.log_level = 'debug'
libc = ELF('./libc.so.6')

free_offset = libc.symbols['free']
print(hex(free_offset))
puts_offset = libc.symbols['puts']
print(hex(puts_offset))
system_offset = libc.symbols['system']
print(hex(system_offset))

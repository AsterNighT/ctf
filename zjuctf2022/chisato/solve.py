from pwn import *
from randcrack import RandCrack

rc = RandCrack()

rm = 1
if rm == 1:
    sh = remote('10.214.160.76', 24562)
else:
    sh = process(['python', './main.py'])

sh.recv()
sh.sendline(b'0')
game_choice = ["石头", "剪刀", "布"]
cnt = 0

for i in range(512):
    recv = sh.recvline_contains(b'Round').decode('utf-8')
    id = re.match(r'Round \d+: #(.*)$', recv).group(1)
    id_num = int(id, 16)
    sh.sendline(game_choice[0].encode('utf-8'))
    recv = sh.recvline_contains('我出的是'.encode('utf-8')).decode('utf-8')
    random_choice = recv.split(' ')[-1]
    random_num = game_choice.index(random_choice)
    randombits = (id_num ^ random_num)*3+random_num
    rc.submit(randombits)
    cnt += 1

sh.sendline(b'0')

for i in range(512):
    recv = sh.recvline_contains(b'Round').decode('utf-8')
    id = re.match(r'Round \d+: #(.*)$', recv).group(1)
    id_num = int(id, 16)
    sh.sendline(game_choice[0].encode('utf-8'))
    recv = sh.recvline_contains('我出的是'.encode('utf-8')).decode('utf-8')
    random_choice = recv.split(' ')[-1]
    random_num = game_choice.index(random_choice)
    randombits = (id_num ^ random_num)*3+random_num
    if (cnt < 624):
        cnt += 1
        rc.submit(randombits)
    else:
        rc.predict_getrandbits(32)
sh.recv()
sh.sendline(b'1')
for i in range(512):
    random_choice = rc.predict_getrandbits(32) % 3
    # print(game_choice[(random_choice+2) % 3])
    sh.sendline(game_choice[(random_choice+2) % 3].encode('utf-8'))
    # print(sh.recv().decode('utf-8'))

sh.interactive()

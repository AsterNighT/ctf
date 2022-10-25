# from web3 import Web3
# w3 = Web3(Web3.HTTPProvider('http://10.214.160.76:54005'))

# address = '0x60f23d439a8094ac6403ce812eaf607df1a93340'
# w3.eth.get_code(address)

p1 = 0x5a4a554354467b526535703343545f376f5f4861436b65725f6f4e5f626c6f434b636861316e7d

print(int.to_bytes(p1,0x4f,'big'))
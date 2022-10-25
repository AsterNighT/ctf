import requests
import base64

ans1 = 'abcdefgh'
ans2 = 'abcde'

for a1 in ans1:
    for a2 in ans2:
        for a3 in range(16):
            name = '1='+a1+'&2='+a2+'&3=' + \
                str(a3)+r'&4=0335-7168800&5=%E6%B5%B7%E8%B1%9A%E9%A6%86'
            n = base64.b64encode(name.encode('utf-8')).decode('utf-8')
            r = requests.get(
                "http://202.38.93.111:10055/"+n+'.txt')
            if r.status_code == 200:
                print(r.url)

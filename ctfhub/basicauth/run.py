import requests
import base64

suffix = ['tar',
          'tar.gz',
          'zip',
          'rar']
name = ['web',
        'website',
        'backup',
        'back',
        'www',
        'wwwroot',
        'temp']

for s in suffix:
    for n in name:
        r = requests.get("http://challenge-40dca3ccb21c90c4.sandbox.ctfhub.com:10800/"+n+'.'+s)
        if r.status_code == 200:
            print(r.url)


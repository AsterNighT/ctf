from matplotlib.pyplot import get
from requests import request
import re
reset_url = 'http://10.214.160.76:39822/api/reset'
upgrade = 'http://10.214.160.76:39822/api/upgrade'
game = 'http://10.214.160.76:39822/game'
buy_url = 'http://10.214.160.76:39822/api/buy'
cookie = {'UOJSESSID': '749e35v631985ilhobqt2jtvkg',
          'id': r'hXKHHajGyXQ2Ndvc1hlt7tmYMOR4OLdwQ6lpHW76SegjfMmMew9Q5n7MwW%2FmhaVfy7YrnnewMpIM'}


def loan():
    request('POST', upgrade, cookies=cookie,
            data={'name': 'Loan', 'quantity': 1})


def getprice():
    text = request('GET', game, cookies=cookie).text
    # print(text)
    return int(re.search(r'Gas \(\$(.+?)\)', text).group(1).replace(',', ''))


def buy(num):
    request('POST', buy_url, cookies=cookie,
            data={'name': 'Natural Gas', 'quantity': num})


def reset():
    request('POST', reset_url, cookies=cookie)


while True:
    reset()
    loan()
    num = 67500 // getprice()
    buy(num)
    for _ in range(5):
        price = getprice()
        if(num*price > 120000):
            print('Nice!')
            exit(0)
    print(num*price)

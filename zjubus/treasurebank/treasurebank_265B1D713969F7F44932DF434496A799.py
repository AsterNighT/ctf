#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import os
import sys

# file_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
# flag = open(os.path.join(file_dir, 'flag'), 'r').read()
# salt = open(os.path.join(file_dir, 'salt'), 'rb').read()
# assert(len(salt) >= 8 and len(salt) <= 32)
vip = 'aaadwg'

def calculate_mdX(data):
    import execjs
    data = (salt + data).encode('hex')
    mdx = open(os.path.join(file_dir, 'mdx.js')).read()
    js = execjs.compile(mdx)
    return js.call('mdX', data)

def check(username, passcode):
    return calculate_mdX(username) == passcode

banner = """
============================ Treasure Bank ============================
  welcome to Treasure Bank, you can retrive your saved treasure here.
  we use a special MDX hash calculator to conduct the authentication,
  this is the most secure system in zhejiang university.
=======================================================================

enter the credentials for authentication:"""
print banner
sys.stdout.flush()

data = raw_input()
data = json.loads(data)
username = base64.b64decode(data['username'])
passcode = base64.b64decode(data['passcode'])

if not username:
    print 'wtf, an empty request?'
    exit(1)

if not passcode:
    if vip in username:
        print 'dwg never forgets the passcode'
        exit(1)
    print 'ah, new client here'
    new_passcode = calculate_mdX(username)
    print 'here is your passcode, bring it next time you come'
    print new_passcode
    exit(1)

if not check(username, passcode):
    print 'ah oh, bad passcode here, check it again'
    exit(1)

if vip not in username:
    print 'alright, this is your treasure:',
    print base64.b64encode(os.urandom(50))
    exit(1)

print 'hello dwg'
print 'your flag is here:',
print flag

# python 3 code

from base64 import b64decode,b64encode

key= ? #meesage lost
assert(len(key)<14)
for k in key:
  assert(0<=k<256)
  
def xor(text,key):
  new_text=list(text)
  for i in range(len(text)):
    new_text[i]=key[i%len(key)]^text[i]
  return bytes(new_text)

plain= ? #meesage lost
assert('AAA' in plain)
cipher='Dq4l/8bPnCsynznU2relLC+oGsq+xIBhBrgF+ZKHgjkM6yrxxsOyDzLuB4mDp6kHKZYkyqWf+HIGqDv1xITzJhutD/nGkpwoMp89y82doQcshjjKubX9cwbpAdudk7gGA+lY7I+8+R4umAOKho65CDOsO82lnJx/BrgJyZjA/ycOvg/qwMOYEzCkPdWEgeQMcOUJyLmMjCURkUPbnZeGPA+6WIU='


assert(cipher.encode()==b64encode(xor(b64encode(xor(plain.encode(),key)),key)))

b64decode(cipher) == xor(b64encode(xor(plain.encode(), key)), key)
xor(b64decode(cipher), key) == b64encode(xor(plain.encode(), key))
xor(b64decode(xor(b64decode(cipher), key)),key) == plain.encode()

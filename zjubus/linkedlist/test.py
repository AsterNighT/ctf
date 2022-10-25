import re
import hashlib


question = '12345'

print(len(hashlib.md5(question.encode('utf8')).hexdigest().encode('utf8')))

import numpy
text_list = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\t\n'
cipher = open('cipher_3280B7AD7D0AA006EA04F35C0A888648.txt', 'r').read()

# for key_length in range(15, 30):
#     frequency = numpy.zeros((key_length,97))
#     for seg in range(0, len(cipher), key_length):
#         for i in range(seg,seg+key_length):
#             if i>=len(cipher):
#                 break
#             frequency[i%key_length][text_list.index(cipher[i])] += 1
#     print(key_length, ":")
#     for i in range(key_length):
#         if(numpy.count_nonzero(frequency[i]))<70:
#             print(numpy.count_nonzero(frequency[i]))
# yields 
key_length = 29
high_frequency_letters = "etaonrishd"
length = 97
possible_key = []

frequency = numpy.zeros((key_length,length))
for i in range(0, len(cipher)):
    frequency[i%key_length][text_list.index(cipher[i])] += 1
for i in range(key_length):
    print("No:", i)
    sum = numpy.sum(frequency[i])-frequency[i][0] # space does not count
    for key in range(1,length):
        recovered = numpy.zeros(length)
        for j in range(length):
            recovered[j] = frequency[i][j*key%length] 
        high_frequency_sum = 0
        for letter in high_frequency_letters:
            high_frequency_sum += recovered[text_list.index(letter)]
        if high_frequency_sum/sum > 0.6:
            # print(recovered)
            print("Possible key:", key)
            possible_key.append(key)
            break

print(possible_key)

def decrypt(s, k):
    out = ''
    for i in range(len(s)):
        index = text_list.index(s[i])
        index *= pow(k[i % len(k)], -1, 97)
        index %= 97
        out += text_list[index]
    return out

text = decrypt(cipher, possible_key)
print(text)
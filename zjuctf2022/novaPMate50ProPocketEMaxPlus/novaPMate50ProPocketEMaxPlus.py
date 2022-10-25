#!/usr/bin/python3
# from secret import flag
import random

words = ["Mate Xs 2","P50 Pocket","Mate 50 Pro","P50 Pro","nova 10 Pro","MateBook X Pro","MateBook E Go","S86 Pro","WATCH GT3 Pro","FreeBuds 2","P50E","nova 9","nova 8 SE","MateBook D 14","MateBook E","Sound Joy","MatePad 11","MateBook 14s","MateStation S","MatePad Pro","FreeBuds Pro","HUAWEI WATCH D"]

def gen(level):
    res = ""
    idx = random.randint(0,len(words) - 1)
    res = words[idx]
    for i in range((level + 1) * (level + 1)):
        idx = random.randint(0,len(words) - 1)
        pos = random.randint(0,len(res) - 1)
        res = res[0:pos] + words[idx] + res[pos:]
        # print(res)
    return res


def check(): 
    for i in range(32):
        guess = gen(i)
        pos1 = random.randint(0,len(guess) - 1)
        pos2 = random.randint(0,len(guess) - 1)
        if pos1 < pos2:
            small = pos1
            big = pos2
        else:
            small = pos2
            big = pos1
        print(guess)
        small = big
        print(small, big)
        guess = guess[0:small - 1] + guess[big] + guess[small:big-1] + guess[small] + guess[big:]
        print("This is level %d" % i)
        print("And Here is my HUAWEI device ",guess)
        print("Please Tell me if is fake:")
        input1 = input().strip()
        if input1 == "true" and guess[pos1] == guess[pos2]:
            print("That's right!")
        elif input1 == "true":
            print("Wrong!")
            exit()
        elif input1 == "false":
            if guess[pos1] == guess[pos2]:
                print("Wrong!")
                exit()
            print("Okay, which pos is wrong?")
            guess_pos1 = input().strip()
            guess_pos2 = input().strip()
            if guess_pos1 == str(small) and guess_pos2 == str(big):
                print("That's right!")
            else:
                print("Wrong!")
                exit()
        else:
            print("Wrong!")
            exit()
    print("Congrates, Here is your flag ", flag)

if __name__ == "__main__":
    check()
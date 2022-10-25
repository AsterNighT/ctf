import hashlib
d01to06 = ["110111", "110108"]
d07to08 = ["21", "22"]
d11to12 = ["02"]

weight = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]

code = ['1','0','X','9','8','7','6','5','4','3','2']

for p1 in d01to06:
    for p2 in d07to08:
        for p3 in range(0,100):
            for p4 in d11to12:
                for p5 in range(1,30):
                    for p6 in range(0,1000):
                        id = p1 + p2 + str(p3) + p4 + str(p5) + str(p6)
                        sum = 0
                        for i in range(len(id)):
                            sum+=int(id[i])*weight[i]
                        sum%=11
                        id+=code[sum]
                        md5 = hashlib.md5(id.encode('utf-8')).hexdigest()
                        if(md5[0:3] == "108" and md5[len(md5)-3:]=="512"):
                            print(id)

print("done")

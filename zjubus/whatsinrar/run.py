import subprocess
file_name = "droste.zip"

def test(i):
    if i%1000 == 0:
        print("Progressing to: " + str(i))
    cmd = ['F:/tools/misc/7-Zip/7z.exe', 'x', '-sns', '-y', '-bb0' ,'-p'+str(i), file_name]
    sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    streamdata = sp.communicate()[0]
    # print(streamdata.decode('utf-8'))
    rc = sp.returncode
    if rc!=2:
        print("The password is to: " + str(i))

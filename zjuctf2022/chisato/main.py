import os
import random
情报 = "Good!"

random.seed(os.urandom(64))

底线 = 512
石头剪刀布映射 = ["石头", "剪刀", "布"]

def 石头剪刀布():
    随机数 = random.getrandbits(32) # x = 3a+b
    猜拳 = 石头剪刀布映射[随机数 % 3] # b
    轮标识符 = (随机数 // 3) ^ (随机数 % 3) # id = a^b
    return hex(轮标识符)[2:].zfill(5), 猜拳

def 检查(猜拳, 输入):
    if 猜拳 == "石头":
        return True if 输入 == "布" else False
    if 猜拳 == "剪刀":
        return True if 输入 == "石头" else False
    if 猜拳 == "布":
        return True if 输入 == "剪刀" else False

def 玩(模式):
    print('- 开始了哦！（平局也算你输哦）')
    轮 = 0
    while 轮 < 底线:
        轮 += 1
        轮标识符, 猜拳 = 石头剪刀布()
        print(f'\nRound {轮}: #{轮标识符}')
        print("- 我准备好了")
        while True:
            输入 = input("- 石头剪刀布！，我出 > ").strip()
            if 输入 in ["石头", "剪刀", "布"]:
                print(f"- 我出的是 {猜拳}")
                break
            print("- 干嘛呢，出 石头/剪刀/布 啊")
        结果 = 检查(猜拳, 输入)
        print("- 你赢了" if 结果 else "- 你输了")
        if 模式 == 1 and not 结果:
            print("你才不是真的千束！你个坏蛋！！")
            return 轮 - 1
    return 底线


def 选择模式():
    print('请选择模式:')
    print('0: 适应模式（输了不会怪你哦）')
    print('1: 认真模式')
    模式 = int(input('> '))
    assert 0 <= 模式 <= 1
    return 模式

if __name__ == '__main__':
    print('井之上泷奈出现在了你面前……\n')
    print('- 想要我得到的情报？')
    print('- 嗯嗯')
    print('- 你真的是千束吗……？')
    print('- 是的呀')
    print('- 在石头剪刀布中，只要我不使用特殊手段，千束一定会 100% 赢我，就用这个来验证你的身份吧！')
    print('- 诶多，这个嘛……\n')

    while True:
        模式 = 选择模式()
        终 = 玩(模式)
        if 模式 == 0:
            print('- 可以开始了吗？')
            continue
        if not 终 < 底线:
            print('- 你……真的是千束！\n')
            print(f'那就给你情报吧: {情报}')
        break

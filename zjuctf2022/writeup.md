# ZJUCTF 2022
Too hard for me，上一次做ctf是hackergame2021，这比hackergame2021难多了。

## Misc

### chisato?
注意到给你的两个数（标识符，选择）可以恢复出随机数来，整624个随机数就可以恢复随机数的状态，参考[https://www.anquanke.com/post/id/205861#h3-9](https://www.anquanke.com/post/id/205861#h3-9)。有个库可以直接拿来用 [Python-random-module-cracker](https://github.com/tna0y/Python-random-module-cracker)。

### 2zsteg

丢进stegsolve，发现3个通道的LSB有信息，拼起来开始肉眼识图，多试几次就能蒙对flag

### ZJU detective1

图丢进 stegsolve 里可以在RGB的LSB发现黑客留下的信息，告诉你是6个digits的密码，然后就爆破呗。

其实真是6个数字，我试了所有字符。

### ZJU detective3

extundelete跑一下，然后就能恢复出来了。

### Gacha Game

看一下网页源代码，发现有一个有趣的函数，

```javascript
var flag='';for(var i=-0x1d09*-0x1+-0x4cf+0x1bb*-0xe;i<s['\x6c'+'\x65'+'\x6e'+'\x67'+'\x74'+'\x68'];i++)flag+=String['\x66'+'\x72'+'\x6f'+'\x6d'+'\x43'+'\x68'+'\x61'+'\x72'+'\x43'+'\x6f'+'\x64'+'\x65'](s[i]^t[i]);alert(flag);
```

var flag后面的部分拉出来丢进console一跑就行

### polyglot

非常有意思的题目，第一反应是#在c里面可以define，但是在python里面是注释，于是基本框架就是：

1. 写一个合法的python
2. 用define搞成合法的c

python里面有一些预定义变量可以拿来当占位符，解决`int main(){`之类的问题

由于得跑system，得从os里面毛，最后想出了一个比较离谱的，把`from os import system`翻译成c的办法

代码如下

```c
#define __name__ int main(){
#define print printf
#define from void*
#define import =(void*)&
#define __doc__ }
#include <stdio.h>
#include <stdlib.h>
from os import system;
__name__
system("cat /flag.txt");
__doc__
```

## Crypto

其实上次比赛我基本做的都是misc（挠头），这次读研了感觉得学一点密码学。

### babymath

说出来不信，这是我卡了最久的一个crypto。

把digitsSum展开，一个数模n-1恰好是n进制下的digitSum，于是会得到300个同余方程，CRT即可

### babyDLP

尝试后发现这个phi可以分解，但是有一个巨大的因数，谔谔。

看到hint以后尝试着拿剩下的因数跑了一下 Pohlig-Hellman，得到一些垃圾。然后试着枚举哪些因数是要用的，得到正确结果。

### easyDLP

看到hint之前一点不会，看到hint之后谷歌三次，会了。

第一部分可以Smarts attack，从网上毛了个题解[CRYPTOCTF 2021 - HARD](https://blog.cryptohack.org/cryptoctf2021-hard)

第二部分分析一下以后会发现，这其实是个展开了的椭圆曲线运算（为此去认真学习了加法怎么算），将图像整体平移之后会得到一个Singular curves，直接进行一个板子的抄。

第三部分那更是直接抄 SuperSingular curves的板子，这真没啥意思。

### signin_crypto1

在纸上推了一下，发现其实中间大部分时间都在瞎搞，反正只要知道最后lr两段和原先lr两段的关系就行了，中间过程没啥用，当黑盒看就行。

从fake_flag可以推出黑盒最后和lr交互的两个参数，然后丢给真的密文恢复就行了。

### SSC

直接丢给quipquip

### HSC

这是个少了几个位置的 Hill cipher，如果把最后那个}换过来还少四个明文，没办法，穷举这几个明文，看看恢复出来的东西是不是printable。解出来的第一个答案不对，最后发现有多解，有点搞。

### MSC

MT19937 [https://www.anquanke.com/post/id/205861#h3-9](https://www.anquanke.com/post/id/205861#h3-9)，学了老半天。通过尝试可以拿到89*24个8位信息，flag里的AAA{又给了32位，刚好凑够19968位，简直是明示。

参考 coin flip 的做法，构造一个19968*19968的矩阵，然后解就完事儿了。你可能会构造出一个不满秩的矩阵，解出来多解，但运气好的话就能直接得到解（

### CPKv1

完全没懂CPK怎么工作。试了半天next，觉得不太对，怎么都是同一个返回值。debug一下发现它需要一个username的参数。给一个username=admin进去，给了一些奇怪的回复。

在flag上故技重施，发现需要一个key参数，把admin的private key传进去，咋就过了？

### pretend to be rich

论文题，文章也才4页，实现都给你了，花20分钟看完论文你就能白得400分

给r2和D2各乘一个编号就行

## Pwm

### shellcode_master1&2

我上网毛了个25字节的shellcode

### signin_pwn1

首先，我叫/bin/sh

从got把printf毛出来，找到system，把system写进free

### signin_pwn2

每一次只能写一次，没有泄露的地址只写一次是不可能搞定的，只能想办法多搞几次

最后有一个exit，把这个exit的got改成main，然后再调用一次main，就可以再搞无数次了

注意到system调一个不存在的东西只报错不崩溃，所以可以把printf改成system

第二次搞出地址，第三次把printf的got改成system，第四次输入/bin/sh

### UOJ Hacks 1

公告里真的有题解，抄过来直接用了。

把stdout buffer然后atexit输出

## Web

### pentest1

think PHP v5有个代码执行漏洞，根据提示找一下.sh文件会找到一个bak.sh，把里面的Token:user改成Token:admin即可

谁想的Token后面跟名字？？？？

### warmup

改一下 UA 和 X-Forwarded-By

### Re0

php的pregmatch有个bug，超过100000的字符串直接就挂了，所以把post的code长度超过100000就行了。

## Reverse
### babyre

符号还在，读一下发现是个SM4

把参数拿出来单独跑一个SM4的解密即可。

### apk1
根据题面描述，丢进模拟器把定位跳到昆仑站即可

### apk1.33
apktools+dex2jar反汇编出来代码，把逻辑反向实现一遍即可

### re signin
快乐的读高级语言时间

## Blockchain
### eth secret

[layout_in_storage](https://docs.soliditylang.org/en/v0.8.17/internals/layout_in_storage.html)

根据以太坊的存储方式，得算个keccak256(0)，然后getStorageAt即可。

## Forensics
我只做了签到和签退qwq

## Hardware
### HarmonyOS1
跑起来以后一顿瞎搞，不知道为什么毛出来一个flag.js，用jerry跑一下即可。

这玩意不支持相对路径，谔谔。

### HarmonyOS2
date里面有额外的信息，`watch -n 1 date`

## PPC
### Self SHA
额，虽然提示说是 Hash length extension attack，但我只做了quine

如果当quine做的话那就是裸quine，就是长了点。
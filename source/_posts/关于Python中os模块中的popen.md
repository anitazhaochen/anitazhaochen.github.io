---
title: 关于Python中os模块中的popen
date: 2020-08-26 17:08:30
tags: [Python]
category: Python
---

近期写一些脚本需要用到 os.popen 函数，然后就看了下实现，发现它返回的是一个文件描述符，就跟 open 这个操作返回的东西一样，只不过 os.popen 返回的是一个只读的。

然后联想到，如果返回的是一个类似文件的fd，岂不是需要执行完命令后，需要手动 close 嘛。

于是做了一个小实验来一探究竟。首先需要一些命令辅助。

```shell
ps -ef |grep demo.py|awk '{print $2}'
```

这个命令是用来查看我们运行 Python 程序后进程 PID 的。

```shell
<!--more -->
lsof -p PID | wc -l
```

这个命令把上一步我们拿到的 PID 填充进去，就可以得到这个进程打开的文件数量。

一般来说，就算我们的程序没有打开额外的文件，这个命令也不会显示0，因为这个进程总会打开一些 Python 库必须的文件，我这里是10个。

在额外说一个命令，修改系统单个进程能够打开的最大文件句柄数量：

```shell
ulimit -n       # 查看当前系统定义的单个进程最大打开的句柄数

lsof -n|awk '{print $2}'|sort|uniq -c|sort -nr|more  #输入第一列为 PID ，第二列为数量

ps aef|grep PID  # 根据进程 PID 查看进程的信息

ulimit – HSn 2048  # 临时设置文件句柄数， 重启失效 H 为硬性 S为软性 n 表示设定单个进程最大的打开文件句柄数量
```

下面是实验的程序：

```python
#!/usr/bin/python env
# coding:utf8


import os
import time


time.sleep(10)

def main():
    for i in range(10):
        time.sleep(2)
        a = os.popen('ls')
        a.close()
        os.popen('ls')
        a.close()

        c = open('./test.sh')
        c.close()
        d = open('./test.sh')
        d.close()
        e = open('./test.sh')
        f = open('./test.sh')
        g = open('./test.sh')
        h = open('./test.sh')


main()

print('退出前20s')
time.sleep(20)
```

你可以 删除 c.close() 、d.close() 、或者添加更多。最终得到的结论是：

1. 如果函数退出，文件描述符自动回收，即使没有手动 close 。

2. 使用 popen 执行后确实会返回一个类似的fd(文件描述符)，但是在系统上使用命令查询却看不出增加了，说明其实这个只是一个 Python 内部的对象，并不需要操作系统真正的分配文件描述符。 而既然是一个对象，那么如果不 close， 最终函数执行结束了，也会被垃圾回收给清理掉。

3. 内存回收机制一定不会不回收，否则就要内存泄露了，像 Python Java 这种语言应该不存在这个问题

   

看到了以上结论后，也许会问，那都可以自动回收，那为啥还要设计 close 呢。以下只是我个人的思考：

1. close 设计的原因： 如果你自己不 close， 等 垃圾回收的话，比如你一个函数巨长，最终还没开始垃圾回收， 就已经无法再打开新文件了，因为超过个数了。
2. 手动 close 可以保证及时把写完的内容刷到文件里。
3. 手动 close 可以随时释放资源，提高资源利用率。
4. 要养成 close 的习惯，来避免一些难于找到又奇怪的 bug。



除此之外，执行系统命令还可以用：

`os.system()` : 这个就不会返回一个 fd 了，无法获取命令的输出和返回值

`os.popen()` ： 可以获取到命令执行后的输出

`commands` : 还有这个库，可以同时获得返回值和输出





参考：

[Linux 查看文件句柄数](https://my.oschina.net/dabird/blog/837784)

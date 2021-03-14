---
title: Python文件学习
date: 2017-07-28 00:32:35
tags: [Python]
category: Python
---

f = open("文件名称","w/r/a")  # 打开文件

r 以只读方式打开文件。文件的指针将会在文件的开头。这是默认模式

w 打开一个文件只用于写入。如果文件存在则将其覆盖，如果不存在则创建。

a 打开一个文件用于追加。如果文件已存在，文件指针将会在文件的结尾。也就是说，新的内容会被写在末尾。

<!-- more -->

rb/wb/ab

r+/w+/a+

rb+/wb+/ab+

f.read() 读取文件内容

f.read(一次读取的字节数)

f.write(写入的内容)

f.close()关闭文件流

f.seek(2,0)表示从改变文件指针的位置，文件指针指在开头两个字节处

f.tell()输出文件指针的位置

import os

os.rename("旧文件名","新文件名")

os.remove("文件名")

os.mkdir()创建文件夹

os.rmdir() 删除文件夹

os.getcwd() 获取当前路径

os.chdir("../")改变默认目录 (改成上一层目录)

os.listdir("./") 列出当前目录文件




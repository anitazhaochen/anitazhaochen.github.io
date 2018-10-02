---
title: Mac中sed无法正常保存
date: 2018-09-30
tags: [Mac, sed]
category: Mac

---

今天有一个文件，每次处理之后，发布之前总需要替换一些东西，本来想着写个脚本，但是后来又发现没必要，一行sed命令就可以解决的事情，于是写了写sed



然后发现 sed 的对于一些正则表达式的支持在 Mac 上面不一样。



事情是这样的，我处理完文件之后，把它处理的结果重定向到文件里面，然后我打开文件，发现，其实它是没有改变的，但是如果输出到 stdout 就是命令行，它是修改了的，然后就研究了一会。

[在 Mac 上的 sed 正则表达式问题， 在 Linux 上面工作正常](http://zgserver.com/macsedexpressionlinux.html)



我的解决方法是将原本的 

`➜ sed -i  's/\(^\s*!\[image.*\)\.\.\(.*\)/\1\2/g'  tmp.md > a.md`

\s 替换成空格

`➜ sed -e  's/\(^ *!\[image.*\)\.\.\(.*\)/\1\2/g'  tmp.md > a.md`

然后就可以了。
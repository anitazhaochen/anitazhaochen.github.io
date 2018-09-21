---
title: virtualenv搭建不同版本python环境
date: 2017-06-04 22:34:40
tags: [python, virtualenv]
category: python
---

# 使用virtualenv实现在mac 上多版本python的使用

​      因为mac上装的python版本是2.7的，初学python的时候，想装最新版，卸载了一回，就导致很多东西运不了了，最后又把新装的python3删了，又装回去了2.7版本。

​	学习肯定是直接学最新版本的，然后发现了有一个工具，他不用复杂的配置PATH等东西，然后查了查资料就搞定了，现在mac上需要用2.7版本的python就用2.7版本的，要用3.5版本就用3.5版本的。



下面开始具体配置方法，写下来也避免自己忘记。

<!-- more -->



* 首先安装最新版本的python，然后就有一个文件夹，我电脑上是安装在 当前用户目录下，有个python3的文件夹，里面就是一些python3的东西。

* 然后利用pip 安装 virtualenv

  ~~~
  $ pip install virtualenv
  ~~~

* 安装完成没有出错的话，进行下一步

  ~~~
  $ virtualenv -p /Users/xxx/python3/bin/python3 ENV
  ~~~

  执行完之后，它就会在你执行的那个目录下创建一个 名为ENV的文件夹，里面就是虚拟环境

  其中，-p 后面跟的是你的python3安装的路径，要找到bin下面的python3可执行文件，然后 后面跟的就是你要创建虚拟环境的名字，我这里叫做ENV

* 至此，虚拟环境创建完成，接下来就是激活 环境。



 我这里安装的ENV文件夹里，进去之后有一个bin然后里面有一个 activate 可执行文件

然后执行他就行

~~~
$ source activate
~~~

执行完毕，你会发现在终端前面多了一个ENV标识，说明启动成功了。

此时在终端输入 python 然后就可以看到版本已经变成python3了。

然后你不管是ide还是终端执行.py文件，默认用的都是python3，现在你用pip 安装的一些包也是安装在python3里的，完全不必担心会和python2.7混在一起。

退出的命令是

~~~
$ deactivate
~~~

然后就又回到python以前的版本了。


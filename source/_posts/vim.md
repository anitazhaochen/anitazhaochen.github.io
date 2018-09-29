---
title: mac 安装vundle遇见的一些问题
date: 2017-04-19 12:52:14
tags: [vundle, vim]
category: vim
---


在mac上安装vundle遇到了很多问题，最终还是都解决了。

### 在vim上使用自动的插件管理工具vundle

确保自己的电脑上装有vim后，就可以进行接下来的配置了

<!-- more -->

当时遇到了很多坑， 官网直接写的 修改 .vimrc 当时就懵了，不知道在哪里找那个文件，还好，然后通过查找资料，终于找到了 一个名为																																																																																																												vimrc的文件, 然后修改，系统告诉我那是一个只读文件，无法修改，我就 又郁闷了。

经过重新阅读很多资料之后，决定通过穷举法，一个一个试试， 首先 网上 普遍说要修改自己用户本目录下的 .vimrc文件，但是，可能mac上并没有找到这个文件，所以我就在~下创建了一个文件.vimrc，然后将配置写入，发现不行，然后删除那个文件，在当时安装vundle的.vim目录下，创建了.vimrc 文件，然后同样的方法，还是不行。.......等等，最后终于解决了，下面是 解决的具体方法。



## 安装vundle

[vundle Github官方教程](https://github.com/VundleVim/Vundle.vim)

1.打开终端，输入如下代码

~~~~~~~
$ git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
~~~~~~~

2.执行完后，他会在你的家目录下创建一个 /.vim/bundle/Vundle.vim,在终端输入如下代码切换到家目录：

~~~~~~
$ cd 
~~~~~~

3,既然，没有找到.vimrc文件，那么我们就创建一个，执行如下命令：

~~~~~~
$ vim .vimrc
~~~~~~

然后这时就可以把官网的教程里的配置 复制粘贴进去。保存，然后 进行接下来的工作，但是我在这一点出错了，出现了一些错误：

![](http://i4.buimg.com/567571/1af69155a6b631f1.png)

然后我输入l查看了日志，发现他说某些网址有误，连不上，估计有可能被墙了，但是我也开了vpn呀，估计不是全局模式，这个时候我又开始广泛收集资料了，然后看到了一篇文章[使用vundle进行插件管理（vim笔记二）](http://www.jianshu.com/p/mHUR4e)

直接跳到第4条，看了一下他发文章的时期，是2013年，也比较久远，不过他有一个[GIt](https://github.com/tailang/vimrc/blob/master/.vimrc)一直更新了 配置文件，然后复制里面的内容，到自己本机的.vimrc文件里，再次打开vim

输入

~~~
:PluginInstall
~~~

即可完成安装，就不会出现Not an editor command: PluginInstall 这个错误。 或者出先某些插件无法正确安装的错误。



### 错误要点分析

最后，总结一下，如果出现执行 vim 然后  :PluginInstall 出现Not an editor command: PluginInstall 就一定意味着你的 .vimrc 文件没有配置正确。

如果出现:PluginInstall 可以运行，但是运行后报错，那应该就是网络不好的问题。可以考虑看一下这里的配置[Git](https://github.com/tailang/vimrc/blob/master/.vimrc)


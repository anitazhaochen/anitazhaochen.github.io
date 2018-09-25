---
title: mac使用vim安装youcompleteme(YCM)补全python
date: 2017-11-17 14:38:59
tags: [mac, vim, 插件]
category: Mac
---

[YoCompleteMe](https://github.com/Valloric/YouCompleteMe)

官方强烈建议使用MacVim，如果你不想用MacVim GUI，你可以使用MacVim内置的vim。

使用brew安装了 MacVim，$ brew install macvim
直接下载安装也可以。

<!-- more -->


`mvim -v` 
是默认在iterm中启动，不开GUI

他告诉你，有一种方法可以很快的安装，但是并不是适合所有人。

然后用Vundle安装YCM的方法非常简单，只需要两步。先在.vimrc文件中添加Plugin命令：

Plugin 'Lokaltog/vim-powerline'
2. 
    
 应该写成 
plugin ‘valloric/youcompleteme’

错误写法：
plugin ‘youcompleteme’

然后等待就行了，安装成功会提示，安装错误，自己去git 它到指定的仓库。

我们需要自己去编译它：
  首先安装 cmake  ， 用brew 安装就行，
然后进入安装的目录，运行 
`./install.py —clang-completer`   
成功就行
—clang-completer 是 C家族的那些语言支持，如果不需要，可以省略。

如果不想看到额外的补全时候的文档，可以在vim 中
：set completeopt-=preview
但是这样只是一次性的，需要你自己写到.vimrc 里面进行永久将配置
`set completeopt-=preview'



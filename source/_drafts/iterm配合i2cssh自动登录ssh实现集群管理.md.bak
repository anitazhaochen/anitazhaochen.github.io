---
title: iterm配合i2cssh自动登录ssh实现集群管理
date: 2020-05-25 23:02:21
tags: [iterm, ssh, i2cssh]
category: iterm
---

## i2cssh

### 安装自己的 RUBY

最好不要用 Mac 自带的 ruby 进行安装，会提示无法写入错误，貌似苹果启用了保护功能，即使加上 sudo 也无法写入。

首先第一步： 不适用系统的 ruby ，使用自己安装的 ruby 。

`brew install ruby`

安装完后，注意页面上的提示告诉你执行下面的命令后，才可以更换成你安装的 ruby，否则还是系统默认的。

`  echo 'export PATH="/usr/local/opt/ruby/bin:$PATH"' >> ~/.zshrc`
<!--more -->

这里，我的是 zsh , 其他shell，换个名字即可，如 .bashrc 。这里解释一下就是优先从用户自定义安装软件的地方来找 ruby，所以 需要在 PATH 前面加上路径。

执行完后，不要忘记执行 `source .zshrc` 来刷新配置。

接着可以看一看是否成功了， 执行 `which ruby` 看看是否是在 `/usr/local/` 里面

### 安装i2cssh

安装好 Ruby 后，就可以使用 gem 来安装 i2cssh 了，官方给出两种选择。打开iterm后，点 iterm2 然后 about 查看自己的版本，如果版本低于 2.9 执行 `gem install i2cssh -v 1.16.0` ,否则执行 `gem install i2cssh` 进行安装。

使用说明见官方文档：[GItHubi2cssh](https://github.com/wouterdebie/i2cssh)

安装完后，输入 `i2cssh` 如果提示你命令找不到，则需要修改 PATH。

首先找到 gem 安装 i2cssh 的位置，我的位置是在 `/usr/local/lib/ruby/gems/2.7.0/gems/i2cssh-2.2.0/bin/i2cssh`

我也不是 ruby 开发者，也没深究，因为 ruby 安装在 `/usr/local/opt/ruby/bin/ruby` 这个目录，所以我就在``/usr/local/opt/ruby/` 这个目录执行 `grep -R "i2cssh" ./ `，然后输出一大堆东西，自己看一下大概可以知道在哪里了。我的是在 `/usr/local/lib/ruby/gems/2.7.0/gems/i2cssh-2.2.0/bin/i2cssh` 目录下，所以执行下面的命令，如果你要执行请先找到然后替换下面的路径。

`  echo 'export PATH="/usr/local/lib/ruby/gems/2.7.0/gems/i2cssh-2.2.0/bin/i2cssh:$PATH"' >> ~/.zshrc`

再次 `source .zshrc` 应该就可以了。

### 问题说明

对于初次使用 i2cssh 的我，因为 i2cssh 的文档实在太少了，所以并不知道该如何去使用。把我摸索出来的东西给需要的人说一下：

首先： 你不需要设置 iterm， 直接在 `.ssh/config` 中先设置好你的服务器，最好把配置写完整，其中一个服务器如下：

```shell
Host ubuntu
HostName 1.2.3.4
Port 32222
User root
IdentityFile ~/.ssh/id_rsa
```

其中 `IdentityFile` 这一项最好写上。

然后直接在 iterm 中执行 `i2cssh host1 host2 xxx xxx ` 他就会自动弹出窗口。

在我这里有一个问题，就是如果 i2cssh 命令后面的主机数小于2的话，就会报错

```shell
ERROR: unknown cluster ["linux"]. Check your /Users/Myname/.i2csshrc
```



### iterm 多个窗口同时输入

在刚才通过 i2cssh 打开的窗口中，随便选一个窗口，然后 `command + shift + i` 就可以开启同时输入了。

比如说，我有几十台服务器，然后我需要查日志，但是我并不知道某次请求会打在哪一台机器上， 这个时候，我就需要使用 i2cssh 来把这些服务器全部连上， 然后因为每台服务器运行的程序位置都相同，所以再执行 `tail -f xxx.log` 同时监听，然后在一个一个看就可以了。


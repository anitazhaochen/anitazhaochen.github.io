---
title: mosh的使用方法
date: 2017-11-17 18:40:30
tags: [mosh, ssh]
category: linux
---

ssh连接电脑，在网络不好的时候，总是会有延迟，而且有的时候延迟直接到达输入字符半天才回显，有的时候体验极差，ssh利用的是tcp协议，自然没有udp快。

注意
Mosh 目前不支持端口映射或代理功能，也不能使用 Mosh 来复制文件或挂载远程目录。您仍然需要 SSH 来完成这些事情。

<!-- more -->

有一个Mosh的连接工具，可能会替代ssh，
https://mosh.org/  Mosh官网
说了很多特性，可以自己去看，英文网站
具体有以下优点：
1.可以延迟更低，ssh需要等待服务器响应后，才显示您输入的内容。而mosh会马上显示您的输入，编辑，删除登内容。
2.在网络差的时候没有ssh容易断线，常常一个连接能保持很久，即使你合上笔记本，打开笔记本连接依旧在。

3.对于移动网络，常常更换ip的情况下也能保持连接，断网后，mosh将会在新网可用的时候自动连接服务器，
等等，有兴趣了解的可以自己去官方网站看，

因为这方面的安装还不多，在我查阅了中文资料之后，依旧一头雾水，或者资料太少，无法多个比对，理解作者真正意图，鉴于英文文档，自然就有抵触的情绪，实在无奈，又深爱计算机，所以，还是读一遍吧。

下面开始说正事，我尽量达到每一步都为读者考虑的心情。

首先，像这样的服务，肯定都有服务端和客户端，
服务端是开启服务，供客户端连接的，
而客户端是连接服务端的工具。

我想配置一台服务器，或者是我自己的电脑，我该怎么做才能像ssh一样连接到它呢。

首先，我们先从ssh讲起，这是基础。

一般linux版本的系统都装有ssh服务，只是没有开启罢了，所以，我们先服务启动,因为本文的重点是mosh，所以ssh 已经有很多资料了，不会的同学，可以google一下，亦或百度一下，自行搞定吧，不管什么系统，应该都有方法。

当我们ssh配置成功之后，并且成功连接了 服务器之后，下面就可以进行mosh的配置了。

当时我看到mosh的这些特性，在想为什么它不会断呢，
难道中间接了一个中间服务器？
我身处学校内网，服务器没有公网ip，那么如果这样的话，我岂不是我的内网的电脑就无法连接到我的内网服务器了嘛， 并且，如果接一个中间人的话，安全也是一个问题，能有人信任然后用它吗？
带着种种疑问，查资料，也查不到，只能看官网文档，
又有一个疑问，我的服务器有没有配置过防火墙，我的ip需不需要转发，我的udp端口用不用手动开放等等，因为知识还不太全面，总是带着种种疑问，没办法，只能试一试了

首先，假设我的疑问全不在，它就像ssh一样，可以内网连接，官网说mosh的操作其实和ssh 非常相似。

1.在服务器上安装mosh，具体安装方法有 apt-get install mosh ，等等，在官网上都可以找到，安装应该不成为问题。首先不必考虑服务端、客户端的问题，其实它是默认都装了的。
mosh 是客户端， mosh-server是服务端。
用不用自己开启端口啊，什么的东西呢？
自己折腾了一阵子，其实都不是这些原因，而是工具不会使用造成的连接不了， 我用ps查看服务端怎么一会就自己没了呢，官网说没人连接服务端会自动quit，我想服务端没运行，那还连个什么呀！！
然后又想，官网不说说mosh事基于ssh嘛，可不能只要ssh开启成功就可以自动转接成mosh呢？
抱着疑问，看了看FAQ，做了一个连接试验一下：
下面把这个里程碑式的实验拿出来，是它解决了我一些疑惑！！！

Q: How do I run the mosh client and server separately?
If the mosh wrapper script isn't working for you, you can try running the mosh-client and mosh-server programs separately to form a connection. This can be a useful debugging technique.
1. Log in to the remote host, and run mosh-server.
It will give output like:
$ mosh-server 

MOSH CONNECT 60004 4NeCCgvZFe2RnPgrcU1PQw

mosh-server (mosh 1.1.3)
Copyright 2012 Keith Winstein <mosh-devel@mit.edu>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

[mosh-server detached, pid = 30261]

2. On the local host, run:
$ MOSH_KEY=key mosh-client remote-IP remote-PORT
where "key" is the 22-byte string printed by mosh-server (in this example, "4NeCCgvZFe2RnPgrcU1PQw"), "remote-PORT" is the port number given by the server (60004 in this case), and "remote-IP" is the IP address of the server. You can look up the server's IP address with "host remotehost".
3. If all goes well, you should have a working Mosh connection. Information about where the process fails can help us debug why Mosh isn't working for you.

这是原文，
1.首先在服务器上运行 mosh-server
然后会出现一大堆的东西，这些东西有些将可以为接下来的连接做为资源的。
2.在客户机上运行这段代码
MOSH_KEY=key mosh-client remote-IP remote-PORT

其中，key 是服务端给的4NeCCgvZFe2RnPgrcU1PQw
remote-IP 是你的服务器的ip地址，remote-PORT 是端口号，服务器给了是 60004  然后要快，因为过一会就掉了吧，反正我是第一次没成功，立马就想到是速度的问题，会不会服务器没人连接又自动结束了。然后又来了第二次，这次信息写的很快，一个回车，激动人心的时刻到了，连接成功了。
这一次的成功连接打消了几个大问题：
1.mosh在内网是可以使用的
2.mosh是不存在中间人的
3.mosh和ssh基本是一样的，只是性能不一样，所以我选择用mosh。

我弄计算机的时候，其实最怕的不是它的配置有多难，而是我的想法能不能实现，它支不支持这样的操作，如果因为没有理解好文档的意思，最后做了一个根本无法实现的配置，那将是徒劳，而且一路失败，很难受的， 只要别人可以实现，那么我也可以和他一样，查资料，看文档来实现，我不需要一个人遇到了点问题就去问他，而是只要告诉我可以做到，接下来，所有的事情，都是google去吧。

好了，回到正题上，mosh说它的操作基本和ssh一样，那么就很简单了。

我们ssh每次都输入密码很麻烦，可以查一下，如何生成一个公钥和一个私钥，然后每次就不用输入一大堆东西了。
在ssh上，我配置好了所有
然后输入
ssh kali 就可以直接连接到我的主机，在mosh中，只要你的ssh连接没问题，那么
mosh kali 这条命令也应该是没问题的，还有一些其他的命令，也都类似ssh，就不多说了。



看过的mosh文章;https://meiriyitie.com/2015/05/28/mosh/

http://itindex.net/detail/54505-ssh-%E5%B7%A5%E5%85%B7-mosh
结合一下





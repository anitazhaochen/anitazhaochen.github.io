---
title: 花生壳内网穿透+mosh
date: 2017-11-17 18:45:22
tags: [内网穿透, mosh]
category: linux
---

# mosh: Nothing received from server on UDP port 60001.[to quit: Ctrl-^.]

我在学校，用手机端的juicessh连接服务器，就会出现上面的这段话。
因为我是用花生壳内网穿透的，所以，就可以用手机的4G网连接。

本来是想4G不太稳定，ssh肯定掉，就想着用mosh连接，可是连接上了，却不能用。

研究了一下mosh的官方文档，似乎知道了答案。

因为mosh会基于ssh连接后，进行udp通信，因为花生壳只给了你一个端口，所以mosh就无法建立udp连接，主要是没有权限让花生壳给端口，所以，我们就收不到服务器那边的数据，而用ssh， 用4g连却可以勉强可以使用。




---
title: authbind在docker中使用
date: 2018-08-04 16:47:56
tags: [linux, docker, authbind]
category: linux
---

# Linux 普通用户使用authbind绑定特权端口

在Linux上普通用户无法绑定1024以下的端口，不过总是会碰到一些特殊情况，比如遇到最多的就是普通用户程序要监听80端口，有很多方法可以实现，之前常用的就是使用sudo给予普通用户一定的权限，不过总感觉sudo控制起来不是很方便，最近发现ubuntu下面有一款小程序authbind可以实现该功能，且配置起来也方便。　　authbind允许程序不使用root权限来绑定系统1024以下的特权端口，你必须使程序调用authbind，authbind会调用一些环境变量，来允许你的程序绑定在特权端口。　　Ubuntu 12.04安装authbind　　apt-get install authbind　　怎样使用authbind呢？通过配置文件区域来使用了，默认的配置文件区域在/etc/authbind目录下，里面有三个目录：byport、byaddr、byuid。　　假如我们有个test账号，想运行一个程序绑定80端口　　在byport目录下建立80文件：/etc/authbind/byport/80即#touch /etc/authbind/byport/80，设置test账户有80文件的使用权限，如果80文件可以被test访问，则绑定就是成功的，否则绑定就是失败的。　　具体操作：　　chmod 755 /etc/authbind/port/80; chown test /etc/authbind/port/80　　在你要启动的命令前加上authbind --deep命令即可。　　我们也可以直接在地址上绑定端口，在byaddr下建立ip:port文件，测试方法如上。也可以在byuid目录下建立uid文件，只要你的test账号可以访问，否则绑定失败

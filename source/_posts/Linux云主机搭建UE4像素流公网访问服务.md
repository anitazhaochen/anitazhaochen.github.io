---
title: Linux云主机搭建UE4像素流公网访问服务
date: 2021-03-11 19:28:43
tags: [UE4, 像素流, TURN, STUN]
category: 像素流
---

## 前言：

由于 UE4 像素流官方提供的服务基本都需要在 Windows 环境上面运行。考虑到具备高性能 GPU 的服务器性价比又太低，正好手上有台 Windows 机器，但是又没有公网IP，如何让其支持公网访问成了一个问题。

如果能利用上现有的 Linux 公网服务器及手中的 Windows 就最好不过了。

1. 本地内网 Windows 机器跑像素流及“信令和Web服务器”
2. 使用 Linux 搭建支持信令服务器的网络打洞/中继服务及Web服务器的转发服务，以支持外网访问。

> 信令和Web服务器： 这个词是官方的叫法，其实它实际上只表示一个组件，这个组件同时包含了信令服务器和Web服务器，他们分别有不同的用途，我们也需要分别对其进行网络穿透支持。

需要解决的问题：


1. UE4 像素流使用到了 [WebRTC](https://zh.wikipedia.org/wiki/WebRTC)（网页即时通信），在移动运营商的网络中如4G网络，一般是不支持用户通过 WebRTC 协议直接与服务器建立连接，需要自建 STUN/TURN 服务，通过中继服务器进行网络中继解决信令服务器的网络问题及在内网访问问题。
3. 信令和Web服务器，官方只提供了 Windows 版本，即无法部署到 Linux 服务器。
5. 内网穿透解决 Web服务器公网访问问题


## 搭建教程

<!--more -->

[创建主机和网络连接指南](https://docs.unrealengine.com/zh-CN/SharingAndReleasing/PixelStreaming/Hosting/index.html) 像素流官方文档，通过查阅文档可以了解其大概的网络架构，由于其文档写的不是很具体，所以其中的参数还需要自己去多多尝试。

1. 内网的一台高性能的 Windows 机器上，包体就在这台机器上面跑。

2. 信令和Web服务器官方直接提供的就是 Windows 版本，所以决定将其也放置在内网的这台高性能 Windows 上面运行，由此引发的网络问题后续解决。（如有 Windows 云主机，部署相对容易）

3. 自己搭建 STUN/TURN 服务器， 在 4G 无线运营商网络下，STUN 一般也是无法穿透的，所以需要使用 TURN 当做中继服务进行中转，对带宽有一定要求。这里我们选择开源服务器 [coturn](https://github.com/coturn/coturn) 进行搭建。

 ```shell
 apt install build-essential
 apt install openssl libssl-dev make
 
 wget https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz
 tar xf libevent-2.1.12-stable.tar.gz
 cd libevent-2.1.12-stable
 ./configure
 make && make install
 
 # 接下来选择数据库，coturn 默认选择 sqllite 数据库
 ## 选择 sqllite 数据库 （如果机器上已有，就不要安装了）
 apt-get install sqlite libsqlite3-dev
 
 # 下载 coturn 源码，并编译安装
 
 wget https://github.com/coturn/coturn/archive/4.5.2.zip
 tar xf 4.5.2.zip
 cd coturn-4.5.2
 ./configure
 make && make install
 
 # 报错解决方法： ERROR: pkg-config not found 
 # 执行 apt install pkg-config
 
 
 # 看看上面有没有报错，数据库是否选择正确，至此安装完成
 
 # 创建用户并配置 coturn
 
 turnadmin -a -u test -p test -r test
 #  创建用户名为 test 密码为 test ，同时 realm(这个参数等下配置文件中需要一致) 为 test
 
 cp /usr/local/etc/turnserver.conf.default /usr/local/etc/turnserver.conf
 vim /usr/local/etc/turnserver.conf
 # 直接在最上面把以下配置粘贴进去， 请看注释进行微调：
 listening-port=3478 #监听端口
 listening-device=eth0 #监听的网卡， ifconfig 查看
 external-ip=1,2,3,4 # 服务器的公网ip
 user=test:test # 用户名:密码
 realm=test #一般与 turnadmin 创建用户时指定的 realm 一致
 
 ```

 配置完成后先前台运行服务器查看有无报错：

 ```shell
 turnserver -a -f -v -r test
 ```

 验证监听是否成功：

 ```shell
 lsof -i:3478
 ```

 如果有输出，则监听成功。

 通过在线检测ice服务是否正常：

 [webrtc-官网检测服务](https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/)

```
STUN or TURN URI: turn:ip:port
TURN username: test
TURN password: test

选择 Add Server

STUN or TURN URI: stun:ip:port
TURN username: 
TURN password: 

选择 Add Server

然后点击  Gather candidates

稍等片刻，如果在 Protocol Address 一栏看到你的公网IP地址，说明服务搭建成功。


```

以上 STUN/TURN 服务搭建成功后，我们开始搭建像素流送服务。

1. 首先确保局域网跑通没问题后

2. 修改"信令和WEB服务器"的配置，在其配置中加入我们的 STUN/TURN 服务地址

   具体操作方法：

   1. 打开 `\Engine\Source\Programs\PixeLStreaming\WebServers\SignallingWebServer` 编辑里面的 `Start_AWS_WithTURN_SignallingServer` 文件， 将 $PublicIp 更改为 STUN/TURN 服务器的公网 IP，然后找到 `$peerConnectionOptions` 这一行，修改其中的 username 及 credential 为你自己设置的用户名和密码，在我这都改为 test 。然后保存。

   2. 在局域网运行的时候，我们启动的是 run.bat 文件， 现在我们改为启动 runAWS_WithTURN.bat 这个文件。

      至此，基本搭建完成。 然后我们进行这一步的测试，保证服务搭建的没问题，我们在内网进行访问，地址还是和我们在局域网的地址一样，看看能否访问，如果可以访问，则证明这条链路是没有问题的，如果不能访问，首先查看 STUN/TURN 日志，看看有没有接收到连接，如果日志没有任何连接之类的信息输出，说明我们的内网 Widnwos 并没有连接上 STUN/TURN 服务，检查是否自己刚才修改 Windows 上的配置文件哪里修改错了，或者无意间破坏了它的格式。

   3. 如果第二步测试没有问题，并且 STUN/TURN 服务器也有日志输出，我们继续下一步的工作，前面提到 “信令服务器” 和 “Web服务器” 在这里，它是一体的，我们部署在 Windows 上，其中 “信令服务器” 的网络问题我们已经解决，就是使用的 STUN/TURN 服务进行中继或者“打洞” 实现。我们接下来实现 Web服务器的外网访问，这个 Web 服务器的功能仅仅是为客户端提供 WebRTC 连接的js文件。以下四种解决方法供参考：

      1. 利用 ssh 命令自带的代理服务将端口映射到服务器上的某个端口上，由于很少在 windows上面操作，所以没有使用这个方法，这个方法其实一条命令就能解决，缺点是不稳定，ssh 经常会自动断开连接。
      2. 使用 Nginx 反向代理功能，前提是服务器可以访问到内网这台 Windows 主机，测试方法，在服务器上面执行 ping windows 的内网ip ， 可以在 windows 的 cmd 中输入 ipconfig 命令查看内网 IP， 如果可以 ping 通，就可以配置 Nginx 反向代理来提供 Web 服务器访问。
      3. （目前使用的方法）使用开源工具 FRP 进行内网穿透，部署方法参考[Frp 官网文档](https://github.com/fatedier/frp) ，需要在 Windows 部署 frpc 客户端及服务端部署 frps 服务端。
   4. 将必要的客户端文件提取出来，将其部署到公网主机上。
   
   全部部署完成后，打开4G网，访问 公网ip:frp穿透到服务器的端口  看看能否访问到 web 页面，如果连页面都访问不到，请检查云主机的端口是否打开。
   
   至此，完成所有部署。



2021-3-17 更新：

​	  今天再次测试的时候，发现 Chrome 浏览器报错了 `failed to parse answers sdp` ，期初以为我改了哪个配置导致的，最终换了个浏览器就好了，可能和我更新了最新版的 Chrome 浏览器有关吧。



2021-3-26更新：

[参考某位知乎大神](https://zhuanlan.zhihu.com/p/357335311) 解决 Chrome 浏览器访问问题。



注意： coturn 编译安装的时候，要注意看清 openssl 版本，使用  `openssl version` 查看，推荐 openssl 1.1.0 以上版本进行安装，如果后面启动服务器说不支持如下的，再考虑升级 openssl 版本。

```

==== Show him the instruments, Practical Frost: ====

0: : TLS supported
0: : DTLS supported
0: : DTLS 1.2 is not supported
0: : TURN/STUN ALPN is not supported
0: : Third-party authorization (oAuth) supported
0: : GCM (AEAD) supported
0: : OpenSSL compile-time version: OpenSSL 1.0.1t  3 May 2016 (0x1000114f)
0: :
```

启动 turnserver 后，看下有没有报错，其中上面说了几个不支持，当时端口绑定不上，就是这个问题造成的，解决方法时升级 openssl 版本，至少升级到 1.1.0 以上版本，我用的是最新的1.1.1 版本。

我原本的 openssl 是这个版本：

```shell
root@ip-10-23-93-138:~/coturn-4.5.2# openssl version
OpenSSL 1.0.1f 6 Jan 2014
```

出现这个问题可以先忽略他：

```shell
root@ip-10-23-93-138:~/coturn-4.5.2#  turnadmin -a -u test -p test -r test
0: : SQLite connection was closed.
0: : log file opened: /var/log/turn_22804_2021-03-26.log
```

这个版本是可以编译成功 coturn 的，但是后面启动的时候就监听不到端口信息，如下：

```shell
root@ip-10-23-93-138:~/coturn-4.5.2# turnserver
0: : WARNING: Cannot find config file: turnserver.conf. Default and command-line settings will be used.
0: : log file opened: /var/log/turn_22815_2021-03-26.log
0: : WARNING: Cannot find config file: turnserver.conf. Default and command-line settings will be used.
0: : WARNING: Cannot find config file: turnserver.conf. Default and command-line settings will be used.
0: :
RFC 3489/5389/5766/5780/6062/6156 STUN/TURN Server
Version Coturn-4.5.2 'dan Eider'
0: :
Max number of open files/sockets allowed for this process: 4096
0: :
Due to the open files/sockets limitation,
max supported number of TURN Sessions possible is: 2000 (approximately)
0: :

==== Show him the instruments, Practical Frost: ====

0: : TLS supported  
0: : DTLS supported
0: : DTLS 1.2 is not supported  # 重点看这里
0: : TURN/STUN ALPN is not supported  # 重点看这里
0: : Third-party authorization (oAuth) supported
0: : GCM (AEAD) supported
0: : OpenSSL compile-time version: OpenSSL 1.0.1f 6 Jan 2014 (0x1000106f)
0: :
0: : SQLite supported, default database location is /usr/local/var/db/turndb
0: : Redis is not supported
0: : PostgreSQL is not supported
0: : MySQL is not supported
0: : MongoDB is not supported
0: :
0: : Default Net Engine version: 3 (UDP thread per CPU core)

=====================================================

0: : Domain name:
0: : Default realm:
0: : ERROR:
CONFIG ERROR: Empty cli-password, and so telnet cli interface is disabled! Please set a non empty cli-password!
0: : WARNING: cannot find certificate file: turn_server_cert.pem (1)
0: : WARNING: cannot start TLS and DTLS listeners because certificate file is not set properly
0: : WARNING: cannot find private key file: turn_server_pkey.pem (1)
0: : WARNING: cannot start TLS and DTLS listeners because private key file is not set properly
0: : NO EXPLICIT LISTENER ADDRESS(ES) ARE CONFIGURED
0: : ===========Discovering listener addresses: =========
0: : Listener address to use: 127.0.0.1
0: : Listener address to use: 10.23.93.138
0: : Listener address to use: 172.17.0.1
0: : Listener address to use: ::1
0: : =====================================================
0: : Total: 2 'real' addresses discovered
0: : =====================================================
0: : NO EXPLICIT RELAY ADDRESS(ES) ARE CONFIGURED
0: : ===========Discovering relay addresses: =============
0: : Relay address to use: 10.23.93.138
0: : Relay address to use: 172.17.0.1
0: : Relay address to use: ::1
0: : =====================================================
0: : Total: 3 relay addresses discovered
0: : =====================================================
0: : pid file created: /var/run/turnserver.pid
0: : IO method (main listener thread): epoll (with changelist)

```

避免走弯路，有些问题不需要去管它，比如 cli-password 问题，重点的我在上面已经标注了。

官网下载地址：[openssl-1.1.0l.tar.gz](https://ftp.openssl.org/source/old/1.1.0/openssl-1.1.0l.tar.gz) 

```shell
wget https://ftp.openssl.org/source/old/1.1.0/openssl-1.1.0l.tar.gz
tar xf openssl-1.1.0l.tar.gz
cd openssl-1.1.0l
./config && make && make install
```

我试了 openssl-1.1.0I.tar.gz  编译安装完成后，openssl version 报了错误如下：

```
root@ip-10-23-93-138:~/openssl-1.1.1k# openssl version
openssl: error while loading shared libraries: libssl.so.1.1: cannot open shared object file: No such file or directory

解决方法： 
mkdir /usr/lib64
ln -s /usr/local/lib64/libssl.so.1.1 /usr/lib64/libssl.so.1.1
ln -s /usr/local/lib64/libcrypto.so.1.1 /usr/lib64/libcrypto.so.1.1
echo "/usr/local/lib64/" >> /etc/ld.so.conf
ldconfig
```

升级完成 openssl 后，可能需要重新编译 coturn ，进入文件夹同样的操作 

`./configure && make && make install` 再来一遍就好了。

```
root@ip-10-23-93-138:~/coturn-4.5.2#  turnserver -a -f -v -r test
0: : Config file found: /usr/local/etc/turnserver.conf
0: : log file opened: /var/log/turn_26454_2021-03-26.log
0: : Config file found: /usr/local/etc/turnserver.conf
0: :
RFC 3489/5389/5766/5780/6062/6156 STUN/TURN Server
Version Coturn-4.5.2 'dan Eider'
0: :
Max number of open files/sockets allowed for this process: 4096
0: :
Due to the open files/sockets limitation,
max supported number of TURN Sessions possible is: 2000 (approximately)
0: :

==== Show him the instruments, Practical Frost: ====

0: : TLS supported
0: : DTLS supported
0: : DTLS 1.2 supported
0: : TURN/STUN ALPN supported
0: : Third-party authorization (oAuth) supported
0: : GCM (AEAD) supported
0: : OpenSSL compile-time version: OpenSSL 1.1.1k  25 Mar 2021 (0x101010bf)
0: :
0: : SQLite supported, default database location is /usr/local/var/db/turndb
0: : Redis is not supported
0: : PostgreSQL is not supported
0: : MySQL is not supported
0: : MongoDB is not supported
0: :
0: : Default Net Engine version: 3 (UDP thread per CPU core)

=====================================================

0: : Domain name:
0: : Default realm: test
0: : ERROR:
CONFIG ERROR: Empty cli-password, and so telnet cli interface is disabled! Please set a non empty cli-password!
0: : WARNING: cannot find certificate file: turn_server_cert.pem (1)
0: : WARNING: cannot start TLS and DTLS listeners because certificate file is not set properly
0: : WARNING: cannot find private key file: turn_server_pkey.pem (1)
0: : WARNING: cannot start TLS and DTLS listeners because private key file is not set properly
0: : NO EXPLICIT LISTENER ADDRESS(ES) ARE CONFIGURED
0: : ===========Discovering listener addresses: =========
0: : Listener address to use: 127.0.0.1
0: : Listener address to use: 10.23.93.138
0: : Listener address to use: 172.17.0.1
0: : Listener address to use: ::1
0: : =====================================================
0: : Total: 2 'real' addresses discovered
0: : =====================================================
0: : NO EXPLICIT RELAY ADDRESS(ES) ARE CONFIGURED
0: : ===========Discovering relay addresses: =============
0: : Relay address to use: 10.23.93.138
0: : Relay address to use: 172.17.0.1
0: : Relay address to use: ::1
0: : =====================================================
0: : Total: 3 relay addresses discovered
0: : =====================================================
0: : pid file created: /var/run/turnserver.pid
0: : IO method (main listener thread): epoll (with changelist)
0: : WARNING: I cannot support STUN CHANGE_REQUEST functionality because only one IP address is provided
0: : Wait for relay ports initialization...
0: :   relay 10.23.93.138 initialization...
0: :   relay 10.23.93.138 initialization done
0: :   relay 172.17.0.1 initialization...
0: :   relay 172.17.0.1 initialization done
0: :   relay ::1 initialization...
0: :   relay ::1 initialization done
0: : Relay ports initialization done
0: : IO method (general relay thread): epoll (with changelist)
0: : turn server id=1 created
0: : IO method (general relay thread): epoll (with changelist)
0: : turn server id=0 created
0: : IPv4. UDP listener opened on: 127.0.0.1:3478
0: : IPv4. UDP listener opened on: 10.23.93.138:3478
0: : IPv4. UDP listener opened on: 172.17.0.1:3478
0: : IPv6. UDP listener opened on: ::1:3478
0: : Total General servers: 2
0: : IO method (auth thread): epoll (with changelist)
0: : IO method (auth thread): epoll (with changelist)
0: : IO method (admin thread): epoll (with changelist)
0: : SQLite DB connection success: /usr/local/var/db/turndb
0: : IPv4. SCTP listener opened on : 127.0.0.1:3478
0: : IPv4. TCP listener opened on : 127.0.0.1:3478
0: : IPv4. SCTP listener opened on : 10.23.93.138:3478
0: : IPv4. TCP listener opened on : 10.23.93.138:3478
0: : IPv4. SCTP listener opened on : 172.17.0.1:3478
0: : IPv4. TCP listener opened on : 172.17.0.1:3478
0: : IPv6. SCTP listener opened on : ::1:3478
0: : IPv6. TCP listener opened on : ::1:3478
0: : IPv4. TCP listener opened on : 127.0.0.1:3478
0: : IPv4. TCP listener opened on : 10.23.93.138:3478
0: : IPv4. TCP listener opened on : 172.17.0.1:3478
0: : IPv6. TCP listener opened on : ::1:3478
```

成功运行输出的日志。


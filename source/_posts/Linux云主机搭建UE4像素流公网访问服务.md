---
title: Linux云主机搭建UE4像素流公网访问服务
tags: [像素流, UE4, 网络]
category: 像素流
date: 2021-03-11
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

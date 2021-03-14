---
title: Linux双网口设置桥接让其他机器连接
date: 2021-03-13 23:36:09
tags: [Linux, Bridge]
category: Linux
---

家里需要连接有线网络的设备越来越多了，三台 Linux 服务器，一台树莓派设备，但是路由器上面只有三个网口，如果再买一台路由器走桥接又得多增加一个设备，多一个耗电设备，还好，其中有台 Linux 主机有两个网口，就想着应该可以设置桥接，路由器连接这台服务器，然后这台服务器的另一个网口给树莓派使用。

## 流程

* 安装 `brctl` 工具

  `sudo apt install bridge-utils`

* 使用 `brctl` 工具创建网桥

  `sudo brctl addbr br0`

* 将两个网口都添加到网桥上，我这里的网卡名并不是 `eth0、eth1` 而是 `enp1s0 和 enp2s0` ，在执行下面的命令的时候确认好你的网口名，可以通过 `ifconfig` 命令查看。
<!--more -->

  `sudo brctl addif br0 enp1s0 enp2s0`

  > tips：一开我认为我只需要其中的一个网口桥接，另一个网口和以前一样使用，所以就只添加一个接口到网桥上了，经过几次测试，发现这种方法不可行，必须要把两个网口都添加到网桥上面才可以。

* 打开 IP 转发

  `sudo vim /etc/sysctl.conf` 

  改 `net.ipv4.ip_forward=1`  ，并且将开头的注释符 “#” 去掉。

  `sudo sysctl -p /etc/sysctl.conf` 

  使其立即生效。

* 最后重启下网络，另一个网口应该就可以正常获取到路由器分配的 IP 了。

  `sudo service network-manager restart`

> 其实也可以通过 Ubuntu 的图形界面进行设置的，重点是要把两个网卡都添加到桥接里就可以了。



最后附一张家里设备的图

![WechatIMG399](/images/WechatIMG399.jpeg)


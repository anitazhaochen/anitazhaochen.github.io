---
title: 使用Netatalk在Linux上面搭建时间机器备份
date: 2021-03-13 22:04:57
tags: [MacOS, Time Machine, Netatalk]
category: MacOS
---

最近本来是准备在黑群晖上面创建一个盘拿来做苹果电脑的 Time Machine 备份的，设置好了后，发现网速极慢，猜想可能是由于我 SSH 上去改了网络配置的原因。这样的事情已经发生了不止两三次了，有几次系统直接崩了，实在是难受，并且慢慢就失去了黑群晖的兴趣，系统偶尔不太稳定，自己的需求大多数时候必须要手动 SSH 上去改配置才能实现。思来想去，我为什么不直接装一台 Linux 呢，说干就干，下了 Ubuntu 最新的 20.xx 版本，先刷入 U 盘，然后改 Bios，因为我这个是蜗牛星际主机，不改 Bios 原来的设置可能会导致开机引导不识别硬盘，然后就是装系统了。

<!-- more -->

## Netatalk

安装完系统后，就开始装 Nettalk 了，安装这个软件很简单，一条命令：

`sudo apt install nettalk -y `

现在安装的应该都是 3.x 版本，配置和网络上大多数的教程都不一样。[Netatakl 官方文档](https://wiki.archlinux.org/index.php/Netatalk_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)) 

然后就开始配置，Netatlk 3.x 只使用一个配置文件 `/etc/afp.conf` :
<!--more -->

```

[Global]
 mimic model = TimeCapsule6,106
 log level = default:warn
 log file = /var/log/afpd.log
 hosts allow = 192.168.1.0/16

[Homes]
 basedir regex = /home

[TimeMachine]
 path = /mnt/timemachine
 valid users = tmuser
 time machine = yes

[Shared Media]
 path = /srv/share/media
 valid users = joe sam
```

并且确保 `avahi` 处于运行状态：

`systemctl status avahi-daemon.service` 查看 `avahi` 运行状态。

## 配置部分

官方给出的配置示例有时候并没能完全满足我们的需求，在这个时候，可以通过已有的经验对其配置进行解读。

* Global

  这个部分主要就是对全局进行配置，具体有哪些参数可以配置可以参考官方文档

* 其他

  除了 Global 配置外，其他的配置只要遵循格式规范就可以了，比如现在我想配置一个时间机器的备份功能，配置如下

  ```
  [ZC Time Machine Volume]
  path = /media/zc_mac
  time machine = yes
  ```

  第一行中括号里面的是名称，当你在 Mac 上面连接后，就会显示上面的名称

  第二行是你的数据备份储存的目录

  第三行是告诉 Netatalk 这个目录是当时间机器备份目录来用的

  以上三行配置好后，在 Mac 上面就可以看到了。前提是你得保证在你的 Mac 上使用 Linux 上面的账户名和密码来连接，并且保证此账户有你配置的这个目录的读取和写入权限。

* 我想再增加一个位置给另一台Mac使用

  其实，如果你想再增加一个位置，这里我建议你先创建一个新的用户账户，然后再跟上面一样，取一个新的名字，使用一个新的目录。

  `useradd -m xiaoming`  # 添加 xiaoming 用户

  `passwd xiaoming`  # 给小明用户设置密码

  然后 创建/挂载 目录如：

  `mkdir -p /media/xiaoming_time_machine` 

  并且修改权限，保证 xiaoming 用户可以访问：

  `chown -R xiaoming:xiaoming /media/xiaoming`

  然后，另一台电脑连接的时候使用 xiaoming 的账户名和密码即可。Netatlk 只会对你显示你当前账户有权限的目录，这样在你备份的时候就只有 1 个目录可选，就不存在交叉感染的危险。

  > 连接方法： 打开 Finder, 左上角菜单栏点击 前往 --> 连接服务器 --> 输入地址如  `afp://192.168.123.2/` 然后点击连接，会提示让你输入用户名和密码，输入你在 Linux 上面创建好的账号和密码即可。 

* 再增加一个目录当做存储盘来用

  操作还是跟上面是一样的，只不过你需要把配置中的 `time machine=yes` 这行去掉。

  还需要注意一件事情就是权限问题，如果你都配置好了，但是发现连接上服务后，这个文件夹并没有出现，可能是权限的问题，可以对一个文件加加多个用户组权限，或者加多个用户权限都可以的。



## Mac 备份非常慢

如果你的 Mac 是第一次在这个上面进行备份，第一次备份一般都很慢，可以调节参数的方式将其调节为全速进行备份，记得备份完后将其调整回来，否则可能会导致你的电脑在正常使用的时候由于同时在备份导致卡顿。

打开终端，执行如下命令开启全速备份：

`sudo sysctl debug.lowpri_throttle_enabled=0`

关闭全速备份：

`sudo sysctl debug.lowpri_throttle_enabled=1`



参考：

[Mac 时间机器备份太慢的解决方法](https://www.jifu.io/posts/4147446761/)


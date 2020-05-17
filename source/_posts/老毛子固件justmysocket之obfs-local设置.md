---
title: 老毛子固件justmysocket之obfs-local设置
date: 2020-05-17 01:26:57
tags: [ss, 老毛子, padavan]
category: openwrt
---

## 关于路由器

最近小米 AC2100 终于可以刷机了。就在前几天听说可以刷机了，立马就刷了老毛子系统。之前是使用 LEDE 软路由进行一些科学设置的，但是 LEDE 是安装在群辉虚拟机上，每次群辉出现一些异常bug的时候，就需要重启，随之网络也断了。在试用了 LEDE 软路由之后，发现其中一些软件已经没有人维护了，根本用不了，还有一些软件如 KOOLDNS， bug 不断，要不然就是不更新ip，要不然就是把ip解析到 127.0.0.1 。

基于小米 AC2100 可以刷机后， 果断放弃了 LEDE 。但是在 LEDE 上面，科学体验还是可以的，就是不支持自动故障切换节点功能，比如走 obfs 的节点，被封了后，每次只能手动上去更改混淆参数。

换了 老毛子 之后，发现自动故障切换节点功能是有了，但是基于它的设置界面及形式，搞得我晕头转向。最后不得不使用穷举法，一个一个试，看看哪一种参数可以成功访问 obfs。这里特别记录一下。

## 页面配置

在页面上建议，直接点击飞机，然后添加节点那里输入如下参数

`  -O origin -o plain --plugin obfs-local --plugin-opts "obfs=tls;obfs-host=www.bing.com"`
<!--more -->

然后填写节点信息，点加号就可以了。

我也不知道是因为我在节点配置配置对了，还是转到详情配置配置对了。

所以，如果上面还不起效的话，或者 通过下一节的 检查 obfs 不过关的话，再去详情里配置下

详情里，节点信息自己填写，然后不认识的都不要动。

obfs 配置这几个地方

1. 插件名称，填写 obfs-local
2. 插件参数，填写 obfs=tls;obfs-host=www.bing.com
3. 然后点击应用本页面设置



* 我遇到一个问题，就是其实是配置成功了，但是我还是打不开科学网站，有的时候是某些网站 dns 出了问题，所以不要老是在一个网站上面测试，或者看一下科学的状态，如果是对勾，那就说明其实一定意义上已经成功了， 或许是某些 DNS 出了问题。
* 关于 DNS 出问题解决方法， 在详情页面下面有一个 DNS 代理服务模式选择，选一个其他的再试试看。



## 如果配置完成后还不行。那么检查 obfs 配置

首先，确定你是否配置好了，可以 ssh 到 路由器里。

然后执行命令:

`cat /tmp/ss-redir_1.json`

看一下一些参数是否配置上去了

```json
{
"server": "xxxxx",
"server_port": "xxx",
"local_address": "0.0.0.0",
"local_port": "1090",
"password": "xxxxxx",
"timeout": "180",
"method": "xxx",
"protocol": "origin",
"protocol_param": "",
"obfs": "plain",
"obfs_param": "",
"plugin": "obfs-local",
"plugin_opts": "obfs=tls;obfs-host=www.aasdf.com",
"reuse_port": true
}
```

这里解释一下 obfs 的参数:

* plugin 这里，需要跟上面的一样
* plugin_opts 这里需要注意 obfs=  需要根据你的服务器来，我的是 tls，所以填写的是 tls，如果你的是 http，就填写http。 obfs-host=  这里随便填写就可以了。



## 重要福利-obfs技巧

通过我使用obfs的一些经验，发现了一个规律，就是如果被封了，可以通过更改 obfs-host 的参数来重新复活，一般来说过一阵以前用的 obfs-host 也会自动复活。

LEDE 无法自动更改，但是老毛子是有自动故障切换功能的，我们怎么做呢，我想了一个办法，就是添加相同的服务，唯有 obfs-host 不同，比如我一个服务添加了10次，每次的 obfs-host 都不同，这样就能实现自动切换及不用经常上路由改动配置。 

---
title: kali中的mysql无法远程访问
date: 2017-11-20 21:22:30
tags: [kali, linux, mysql]
category: linux
---

kali挺好用的，专门渗透的系统，想要搞一搞数据库当做服务器用，可偏偏半天连不上。
我的kali 是官网目前最新的2017.2 64bit版本

* 先把初始密码，以及数据库的权限配置完成
* 一下是网上摘抄的方法：
    
1.改表法。可能是你的帐号不允许从远程登陆，只能在localhost。这个时候只要在localhost的那台电脑，登入mysql后，更改 “mysql” 数据库里的 “user” 表里的 “host” 项，从“localhost”改称“%”

<!-- more -->
`mysql -u root -p 
`mysql>use mysql;`
`mysql>update user set host = ‘%’ where user = ‘root’;`
`mysql>select host, user from user;`

2. 授权法。例如，你想myuser使用mypassword从任何主机连接到mysql服务器的话。

`GRANT ALL PRIVILEGES ON *.* TO myuser@'%' IDENTIFIED BY 'mypassword' WITH GRANT OPTION;`
`FLUSH   PRIVILEGES;`

如果你想允许用户myuser从ip为192.168.1.6的主机连接到mysql服务器，并使用mypassword作为密码

`GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'192.168.1.3' IDENTIFIED BY 'mypassword' WITH GRANT OPTION; `
  ` FLUSH   PRIVILEGES;`

我用的第一个方法,刚开始发现不行,在网上查了一下,少执行一个语句 mysql>FLUSH   PRIVILEGES
使修改生效.就可以了

#################################

开启Mysql数据库的远程连接权限：
一句话，并且修改root 密码为 wrx123
`grant all privileges on *.* to 'root' @'%' identified by 'wrx123';`
`flush privileges;`

 

开启mysql的远程连接
把你的HOST字段改成 % ，表示任何地址的都可以用此帐号登录，或你也可以定IP

`mysql>GRANT ALL on *.* to 123@192.168.0.% identified by “456″;`

* 接下来完成了mysql本身的远程访问权限配置，还是无法连接。
    执行如下命令： 
    `netstat -ntlp`
    发现 mysql 那一栏显示的是127.0.0.1：3306或者localhost：3306这表示mysqld服务只监听本机，只有本机可以连接。
    
    因为kali 的mysql配置文件不好找，也没有网上说的对应的mysql.conf,
    或者my.conf里面也没有什么东西，找了一会，终于找到了。
    在这个目录里/etc/mysql/mariadb.conf.d 改动50-server.cnf这个文件里的 bind-address    127.0.0.1 注释掉就行了，在前面加一个# 号。
    
    然后，我开始还是不行，怎么重启服务都不行。
    
    最后还是重启电脑好了，所以重启一下看下可以不，如果还不行的话
    把 bind-address    0.0.0.0   改成这样在重启一遍。
    

    






---
title: sudo权限分配
date: 2017-06-04 22:09:05
tags: [linux, sudo]
category: linux
---

# sudo

授权之后，能够让某用户以另一个用户的身份运行命令
<!-- more -->

```
配置文件： /etc/sudoers
    root    ALL=(ALL)   ALL
    %wheel  ALL=(ALL)   ALL
    
    who :运行命令者身份，user
    where：通过哪些主机，host
    （whom）：以哪个用户的身份，runas
    which：运行哪些命令，command
    
    配置项：
        users   hosts=(runas)   commands
        
        users:
            username
            #uid
            user_alias
            %group_name
            %#gid
            
        host:
            ip
            hostname
            netaddr
        
        command:
            command


        Alias_Type NAME = item1, item2, ...
        注意：NMAE必须全大写字母
        Alias_Type:
            User_Alias
            Host_Alias
            Runas_Alias
            Cmnd_Alias
    
    Cmnd_Alias USERADMINCMNDS = /usr/sbin/useradd, /usr/sbin/usermod, /usr/bin/passwd [a-z]*, !/usr/bin/passwd
```

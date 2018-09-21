---
title: 'TCP_WRAPPER:TCP包装器'
date: 2018-03-05 22:11:47
tags: [linux, TCP, 访问控制]
category: linux
---


# Tcp_wrapper:tcp包装器

对于基于tcp协议开发并提供服务的应用程序，提供的一层访问控制工具
基于库调用实现其功能
    libwrap

判断服务是否能够由tcp_wrapper进行访问控制
    （1）动态编译：ldd命令
    （2）静态编译：strings命令查看应用程序文件，其结果中如果出现
        hosts.allow
        hosts.deny
<!-- more -->

在配置文件在为各服务分别定义访问控制规则实现访问控制
    /etc/hosts.deny
    /etc/hosts.allow
    
    配置文件语法：
        daemon_list:
            应用程序的文件名称，而非文件名
            应用程序文件名称列表，彼此间使用逗号分隔
                例如：sshd，vsftpd：
                    ALL表示所有服务
        
        client_list:
            IP地址：
            主机名：
            网络地址：必须使用完整格式的掩码，不适用前缀格式掩码：所以类似于192.168.1.1/16不合法
            简短格式的网络主机：例如192.168 表示192.168.0.0/255.255
            ALL：所有主机
            KNOW：
            UNKNOW
            PARANOID
            
            EXCEPT：除了
                hosts.allow
                    vsftpd 172.16. EXCEPT 172.16.100.0/255.255.255.0 EXCEPT 172.16.100.1
                    
            [:options]
                deny: 拒绝，主要用于hosts.allow文件中
                allow： 允许，用于hosts.deny文件，实现allow的功能
                spawn： 启动额外应用程序：
                    vsftpd：ALL：spawn /bin/echo `date` login attempt from %c to %s , %d >> /var/log/vsftpd.deny.log
                        %c: client ip
                        %s: server ip
                        %d: daemon name

​                        

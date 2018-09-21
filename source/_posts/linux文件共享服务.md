---
title: linux文件共享服务
date: 2018-02-04 22:09:48
tags: [linux, ftp, centos]
category: linux
---

# 文件共享服务
应用层： ftp
内核：nfs（Sun）
跨平台：samba
    在Linux实现CIFS（SMB）协议

DAS，NAS，SAN

<!-- more -->
ftp:File Transfer Protocol
    应用层协议：tcp，21/tcp
    C/S:
        Client:程序
        Server:程序

数据：
    命令连接：文件管理类命令，始终在线的连接
    数据连接：数据传输，按需建立及关闭连接
    
            数据传输格式：
                文本传输
                二进制传输
            主动：由服务器端创建连接
                命令：
                    Client：50000 --> Server:21
                数据：
                    Server：20/tcp --> Client:50000+1
            被动：由客户端创建连接
                命令：
                    Client：50000 --> Server:21
                
                数据：
                    Client：50000+1 --> Server: 随机端口


C/S:
    Server:
        wu-ftpd
        proftpd
        pureftp
        vsftp
        ServU
        
    Client:
        ftp
        lftp,lftpget
        wget,curl
        filezilla
        gftp(Linux GUI)
        商业软件：
        flashfxp
        cuteftp

响应码：
    1xx：信息
    2xx：成功类的状态码
    3xx：提示需进一步提供补充类信息的状态码
    4xx：客户端错误
    5xx：服务端错误

用户认证：
    虚拟用户：仅用于访问某服务中特定资源的服务

        nsswitch：network server switch，名称解析框架
            配置文件：/etc/nsswitch.conf
            模块：/lib64/libnss*,/usr/lib64/libnss*
        pam：pluggable authentication module，用户认证框架
            模块：/lib64/security/
            配置文件：/etc/pam.cnf,/etc/pam.d/*
            
    系统用户：
    匿名用户：
    
    CentOS 6.5：vsftpd
        用户认证配置文件：/etc/pam.d/vsftpd
        服务脚本：/etc/rc.d/init.d/vsftpd
        配置文件目录：/etc/vsftpd
            主配置文件：vsftpd.conf
        匿名用户（映射为ftp用户）共享资源位置：/var/ftp
        系统用户通过ftp访问的资源的位置：用户自己的家目录
        虚拟用户通过ftp访问的资源的位置：给虚拟用户指定映射成为系统用户的家目录
            
    匿名用户的配置
    anon_mkdir_write_enable=YES
    anon_upload_enable=YES
    anon_other_write_enable=YES
    
    系统用户的配置
        local_enable=YES
        
        write_enable=YES
        local_umask=022
            
        禁锢本地用于与家目录中
            chroot_local_user=YES
        禁锢文件中指定用户与家目录中
            chroot_list_enable=YES
            chroot_list_file=/etc/vsftpd/chroot_list
            
        日志：
            xferlog_enable=YES
            xferlog_file=/var/log/xferlog
            xferlog_std_format=YES
            
        改变上传文件的属组：
            chown_uploads=YES
            chown_username=whoever
        
        vsftp使用pam完成用户认证，启用到的pam配置文件：
            pam_service_name=vsftpd
            /etc/vsftpd/ftpusers
            
        是否启用控制用户登陆的列表文件
            userlist_enable=YES
            userlist_deny=YES|NO(白名单，黑名单)
            默认文件为/etc/vsftp/user_list
            
        连接限制：
            max_client:最大并发连接数：
            max_per_ip:每个IP可同时发起的并发请求数
            
        传输速率：
            anno_max_rate: 匿名用户的最大传输速率，单位是“字节/秒”
            local_max_rate:本地用户的最大传输速率
            
        虚拟用户：
            素有的虚拟用户会被统一映射为一个指定的系统账号，访问的共享位置即为此系统的家目录：
            
            各虚拟用户可以被赋予不同的访问权限：
                通过匿名用户的权限控制参数进行指定：
                
            虚拟用户的存储方式：
                文件：编辑文件
                    奇数行为用户名
                    偶数行为密码
                    此文件需要被编码为hash格式
                    
                关系型数据库的表中：
                    即时查询数据库完成用户认证
                    mysql库
                        pam要依赖于pam-mysql模块
                        
            补充：
            axel, lftpget ,wget ,curl
                
            ftp协议是明文：
                ftps：SSL
                sftp:SSH
            总结：
                ftp：命令和数据


​            
​            

​        


---
title: httpd
date: 2018-03-20 22:06:35
tags: [linux, httpd]
category: linux
---

# httpd
常用配置：
    1.修改监听的IP和Port
        Listen [ip:]Port
        省略ip表示监听本机所有IP；Listen可重复出现多次；
        
    2.持久化连接
        Persistent Connection：连接建立，每个资源获取完成之后不会断开连接，而是继续等待其他请求完成
        如何断开？
            数量限制：100
            时间限制：可配置
        副作用：对并发访问量较大的服务器，持久连接功能会使有些请求得不到响应
        折中：使用较短的持续连接时间
            http-2.4 支持毫秒级持久时间

<!-- more -->

        非持久连接
        
        KeepAlive On|Off
        MaxKeepAliveRequests #
        KeepAliveTimeout #
        
        测试：
            telnet HOST PORT
            GET /URL HTTP/1.1
            Host: HOSTNAME or IP


    3.MPM
        prefork :多进程模型，一个进程响应一个请求
        worker： 多线程模型（多进程生成，一个进程生成多个线程），一个线程响应一个请求（linux进程本来就很轻量）
        evernt：事件驱动模型，一个线程响应多个请求
        
        并发服务器响应模型：
            单进程的I/O模型
            多进程I/O模型
            复用的I/O模型
                多线程模型
                事件驱动


        CentOS 6:
            程序环境
                配置文件：
                    /etc/httpd/conf/httpd.conf
                    /etc/httpd/conf.d/*.conf
                服务脚本：
                    /etc/rc.d/init.d/httpd
                    配置文件： /etc/sysconfig/httpd
                主程序配置文件：
                    /usr/sbin/httpd
                    /usr/sbin/httpd.event
                    /usr/sbin/httpd.worker
                日志文件目录：
                    /var/log/httpd
                        access_log:访问日志
                        error_log:错误日志
                站点文档目录：
                    /var/www/html
                配置文件组成：
                    [root@localhost ~]# grep "Section" /etc/httpd/conf/httpd.conf
                        ### Section 1: Global Environment
                        ### Section 2: 'Main' server configuration
                        ### Section 3: Virtual Hosts
                常用配置
        CentOS 7:


        Multipath Process Module: 多道处理模块
        prefork, worker, event
        
        http-2.2不支持同时编译多个模块，所以只能编译时选定一个；rpm安装的包提供三个二进制程序文件，分别用于实现
        
        默认为/usr/sbin/httpd,其使用prefork
        查看模块列表：
            查看静态编译的模块
        # httpd -l
            Compiled in modules:
            core.c
            mod_so.c
            http_core.c
        查看静态编译及动态装载的模块
            # httpd -M
            
    更换使用的httpd程序
        /etc/sysconfig/httpd
        
        <IfModule prefork.c>
StartServers       8
MinSpareServers    5
MaxSpareServers   20
ServerLimit      256
MaxClients       256
MaxRequestsPerChild  4000
</IfModule>

<IfModule worker.c>
StartServers         4
MaxClients         300
MinSpareThreads     25
MaxSpareThreads     75
ThreadsPerChild     25
MaxRequestsPerChild  0
</IfModule>

PV,UV
    PV: Page View
    UV: User View
        独立IP量
        
        300*86400 = 40W+

4.DSO
    配置指定实现模块加载
        LoadModule <mod_name> <mod_path>
        
        模块路径可使用相对地址
            相对于ServerRoot(/etc/httpd)指向的路径而言


5.定义‘Main’ server的文档页面路径
    DocumentRoot

    文档路径映射：
        DocumentRoot指向的路径为URL路径的起始位置
            DocumentRoot "/var/www/html"
                test/index.html --> http://HOST:PORT/test/index.html

6.站点访问控制
    可基于两种类型的路径指明对哪种资源进行访问控制
        文件系统类型：
            <Directory "">  </Directory>
            <File ""> </File>
            <FileMatch ""> </FileMatch>
        URL路径：
            <Location ""> </Location>
            ...
        访问控制机制：
            基于来源地址
            基于账号

7.Directory 中 “基于来源地址”实现访问控制

    (1) Options
        所有可用特性: Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
                    None，All
        indexes: 索引
        FollowSyLinks：允许跟踪符号链接文件
        SymLinksifOwnerMatch：符号链接的属组和文件的属组一样可以访问
        
    （2）基于来源地址的访问控制机制
        Order：检查次序
            Order allow，deny 白名单
            Order deny，allow 黑名单
        Allow from
        Deny from
            来源地址：
                IP
                NetAddr：
                    172.16
                    172.16.0.0
                    172.16.0.0/16

8.定义默认主页面
    DirectoryIndex index.html index.html.var

9.日志设定

    错误日志
        ErrorLog logs/error_log
        LogLevel warn
        
         debug, info, notice, warn, error, crit 默认是warn
         
         访问日志:
         CustomLog logs/access_log combined(combined日志的格式)
         LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
         
         %h:客户端IP地址
         %l:Remote logname (from identd,if supplied) -表示为空
         %u：remote user， （from user） - 为空
         %t：Time the request was received 服务器收到请求的时间
         %r：请求报文的首行信息
         %>s：响应状态码
         %b：响应报文主体部分大小，单位byte，不包含响应首部
         %{Referer}i：请求报文当中“referer”首部的值：当前资源的访问入口，即从哪个页面的超链接跳转页面而来
         %{User-Agent}：请求报文中”User-Agent“首部的值：即发出请求用到的应用程序

10.路径别名
    DocumentRoot ”/www/htocs"
        http://localhost/download/bash-5.5.rpm
       --> /www/htdocs/download/bash-5.5.rpm 
    Alias /URL/ "/PATH/to/SOMEDIR/"
        Alias /bbs/ "/forum/htdocs"
            --> /www/htdocs/bbs/

11.设置默认字符集
    AddDefaultCharset UTF-8

    GBL，GB2312，GB18030

12.基于用户的访问控制
    认证质询：
        WWW-Authenticate： 响应码为401，拒绝客户端请求，并说明要求客户端提供账号和密码
    认证：
        Authenticate：客户端用户填入账号和密码后再次发送请求报文:认证通过，则服务器发送响应的资源
    认证方法:
        basic:明文
        digest：消息摘要（如MD5）
        
    安全域：需要用户认证后方能访问的路径
        应该通过名称对其进行表示，并用于告知用户认证的原因
        
    用户的账号密码存储于何处？
        虚拟账号：仅用于访问某服务时用到的认证标识
        存储：
            文本文件
            SQL数据库
            ldap
            nis
            
    basic认证：
        （1）定义安全域
            <Directory "">
                Options None
                AllowOverride None
                AuthType Basic
                AuthName "STRING"
                AuthUserFile "/PATH/TO/HTTPD_USER_PASSWD_FILE"
                Require user username1 username2 ...
            </Directory>
                允许账号文件中所有用户登陆
                Require valid-user
        （2）提供账号和密码存储（文本文件）
                使用htpasswd命令进行管理
                    htpasswd [option] passwordfile username
                    -c :自动创建passwordfile，因此，仅应该在添加第一个用户时使用
                    -m：md5加密密码
                    -s：sha1加密用户密码
                    -D：删除指定用户
        （3）实现基于组进行认证
                    <Directory "">
                Options None
                AllowOverride None
                AuthType Basic
                AuthName "STRING"
                AuthUserFile "/PATH/TO/HTTPD_USER_PASSWD_FILE"
                AuthGroupFile “/PATH/TO/HTTP_GROUP_FILE"
                Require group GROUP1 GROUP2
            </Directory>
        
            要提供：用户账号文件和组文件
            
                组文件：每一行定义一个组
                    GRP_NAME： user1 user2 user3 ...

13.虚拟主机
​    
    有三种实现方案：
        基于IP：
            为每个虚拟主机准备至少一个IP地址
        基于port
            为每个虚拟主机准备至少一个专用port：实践中很少使用
        基于hostname
            为每个虚拟主机准备至少一个专用hostname
        可混合使用上述三种方式中任意方式
        
        注意：一般虚拟主机不与中心主机混用，所以，要使用虚拟主机，先禁用中心主机
            禁用中心主机：注释DocumentRoot
        
        每个虚拟主机都有专用配置：
            <VirtualHost "IP:PORT">
                ServerName
                DocumentRoot ""
            </VirtualHost>

14.内置的status页面

    <Location /server-status>
        SetHandler server-status
        Order deny,allow
        Deny from all
        Allow from .example.com
    </Location>
实现：基于账号实现访问控制

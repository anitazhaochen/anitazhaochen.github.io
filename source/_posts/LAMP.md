---
title: LAMP
date: 2018-03-24 22:07:29
tags: [linux, lamp, 运维]
category: linux
---

# LAMP
a: apache
m: mariadb, mysql
p: php,perl,python

LAMMP : memcached

静态资源：静态内容，客户端从服务器获得的资源的表现形式与原文件相同
动态资源：通常是程序文件，需要在服务器执行之后，将执行的结果返回给客户端

    CGI：Common Gateway Interface

    fastcgi

<!-- more -->

    程序=指令+数据

httpd+php:
    modules
    cgi
    fastcgi(frpm)

请求流程： Client --> (http) --> httpd --> (cgi) --> application server (program file) --> (mysql) --> mariadb

Centos 7:
    程序包： httpd，php，php-mysql，mariadb-server
        注意：php需要httpd使用perfork MPM
        
    启动服务：
        systemctl start httpd.service
        systemctl start mariadb.service

Centos 6:
    程序包：httpd，php，php-mysql，mysql-server
    启动服务：
        service httpd start
        service mysqld start

测试：
    php程序执行环境：
        test.php
        <?php
            phpinfo();
        ?>
        
    测试php与mysql通信
        test2.php
            <?php
                $conn = mysql_connect('HOST','USERNAME','PASSWORD');
                if ($conn)
                    echo "OK";
                else
                    echo "Ffilure";
                
                mysql_close();
            ?>
    
    phpMyAdmin:
        mariadb 的WebGUI
        
    php解释器如何与MariaDB交互
        解释器无需与Mariadb交互，那些需要用到数据存储系统的程序才需要与数据存储交互
        
        存储系统：
            文件系统：文件
            SQL： Mariadb，Oracle，MSSQL，...
            NoSQL: redis,mogodb,hbase,...
            NewSQL:


    Mariadb的特性：
        插件式存储引擎：存储管理器有多重实现版本，功能和特性可能略有差别，用户可根据需要灵活选择
        
        存储引擎也称之为“表类型”
        （1）更多的存储引擎
            MyISAM --> Aria 
            InnoDB --> XtrDB
            
        （2）诸多扩展和新特性
        （3）提供了较多测试组件中
        （4）truly open source

安装和使用MariaDB
    CentOS 7 直接提供
    CentOS 6 通用二进制格式安装过程
        （1）准备数据目录
        （2）配置mariadb
```
            # groupadd -r -g 306 mysql
            # useradd -r -g 306 -u 306 mysql
            # tar xf mariadb-VERSION.tar.gz -C /usr/local
            # ln -sv
            # cd /usr/local/mysql
            # chown -R root:mysql ./*
            # scripts/mysql_install_db --datadir=/mydata/data --user=mysql
            # cp supper-files/mysql.server /etc/rc.d/init.d/mysqld
            # chkconfig --add mysqld
        （3）准备配置文件
            配置格式：类ini格式，为各程序均通过单个配置文件提供配置信息
                [prog_name]
            配置文件查找次序：
                /etc/my.cnf --> /etc/mysql/my.cnf/ --> --default-extra-file=/PATH/TO/CONF_FILE --> ~/.my.cnf 
            # mkdir /etc/mysql
            # cp support-files/my-large.cnf /etc/mysql/my.cnf
            
            添加三个选项：
             datadir = /mydata/data
             innodb_file_per_table = on
             skip_name_resolve = on
```
             
    MariaDB的程序组成：
        C:
            mysql：CLI交互式客户端程序
            mysqldump，mysqladmin...
        S:
            mysqld_safe
            mysqld
            mysqld_multi
            
    服务器监听的两种socket地址：
        ip socket：监听在tcp的3306端口，支持远程通信
        unix sock：监听在sock文件上（/tmp/mysql.sock,/var/lib/mysql/mysql.sock),仅支持本地通信
            server：localhost，127.0.0.1
            
    命令行交互客户端程序：mysql
        mysql
            -uUSERNAME: 用户名
            -hHOST: 服务器主机
            -pPASSWORD: 用户的密码
            
            注意： mysql用户账号由两部分组成： ‘USERNAME’@‘HOST’；其中HOST用于限制此用户可通过哪些主机远程连接mysql服务
                支持使用通配符：
                %：匹配任意长度的任意字符：
                172.16.0.0/16  172.16.%.%
                _:匹配任意单个字符
                
        mysql_secure_installation ：安全初始化
        
        命令：
            客户端命令：本地执行
                mysql> help
                每个命令都有完整形式和简写形式
                    status，\s
            服务端命令：通过mysql协议发往服务器执行并取回结果
                每个命令都必须有命令结束符号，默认为分号；
                
    关系型数据库的常见组件：
        数据库：database
        表：table
            行：row
            列：column
        索引：index
        视图：view
        用户：user
        权限：privilege
        
        存储过程：procedure
        存储函数：function
        触发器：trigger
        事件调度器：event scheduler


LAMP组合的编译安装：
    httpd+php
        modules： 把php编译成httpd的DSO对象：
            prefork：libphp5
            event，worker：libphp5-zts
        cgi
        fpm（fastcgi）：php作为独立的服务
        
    httpd对fastcgi协议的支持：
        httpd-2.2：需要额外安装fcgi模块
        httpd-2.4：自带fcgi模块
        
    安装次序：
        httpd，MariaDB，php


       ` [root@localhost httpd-2.4.29]# ./configure --prefix=/usr/local/apache --sysconfdir=/etc/httpd24/ --enable-so --enable-ssl --enable-cgi --enable-rewrite --with-zlib --with-apr=/usr/local/apr --with-apr-util=/usr/local/aprutil --enable-modules=most --enable-mpms-shared=all --with-mpm=event `

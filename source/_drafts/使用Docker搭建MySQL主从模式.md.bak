---
title: 使用Docker搭建MySQL主从模式
date: 2020-07-27 17:36:38
tags: [MySQL, Docker]
category: MySQL
---

眼过千遍不如手过一遍，最近在复习 MySQL 知识的时候，准备边看边练。记得有一个国内某家安全公司的一个黑客说过一句话： 搞就牛。
所以，还是理论与实践相结合。

[Docker MySQL 指南](https://hub.docker.com/_/mysql)

## 搭建 MySQL 主从模式

如果那虚拟机，或者服务器搭建的话，有点麻烦，且不易移植，使用 Docker 就可以了。

由于当时pull 镜像的时候，没有选择版本，所以就默认 MySQL 最新版本，确实问题有点多。

MySQL 版本： 8.0.21

<!--more -->
第一步从 Docker 上面下载 MySQL 镜像：

`docker pull mysql`

第二步： 创建一些列文件夹及配置文件，后面分析一些 MySQL 数据需要用到。
      目前是一主一从的模式： 所以就在家目录建立了如下文件夹：
```shell
.MySQL
├── master
│   ├── conf.d -- my.cnf
│   └── data
└── slaver
    ├── conf.d -- my.cnf
    └── data
```
一个存放 master 的配置文件，及数据文件，一个存放 slave 的。

* master 配置文件:
```shell
[mysqld]
# MySQL 服务id， 只要不重复就好
server_id = 1
# 开启 binlog
log_bin = mysql-bin
# 设置只读为否
read-only=0
# 设置哪个数据库产生binlog，这个数据库也是后面做实验的对象
binlog-do-db=test_db
# 以下是忽略的数据库
replicate-ignore-db=mysql
replicate-ignore-db=sys
replicate-ignore-db=information_schema
replicate-ignore-db=performance_schema
```
master 数据库的配置文件配置好后，创建一个 data 文件夹来存放 MySQL 存储在硬盘的数据。

一开始难免有时会配错，所以，我直接写了一个开启 Docker 的脚本也就一行命令。
```shell
docker run --name mysql_master -v /root/MySQL/master/data:/var/lib/mysql -v /root/MySQL/master/conf.d:/etc/mysql/conf.d -p 3307:3306 -e MYSQL_ROOT_PASSWORD=123456789 -d mysql
```
从库也差不多,从库的MySQL 配置文件：
```shell
[mysqld]
server_id = 2
log_bin = mysql-bin
read-only=1
binlog-do-db=test_db
replicate-ignore-db=mysql
replicate-ignore-db=sys
replicate-ignore-db=information_schema
replicate-ignore-db=performance_schema
```
不同的地方在于把从库设置为只读模式， 然后 `server_id` 不能跟master相同
其他地方都与master类似。
从库 Docker 脚本：
```shell
docker run --name mysql_slaver -v /root/MySQL/slaver/data:/var/lib/mysql -v /root/MySQL/slaver/conf.d:/etc/mysql/conf.d -p 3308:3306 -e MYSQL_ROOT_PASSWORD=123456789 -d mysql
```

到目前为止，基本工具都已经准备好了，可以开启 Docker 了。

因为这次使用的是 MySQL 最新版本，所以会遇到一些问题。

Docker 开启后，使用命令进入 Docker 内部:
`docker exec -it docker_name bash`
然后就可以使用 mysql 命令了。
先设置 master MySQL：
`mysql -uroot -p123456`
连上之后，我们先创建一个专门给 slave 使用的用户。
以前的创建方式可以这样:
```shell
GRANT REPLICATION SLAVE ON *.* to 'backup'@'%' identified by '123456';
```
但是现在不可以了，MySQL 最新版本已经将这种方式禁用了。
现在需要分为两步进行创建，即先 创建，在授权。
```shell
# 添加用户
create user backup identified by '123456';
# 授权
grant replication slave on *.* to 'backup'@'%';
```
到此为止 MySQL master 部分就配置完成了。
[Creating a User for Replication](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-repuser.html)

接下来继续配置 slave，使用同样的方式进入 docker 容器。
进入 mysql:
`mysql -uroot -p123456789`

设置从库：
```shell
change master to 
master_host='你的master的ip地址',
master_port=3306,
master_user='backup',
master_password='123456',
master_log_file='mysql-bin.000003',
master_log_pos=2290,
get_master_public_key=1;
```
Master 的ip地址可以在 Docker 外部通过:
`sudo docker inspect --format '{{ .NetworkSettings.IPAddress }} container_id`
查看, 也可以直接在容器内 cat /etc/hosts 文件，最下面的地址就是容器的 ip 地址。
也可以放到你的 .bashrc 文件中，这样就很方便， 在此感谢下面这篇文章。
```shell
function docker_ip() {
    sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' $1
}
```
然后 `source .bashrc`
查看IP: `docker_ip container-ID/container-name` , 使用容器id，容器name都可以，只要唯一能够确定。
[获取Docker的IP](https://blog.csdn.net/sannerlittle/article/details/77063800)

端口： 如果就是 3306
master_user: 就是刚才在 master 上面创建的专门用于同步的用户
master_password： 同上
master_log_file: 这个需要通过在 mysql 终端里通过 `show master status` 来进行查看。
master_log_pos: 同上
get_master_public_key=1: 这个参数是因为 MySQL 8.0 需要进行加密传输,直接用明文它不允许
解决方法是： 首先推出当前 mysql 终端，在slave 上面使用 
`mysql -h master_ip -ubackup -pxxxxx` 连接一次，登上后在退出就好了。
开启 slave 模式
`start slave;`
关闭 slave 模式
`stop slave`
通过：
`show slave status;` 来查看状态，如果发现 

```shell
Got fatal error 1236 from master when reading data from binary log:
```
有可能是因为 bin_log packet 大小导致的，master 的超过了 slave 最大能承受的大小。
先执行一下:
```shell
set global max_allowed_packet=1*1024*1024*1024;
stop slave;
start slave;
```
如果还没有好的话，请参考这篇文章
[MySQL Got fatal error 1236 解决方法](https://www.cnblogs.com/zhoujinyi/p/4760184.html)


如果显示：
```shell
  Slave_IO_State: Waiting for master to send event
  Slave_IO_Running: Yes
  Slave_SQL_Running: Yes
```
就说明成功了,这个时候可以去 master 上试试，增删操作，看看 从库是否也会跟着动。



























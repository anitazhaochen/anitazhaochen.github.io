---
title: MySQL主从搭建及创建新用户及远程访问
date: 2021-04-15 17:55:58
tags: MySQL
category: MySQL
---

## MySQL 版本

```
mysql> select version();
+-------------------------+
| version()               |
+-------------------------+
| 8.0.23-0ubuntu0.20.04.1 |
+-------------------------+
1 row in set (0.00 sec)
```

ubuntu 20.04 
<!--more -->

<!-- more -->

## Master （主库）配置

修改配置文件： `/etc/mysql/mysql.conf.d/mysqld.cnf`

```mysql
[mysqld]
server-id=1 
# server-id 保证唯一，必须与从库不同

log-bin=mysql-bin
# 开启二进制日志，主库必须开启

binlog_expire_logs_seconds=2592000
# 自动删除 2592000 秒(30天)前的日志（可选）

binlog_format=mixed
# binlog 记录模式：
# statement 模式不会记录每一条更改语句，节约资源但是会造成主从数据不一致
# row 模式记录每一条更改的语句，日志量非常大
# mixed 模式是前两者有点的综合，日志结构较复杂

binlog-do-db=demo
# 设置只记录 binlog 的库 （可选）

```



## Slave（从库）配置

修改配置文件： `/etc/mysql/mysql.conf.d/mysqld.cnf`

```mysql
[mysqld]
server-id=2
# 设置 server-id, 唯一值，必须与主库不同

replicate-do-db=demo
# 设置只同步 binlog 的库。

read_only=1
# 设置从库只读 （可选）

```



### 导出主库并还原从库（如果你是临时加了一台从库）

```csharp
mysqldump -uroot -p --skip-lock-tables --single-transaction --flush-logs --hex-blob --master-data=2 demo > /demo.sql
```

--skip-lock-tables：不锁表

--single-transaction：设定事务级别为可重复读

--flush-logs：开启一个新的binlog文件

--hex-blob：以16进制导出blob数据

--master-data=2：导出数据库时将binlog信息也一并导出，2表示注释binglog信息

接下来，将导出的文件传输到从服务器上面，然后将SQL文件导出到从库，导入前记得先创建好和主库一致的数据库。

```
mysql> use demo;

mysql> source /xxx/xxx/demo.sql;
```



* 创建主从专用账号（Recommand）

从库连接主库需要一个用户，也可以直接使用 root 账户进行配置，但是不建议。

```mysql
create user 'copy'@'%' identified by 'copy@copy';

grant replication slave,replication client on *.* to 'copy'@'%';
```

1. 创建了一个用户名为 copy 的用户，可从任意地址访问，密码为：copy@copy
2. 将 replication slave （没有这个权限将不能同步数据）、replication client（用于查看从库状态即：show slave status 命令） 权限赋予给 copy 用户。



## 配置主从

我们刚才从主库导出数据的时候，将binlog信息也一块导出来了，我们使用如下命令:

```
cat demo.sql | grep CHANGE

-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000005', MASTER_LOG_POS=630;

```

上图说明主库目前正在使用 `mysql-bin.000005` 这个binlog文件，位置为 630。

在从服务器上执行：

```mysql
# 假设主服务器IP为 192.168.1.2 并且默认端口为 3306。

mysql> change master to master_host='192.168.1.2',
    -> master_port=3306,
    -> master_user='copy',
    -> master_password='copy@copy',
    -> master_log_file='mysql-bin.000005',
    -> master_log_pos=630;
Query OK, 0 rows affected, 2 warnings (0.02 sec)

# 最后开启主从复制
mysql> start slave;
Query OK, 0 rows affected, 1 warning (0.00 sec)

# 查看主从连接状态

mysql> show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: ip
                  Master_User: username
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000007
          Read_Master_Log_Pos: 517
               Relay_Log_File: adam-relay-bin.000010
                Relay_Log_Pos: 685
        Relay_Master_Log_File: mysql-bin.000007
             Slave_IO_Running: Yes  # 正常为 YES
            Slave_SQL_Running: Yes  # 正常为 YES
              Replicate_Do_DB: demo
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: 
  Replicate_Wild_Ignore_Table: 
                   Last_Errno: 0
                   Last_Error: 
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 517
              Relay_Log_Space: 1108
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 0
               Last_SQL_Error: 
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 1
                  Master_UUID: 10d10288-32ce-11eb-8674-00163e086d97
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: 
            Executed_Gtid_Set: 
                Auto_Position: 0
         Replicate_Rewrite_DB: 
                 Channel_Name: 
           Master_TLS_Version: 
       Master_public_key_path: 
        Get_master_public_key: 0
            Network_Namespace: 
1 row in set, 1 warning (0.00 sec)
```

上面的两个指标： Slave_IO_Running 和 Slave_SQL_Running 都为 Yes 的时候表示主从同步正常。



## 远程连接

不建议使用 root 用户进行远程连接，如果非得使用 root，可自行查阅资料。

```mysql
CREATE USER 'remote_user'@'%' IDENTIFIED BY 'v4QA7K7wOJTM@';
# 创建一个 MySQL 专门的用户, 使用这个用户对数据库进行操作, 这里我创建了一个 
# 用户名为 remote_user ，密码为 v4QA7K7wOJTM@ 的用户。 注意密码最好随机生成，否则可能会提示你密码不满足，就无法创建用户。

GRANT ALL PRIVILEGES ON *.* TO 'school'@'%';
# 赋予这个用户库权限，这里给了这个用户 school 库权限

FLUSH PRIVILEGES;
# 刷新权限，然后就可以远程使用这个用户进行登录了。
```





# QAQ

* 我设置了从库只读，在配置文件中加入了 read_only，但是使用 root 用户登录到 MySQL 后还是可以执行增删改操作？

  首先 read_only=1 只读状态，是不会影响主从复制功能的。仅仅是限定普通用户进行数据修改操作，但不会限定具有 super 权限的用户的数据修改操作。如果要限制 root 用户也无法进行修改操作，可以加入 super_read_only=1 就可以了， 这个变量也不会影响主从复制功能。



* 在 Ubuntu 20.04 上直接通过 apt 安装完 mysql (8.0.23版本)后，发现无论怎么设置，root 用户都无法远程连接， 有些设置完后，连 MySQL 都连接不上了。

  操作方法： 首先 `service mysql stop ` 停止 MySQL 服务，然后在配置文件中 `/etc/mysql/mysql.conf.d/mysqld.cnf` 加入 `skip-grant-tables ` 参数，然后开启服务 `service mysql start` 后，就可以直接通过 `mysql -uroot ` 进行连接，然后再把我们修改的地方修改回去就可以了。修改完后，记得把配置文件中加的跳过权限校验的参数去掉。

* 在 MySQL 的 mysql.user 表中，将 root 的 host 改为 `%` 依旧无法远程登录

  [stackoverflow 讨论](https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost) 我使用第一种方式后，MySQL 直接无法登录，第二种方式创建一个新的用户是可行的。



[参考MySQL 8 主从搭建](https://www.jianshu.com/p/e33c861c2141)

[限制MySQL从服务器为只读状态](https://www.cnblogs.com/qlqwjy/p/8541959.html)


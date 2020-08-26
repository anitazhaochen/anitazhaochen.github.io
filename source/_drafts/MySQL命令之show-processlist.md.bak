---
title: MySQL命令之show processlist
date: 2020-08-20 10:00:17
tags: [MySQL]
category: MySQL
---



如果你是 Linux 初级用户，为什么不建议使用 root 账户，一方面 root 权限太大，这谁都知道，另一方面可能也是较为重要的一点，那就是 普通用户和 root 用户执行同一个操作，最终的结果可能不一样，而在公司工作，往往都不会使用 root 账户。这也就是有时候你查询到的资料的结果和你自己执行的结果不一样的原因。



在 MySQL 中，执行 `show processlist; ` 是显示用户用户正在运行的线程，

```sql

mysql> show processlist;
+----------+------------+----------------------------------------+------+---------+------+-------+------------------+
| Id       | User       | Host                                   | db   | Command | Time | State | Info             |
<!--more -->
+----------+------------+----------------------------------------+------+---------+------+-------+------------------+
| 12913293 | my_user | localhost:54716 | NULL | Query   |    0 | NULL  | show processlist |
+----------+------------+----------------------------------------+------+---------+------+-------+------------------+
1 row in set (0.00 sec)
```

* Id ： 数据库连接的id，可以在 MySQL 中使用 kill  Id 将其结束。
* User：用户名
* Host： 分为主机名和主机的主动连接的端口（这个端口是随机的）
* db： 选择的数据库，这里还没选择数据库就是 NULL
* Command： 当前正在执行的命令
* Time： 处于 State 显示的状态多久了，如果没有其他连接，只有这一个连接，它永远是0，因为你一执行命令他就刷新了。
* State： 状态取决于正在执行的 Command 命令。
* Info：记录线程直接的语句。默认只显示100个字符，如果要看全部信息，需要使用 `show full processlist`

State的各种状态：

A thread can have any of the following `Command` values:

- `Binlog Dump`

  This is a thread on a replication source for sending binary log contents to a replica.

- `Change user`

  The thread is executing a change-user operation.

- `Close stmt`

  The thread is closing a prepared statement.

- `Connect`

  A replica is connected to its source.

- `Connect Out`

  A replica is connecting to its source.

- `Create DB`

  The thread is executing a create-database operation.

- `Daemon`

  This thread is internal to the server, not a thread that services a client connection.

- `Debug`

  The thread is generating debugging information.

- `Delayed insert`

  The thread is a delayed-insert handler.

- `Drop DB`

  The thread is executing a drop-database operation.

- `Error`

- `Execute`

  The thread is executing a prepared statement.

- `Fetch`

  The thread is fetching the results from executing a prepared statement.

- `Field List`

  The thread is retrieving information for table columns.

- `Init DB`

  The thread is selecting a default database.

- `Kill`

  The thread is killing another thread.

- `Long Data`

  The thread is retrieving long data in the result of executing a prepared statement.

- `Ping`

  The thread is handling a server-ping request.

- `Prepare`

  The thread is preparing a prepared statement.

- `Processlist`

  The thread is producing information about server threads.

- `Query`

  The thread is executing a statement.

- `Quit`

  The thread is terminating.

- `Refresh`

  The thread is flushing table, logs, or caches, or resetting status variable or replication server information.

- `Register Slave`

  The thread is registering a replica server.

- `Reset stmt`

  The thread is resetting a prepared statement.

- `Set option`

  The thread is setting or resetting a client statement-execution option.

- `Shutdown`

  The thread is shutting down the server.

- `Sleep`

  The thread is waiting for the client to send a new statement to it.

- `Statistics`

  The thread is producing server-status information.

- `Table Dump`

  The thread is sending table contents to a replica.

- `Time`

  Unused.



[MySQL官网](https://dev.mysql.com/doc/refman/5.6/en/thread-commands.html)

中文解释：

- Binlog Dump: 主节点正在将二进制日志 ，同步到从节点
- Change User: 正在执行一个 change-user 的操作
- Close Stmt: 正在关闭一个Prepared Statement 对象
- Connect: 一个从节点连上了主节点
- Connect Out: 一个从节点正在连主节点
- Create DB: 正在执行一个create-database 的操作
- Daemon: 服务器内部线程，而不是来自客户端的链接
- Debug: 线程正在生成调试信息
- Delayed Insert: 该线程是一个延迟插入的处理程序
- Drop DB: 正在执行一个 drop-database 的操作
- Execute: 正在执行一个 Prepared Statement
- Fetch: 正在从Prepared Statement 中获取执行结果
- Field List: 正在获取表的列信息
- Init DB: 该线程正在选取一个默认的数据库
- Kill : 正在执行 kill 语句，杀死指定线程
- Long Data: 正在从Prepared Statement 中检索 long data
- Ping: 正在处理 server-ping 的请求
- Prepare: 该线程正在准备一个 Prepared Statement
- ProcessList: 该线程正在生成服务器线程相关信息
- Query: 该线程正在执行一个语句
- Quit: 该线程正在退出
- Refresh：该线程正在刷表，日志或缓存；或者在重置状态变量，或者在复制服务器信息
- Register Slave： 正在注册从节点
- Reset Stmt: 正在重置 prepared statement
- Set Option: 正在设置或重置客户端的 statement-execution 选项
- Shutdown: 正在关闭服务器
- Sleep: 正在等待客户端向它发送执行语句
- Statistics: 该线程正在生成 server-status 信息
- Table Dump: 正在发送表的内容到从服务器
- Time: Unused

[感谢知乎博主](https://zhuanlan.zhihu.com/p/30743094)


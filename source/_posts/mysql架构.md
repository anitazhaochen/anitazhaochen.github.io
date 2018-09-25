---
title: mysql架构
date: 2018-02-06 01:17:07
tags: [mysql, arch]
category: 数据库
---

# MySql ARCH

单进程多线程：


用户连接：连接线程，支持长短连接    
* MySql 线程池：Connection Pool
    包含： Authentication 、Thread Reuse、Connection Limits、Check Memory、Caches
<!-- more -->

* SQL 接口 SQL interface 
    分析语句
* Parser 解析：
    解析语句，检测用户是否有权限执行某些语句
* Optimizer 检查多条路径，根据统计数据选择最低开销执行 （优化查询）
* Caches & Buffers
* mysql 插件式引擎，可以任意切换
    如： MyISAM、innoDB、NDB、Archive、Memory、Federate等等引擎

# Mysql数据文件类型
* 数据文件、索引文件
* 重做日志、撤销日志、二进制日志、错误日志、查询日志、慢查询日志、中继日志

## Management Service & Utilitles 管理服务及工具
备份恢复工具、安全工具、集群服务、应用工具、管理配置工具、迁移工具

# DDL&DML
索引管理：
    按特定数据结构存储的数据：

索引类型：
    聚集索引、非聚集索引：数据是否与索引存储在一起
    主键索引、辅助索引
    稠密索引、稀疏索引：是否索引了每一个数据项
    B（Balance）+TREE、HASH（键值对）、R TREE
    简单索引、组合索引
    覆盖索引：不用查找源数据，直接就能就能找到数据，如：名字和课程索引，查到课程就可以知道名字。
    左前缀索引： 从左到右抽取特定大小数据进行索引。这样就会导致一个问题，通过查询中间出现abc的语句， like %abc% 查询索引就失效了，最好不要加左%号

## 管理索引的途径：
创建索引：创建表时指定
创建或者删除索引：修改表的命令

使用EXPLIAN: 查看查询了的过程
EXEPLIAN select * from table where  xx = xx\G 可以查看查询过程，

## 视图：VIEW
    虚表：
    视图中的数据事实上存储于基表中，因此，其修改也会针对基表实现，其修改操作受基表限制





mysql优化： 使用一种sql语句风格进行查询， 因为在查询的时候，会对 查询语句做一次hash， hash 是区分大小写的。



查询 表 扫描 转化为 索引扫描 

左前缀索引：








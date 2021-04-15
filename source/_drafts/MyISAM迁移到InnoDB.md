---
title: MyISAM迁移到InnoDB
date: 2021-04-09 11:22:27
tags: [MyISAM, InnoDB]
category: MySQL
---

表：

1. MyISAM 的主键索引中，可以在非第一列使用自增列，而 InnoDB 的主键索引中包含自增列时，必须在最前面，如果有类似的表则无法从 MyISAM 转成 InnoDB。
2. 查找代码中类似这种不带条件频繁统计全表记录数 `SELECT COUNT(*) FROM TAB` ，InnoDB速度不如 MyISAM ，因为 MyISAM 存储了表的行数，由于 InnoDB 支持事务，返回的行数一般是不确定的，所以每次都需要算一遍。
3. 一次性导入大量数据，后续修改很少，可以继续使用 MyISAM 引擎。

MyISAM引擎特点：

不支持事务，数据文件和索引文件分开存储

支持全文索引，主键索引和二级索引完全一样都是 B+ 树的数据结构，只有是否唯一的区别。主键索引和唯一索引有唯一属性，其他普通索引没有唯一属性。 B+树 叶子节点存储的都是指向行记录的 指针。

有特殊的计数器记录当前行数

不支持崩溃恢复。

InnoDB 引擎特点：

支持事务， 数据文件和索引文件存储在同一个表空间中，主键和二级索引数据结构也是B+树，但是叶子节点存储的键值不一样（主键的叶子节点存储整行数据，也称局促索引；而二级索引的叶子节点存储的是主键的键值）

支持崩溃恢复

相同数据量时，InnoDB 表空间文件大小约为 MyISAM 引擎的 1.5~2倍。

InnoDB 把数据和索引同时缓存在内存中，而 MyISAM 只缓存了索引。



目前 MyISAM 的一些设置：

```
mysql> show variables like '%key_buffer%';
+-----------------+-------------+
| Variable_name   | Value       |
+-----------------+-------------+
| key_buffer_size | 12884901888 |
+-----------------+-------------+
1 row in set (0.00 sec)

mysql> show global status like 'key_read%';
+-------------------+-------------+
| Variable_name     | Value       |
+-------------------+-------------+
| Key_read_requests | 27907338927 |
| Key_reads         | 32307129    |
+-------------------+-------------+
2 rows in set (0.00 sec)

mysql>
```

`key_buffer_size`: 指定索引缓存区的大小，决定索引处理的速度，尤其是读的速度。

此参数只适用于 MyISAM 表，即使不使用此值，如果会创建内部临时磁盘表是 MyISAM 表，也要使用此值。

可以使用 `show status like %created_tmp_disk_tables%` 进行查看磁盘临时表创建情况。

上面是原来的 MyISAM 表 Key_reads / Key_read_requests *100 百分比 0.1 都不到，值越小性能越好，过小可能造成内存浪费。

innodb_buffer_pool_size: [官网文档](https://dev.mysql.com/doc/refman/5.7/en/innodb-buffer-pool-resize.html) 合理设置缓冲池大小。

关闭查询缓存，锁表的时候，常常会出现 `query cache lock` 这个状态，查询缓存在 MySQL 最新的版本已经被移除，只要表里面有一行记录发生增删改，就会导致整个表的查询缓存失效。



代码：

1. 由于InnoDB支持事务， 所以最好开启自动提交，否则会有很多长事物。
2. 大量数据插入操作，最好批量进行 commit，而不是最后提交一次，尽量避免长事物。

3. 跑报表等长时间 sql，可以将 autocommit 设置为 1， 这个是默认值。



建表：

每张表必须有一个主键，用来提高查询效率，逐渐不能频繁修改
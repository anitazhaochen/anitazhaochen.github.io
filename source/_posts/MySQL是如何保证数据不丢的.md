---
title: MySQL是如何保证数据不丢的(binlog/redolog)
date: 2021-03-15 10:39:59
tags: [MySQL]
category: MySQL
---

以下讨论都基于 MySQL 的 InnoDB 存储引擎上。

结论： 只要 redo log 和 binlog 保证持久化到磁盘，就能确保 MySQL 异常重启后，数据可以恢复。

## 崩溃恢复逻辑

* 如果 redo log 里面的事务时完整的，也就是已经有了 commit 标识，则直接提交
* 如果 redo log 里面的事务只有完整的 prepare，则判断对应的事务 binlog 是否存在并完整，如果是则提交，否则回滚事务

这里恢复逻辑是都依赖了 redo log 的两阶段提交中的 prepare 和 commit 。



<!--more -->
## binlog 写入机制

binlog 的写入逻辑：事务执行过程中，先把日志写到 `binlog cache`，事务提交的时候，再把 `binlog cache` 写到 `binlog` 文件中。

一个事务的 `binlog` 是不能被拆开的，因此不论这个事务多大，也要确保一次性写入。这就涉及到了 `binlog cache` 的保存问题。

系统给 `binlog cache ` 分配了一片内存，每个线程独立，参数 `binlog_cache_size` 用于控制单个线程内 `binlog cache` 所占内存的大小。如果超过了这个参数规定的大小，就要暂存到磁盘。

事务提交的时候，执行器把 `binlog cache` 里的完整事务写入到 `binlog` 中，并清空 `binlog cache` 。

> tips： 这里所说的将完整事务（write）写到 binlog 文件中，只是将日志写入到文件系统的 page cache 中，并没有持久化到磁盘，所以速度比较快。
>
> 最终，由 fsync 将数据持久化到硬盘。一般而言，几乎只有 fsync 才占磁盘的 IOPS。

write 和 fsync 的时机，是由参数 sync_binlog 控制的：

* sync_binlog = 0 表示每次提交事务都只 write，不 fsync
* sysnc_binlog = 1 表示每次提交事务都会执行 fsync
* sync_binlog = N (N>1) 表示每次提交事务都 write，但累积 N 个事务后才 fsync



因此，在出现IO瓶颈的场景中，将 sync_binlog 设置成一个比较大的值，可以提升性能。在实际的业务场景中，考虑到丢失日志量的可控性，一般不建议将这个参数设为0，比较常见的是将其设置为100~1000之间的某个数值。

但是，将 sync_binlog 设置为 N ，对应的风险是：如果主机发生异常重启，会丢失最近 N 个事务的 binlog 日志。



## redo log 写入机制

redo log 的数据也对应三种状态：

* 存在 redo log buffer 中，即 MySQL 进程内存中
* 写到磁盘（write），但是没有持久化（fsync），存在于文件系统的 page cache 里
* 持久化硬盘，对应的是存储在磁盘中

redo log 首先会将日志写到 redo log buffer 中速度是非常快的，write 到 page cache 也差不多，但是持久化到磁盘速度就很慢了。

为了控制 redo log 的写入策略， InnoDB 提供了 `innodb_flush_log_at_trx_commit` 参数，取值如下：

* 为0时，表示每次事务提交时都只把 redo log 留在 redo log buffer 中
* 为1时，表示每次事务提交时都将 redo log 直接持久化到硬盘
* 为2时，表示每次事务提交时都只把 redo log 写到 page cache(文件系统缓存)。

InnoDB 有一个后台线程，每隔1秒，就会把 redo log buffer 中的日志，调用 write 写到文件系统的 page cache，然后调用 fsync 持久化到硬盘。

> tips：事务执行中间过程的 redo log 也是直接写在 redo log buffer 中的，这些 redo log 也会被后台线程一起持久化到硬盘。也就是说，一个没有提交的事务的 redo log，也是可能已经持久化到硬盘的。

实际上，除了后台线程每秒一次的轮询，还有两种场景会让一个没有提交的事务的 redo log 写入到磁盘中。

* redo log buffer 占用的空间即将到达 innodb_log_buffer_size 一半的时候，后台线程会主动写盘。注意，由于这个事务没有提交，所以这个写盘动作只是 write，而没有 fsync，也就是只留在了文件系统的 page cache。
* 并行的事务提交的时候，顺带将这个事务的 redo log buffer 持久化到硬盘。假设一个事务A执行到一半，已经写了一些 redo log 到 buffer 中，这时候有另一个线程的事务B提交，如果 innodb_flush_log_at_trx_commit 设置的是1，那么按照这个逻辑，事务B就要把 redo log buffer 里的日志全部持久化到磁盘。这时候，就会带上事务A在 redo log buffer 里的日志一起持久化到磁盘。



如果将 innodb_flush_at_trx_commit 设置为1，那么 redo log 在 prepare 阶段就要持久化一次，因为有一个崩溃恢复逻辑是要依赖于 prepare 的 redo log，再加上 binlog 来恢复的。

每秒一次后台轮询刷盘，再加上崩溃恢复这个逻辑，InnoDB 就认为 redo log 在 commit 的时候就不需要 fsync 了，只会 write 到文件系统的 page cache 中就够了。

## 组提交

` show global status like 'Com_commit'; ` 

上面这条命令可以查看 MySQL 每秒的事务提交量，简称 TPS。

如果 sysnc_binlog 和 innodb_flush_log_at_trx_commit 都设置为1。也就是说，一个事务完整提交前，需要等待两次刷盘，一次是 redo log (prepare阶段)，一次是 binlog。

为了节省磁盘的 IOPS，MySQL 使用了组提交进行 fsync 写盘。

* binlog_group_commit_sync_delay 参数，表示延迟多少微秒后才调用 fsync
* binlog_group_commit_sync_no_delay_count 参数，表示积累多少次以后才调用 fsync。

以上两个条件是或的关系，也就是说只要有一个满足条件就会调用 fsync。

所以，当 binlog_group_commit_sync_delay 设置为0的时候，binlog_group_commit_sync_no_delay_count 也就无效了。

WAL 机制得益于两方面：

1. redo log 和 binlog 都是顺序写，磁盘的顺序写比随机写速度要快
2. 组提交机制，可以大幅度降低磁盘的IOPS消耗

## MySQL出现了IO瓶颈的优化思路

* 设置 binlog_group_commit_sync_delay 和 binlog_group_commit_sync_no_delay_count 参数，减少 binlog 的写盘次数。这个方法是基于 “额外的故意等待” 来实现的，因此可能会增加语句的响应时间，但没有丢失数据的风险。
* 将 sync_binlog 设置为大于1的值（比较常见100~1000）。这样做的风险是，主机掉电会丢失 binlog 日志。
* 将 innodb_flush_log_at_trx_commit 设置为2。这样做的风险是，主机掉电的时候会丢失数据。

> tips：不建议将 innodb_flush_log_at_trx_commit 设置为 0 。因为这样的话，表示 redo log 只保存在内存中，MySQL 本身异常重启也会丢数据，风险太大。而 redo log 写到文件系统的 page cache 的速度也是很快的，所以将这个参数设置成2跟设置成0其实性能差不多，但是这样做 MySQL 异常重启时就不会丢数据了，相比之下风险更小。



生产环境，数据库一般使用的是双1模式，即 `sysnc_binlog =1, innodb_flush_log_at_trx_commit = 1`。表示每次事务提交， binlog 及 redo log 都会执行 fsync 操作。

在某些时候，为了应对临时的高发流量，如果IO成了瓶颈，我们可以试着修改上面的参数来临时应对。

---
title: InnoDB之LRU缓存及SQL状态
date: 2020-11-04 15:45:57
tags: [InnoDB, LRU, processlist]
category: MySQL
---

在 MySQL 中可以使用 show processlist 来观察 sql 的执行状态。

举个例子： 我们现在查询一个很大的表，100G 左右，超过了我们的 16G 内存，那么它是怎么执行的呢？

1. 获取一行，写到 net_buffer 中。这块内存的大小是由参数 net_buffer_length 定义的，默认16Kb。
2. 重复获取，直到 net_buffer 写满，然后就会调用网络接口发送出去。
3. 如果发送成功，就清空 net_buffer，然后继续取下一行，并写入 net_buffer.
4. 如果发送函数返回对方网络栈写满了，就进入等待。直到网络栈重新可写，再继续发送。

由于MySQL 是”边读边发“的。这就意味着如果客户端接收得慢，会导致 MySQL服务端由于迟迟得不到响应，这个事务的执行时间就会变长。就是说如果客户端和服务端网络不佳的情况下，并且又对MySQL查了大量数据，就可能造成 MySQL 的性能急剧下降。

我们使用 show processlist 会看到有关的状态：

<!--more -->
* **Stat 处于 Sending to client**

如果一直处于这状态，说明服务端的网络栈写满了。常常是因为客户端来不及接收导致的。在 MySQL 中客户端使用 --quick 参数，会使用 mysql_use_result 方法。这个方法时读一行处理一行。如果业务的逻辑比较复杂，每一行都需要处理很久，那么久可能导致服务器发送堵塞。如果想减少这种状态的线程，也可以把net_buffer_length参数设置的大一点。

因此一般情况下尽量使用 mysql_store_result 接口，直接把查询结果保存到本地内存会好一些。前提是查询结果返回不多，如果查询结果很多，有好多个G，那还是需要改用 mysql_use_result 接口了。

* **Stat 处于 Sending data**

这个状态其实跟他的名字关联不大，常常被误解。

1. MySQL 查询语句进入执行阶段后，首先把状态设置成 ”Sending data“， 
2. 然后发送执行结果的列相关信息（meta data）给客户端
3. 再继续执行语句的流程
4. 执行完成后，把状态设置成空字符串

以上可以看出，”Sending data“ 并不一定是指”正在发送数据“， 而可能是处于执行器过程中的任意阶段。

```sql
session A:                   												sessionB:

begin;

select * from table where id=1 for update;
																											select * from t lock in share mode;
```

这个时候使用 show processlist 查看就可能显示 "Sending data"，但是B明明是在等待锁。

也就是说，仅当一个线程处于”等待客户端接收结果“的状态，才会显示”Sending to client“；而如果显示”Sending data“， 它的意思只是”正在执行“。

以上仅针对 MySQL server 层的处理逻辑。

* 全表扫描对InnoDB的影响

InnoDB 由于有了 WAL 机制，再配合 redo log，就可以避免随机写盘。

内存中的数据页是在Buffer Pool 中管理，在 WAL 里 Buffer Pool 起到了加速更新的作用。而实际上，Buffer Pool 还有一个更重要的作用就是加速查询。

如果有一个查询要来读刚刚修改的数据页，这个时候最新的数据还在 Buffer Pool 里面，就可以实现直接从内存返回，而不需要去读取磁盘，从而实现了加速查询。衡量 Buffer Pool 的加速效果，可以通过内存命中率来看。

使用 `show engine innodb status` 来查看系统当前的 Buffer Pool 命中率。一般情况下，一个稳定服务的线上系统，要保证响应时间符合要求的话，内存命中率要在 99% 以上。其中 "Buffer pool hit rate" 就表示命中率。

如果查询需要的数据页能够直接从内存得到，那么命中率就是 100%，这一般很难做到。

InnoDB Buffer Pool 的大小是由参数 innodb_buffer_pool_size 确定的，一般建议设置成可用物理内存的 60%-80%。

这个时候再来看看缓存，InnoDB 使用的是LRU 算法，不过对其进行了改进。这算法的核心就是淘汰最近未使用的数据。

如果直接使用 LRU 会怎样？ 假设我们要扫描一个 200G的表，这个表示一个冷表，平时没有业务访问它。那么按照这个算法扫描的话，就会把当前的Buffer Pool 里的数据全部淘汰掉。这时，对于一个正在做业务服务的库，这可不妙。你会看到内存命中率急剧下降，磁盘压力增加，SQL 语句响应变慢。

改进LRU算法之处在于，InnoDB 按照 5：3 的比例将整个 LRU 链表分成了 young 区域和 old 区域。某个数据如果不在链表中，那么第一次先放到 old 区域，如果在 1 秒后，这个数据再次被访问，就将其放在 young 区域。这样就避免了在扫描大表的过程中，将 缓存的正常业务数据给淘汰了。如果是全表扫描，基本上一个内存页一定可以在 1秒中之内完成访问，然后就不会再访问，这样就会在 old 区域不断的添加和淘汰，根本进入不了young区域。 对 old 区域有影响，但是对 young 区域完全没有影响，从而保证了Buffer Pool 响应正常业务的查询命中率。


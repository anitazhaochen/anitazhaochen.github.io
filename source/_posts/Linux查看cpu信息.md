---
title: Linux查看cpu信息
date: 2020-11-06 11:41:47
tags: [Linux]
category: Liunx
---

当需要查看负载情况的时候，总要看一下cpu的硬件信息。其中常说的有物理cpu、逻辑cpu。

物理cpu 就是 cpu 的个数，一般家庭电脑都是只有一个 cpu 的。

cpu 中包含核数，通过 cpu 数量 乘以 核数 就等于逻辑cpu个数了。



可以通过查看 /proc/cpuinfo 来获取 cpu 的详细信息。

1. 查看 cpu 个数：

`grep 'physical id' /proc/cpuinfo | uniq -c | wc -l`
<!--more -->

2. 查看 cpu 核数:

`grep 'cpu cores' /proc/cpuinfo | uniq | awk -F ':' '{print $2}'`

3. 查看逻辑cpu个数：

`grep 'processor' /proc/cpuinfo | wc -l`

cpu个数 * cpu核数 = 逻辑cpu个数


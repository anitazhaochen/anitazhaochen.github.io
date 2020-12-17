---
title: Linux使用find命令查找并删除某天前的文件
date: 2020-12-17 20:11:24
tags: [Linux, find]
category: Linux
---

```shell
$ find /xxx/ -type f -atime +30 -exec rm -f {} \;
```

mtime 表示最后内容修改

ctime 表示最后状态修改

atime 表示最后访问

[m|c|a]time 表示的是天数，

-days 表示距现在 days 内修改过的文件
<!--more -->

days 表示距现在 days前 到 days+1 天 内修改过的文件

+days 表示 days 之前修改过的文件

其中 time 也可以换成 min，时间单位是分钟 [m|c|a]min ,用法同上


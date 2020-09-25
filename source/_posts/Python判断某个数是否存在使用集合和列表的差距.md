---
title: Python判断某个数是否存在使用集合和列表的差距
date: 2020-09-17 17:24:39
tags: [Python, set, list]
category: Python
---

其实大家都知道判断一个数字是否存在，使用集合速度会更快。这次，我实际测试了一下，结果出乎意料，也在意料之中。 出乎意料的是，这个不应该会被底层优化成集合嘛！意料之中的是，不要什么都需要底层优化来帮你优化，其实有的时候，他并不会为我们优化。 正是某些情况如： 现在不需要注意那些了， 底层都会帮你优化的，导致最终性能下降的厉害，毕竟他优化没优化我们也不知道。 说到底还是一句话，写代码规范问题。

```python
#!/usr/bin/python env
# coding:utf8

import time


arr = [i for i in  range(10000)]

def test_list(arr):
    for i in range(10000):
<!--more -->
<!--more -->
        if i in arr:
            pass


def test_set(arr):
    for i in range(10000):
        if i in arr:
            pass



list_arr = arr
set_arr = set(arr)
start = time.time()
test_list(list_arr)
t_list = time.time() - start

start = time.time()
test_set(set_arr)
t_set = time.time() - start

print('列表耗时: ', str(t_list))

print('集合耗时: ', str(t_set))

print('快多少倍: ' , str(t_list // t_set))

python3 执行结果(仅供参考)：

列表耗时:  0.498913049697876
集合耗时:  0.00047206878662109375
快多少倍:  1056.0
```

直接写段代码试下就完事了，简单直观。

规范的重要性油然而生。

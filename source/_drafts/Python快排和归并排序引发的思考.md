---
title: Python快排和归并排序引发的思考
tags: [Python, 数据结构]
category: Python
date: 2018-11-30
---



好久又没刷算法了。勉勉强强记得算法的一些思想。

写的时候，却又不能一次性把它写对，总是有些遗漏与疏忽。

目前掌握排序算法：

​	冒泡排序

​	选择排序

​	插入排序

​	快速排序

​	归并排序

​	快速排序

​	堆排序

​	桶排序



首先，写一个装饰器，来测试：



```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import copy

def getRandom(start=-999, end=999, count=10):
    return [random.randint(start,end) for _ in range(count)]


def compare(func):
    def wrap(arr):
        arr2 = copy.deepcopy(arr)
        arr2 = sorted(arr2)
        print(arr2)
        func(arr)
        print(arr)
        return "sucess" if arr == arr2 else "failed"
    return wrap

```



## 冒泡排序

- 最优时间复杂度：O(n) （表示遍历一次发现没有任何可以交换的元素，排序结束。）
- 最坏时间复杂度：O(n2)
- 稳定性：稳定

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from myutils import *

@compare
def bubbleSort(arr):
    if arr is None or len(arr) == 0:
        return
    length = len(arr)
    for i in range(0,length):
        for j in range(0,length-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

if __name__ == "__main__":
    arr = getRandom(-999, 999, 10)
    print(bubbleSort(arr))

```






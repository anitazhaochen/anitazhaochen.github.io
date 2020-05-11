---
title: python 使用list做list下标交换数值遇到的问题
date: 2018-09-20 15:03:15
tags: [bug, fix]
---

## 代码：

```python
L = 0
nums = [2,1]
#进行交换
nums[L],nums[nums[L]-1] = nums[nums[L]-1], nums[L]
# 列表里的值还是不变
#如果这样，就可以
tmp = nums[L] - 1 
nums[L], nums[tmp] = nums[tmp], nums[L]
```

在python 2,7  和 3.7 实验，均无法交换。

## 究其原因

这个列表只存在两个变量的情况下，确实不好来实验。有可能是因为Python 的交换执行顺序导致没有交换成功。

改进代码一探究竟：

```python
L = 0
nums = [10,0,1,2,3,4,5,6,7,8,9]
nums[L], nums[nums[L] - 1] = nums[nums[L] - 1], nums[L]

# nums: [8, 0, 1, 2, 3, 4, 5, 10, 7, 8, 9]
```

有了结果就可以逆推一遍：

执行顺序是这样的：

```python
nums[L] = nums[nums[L] - 1]
# 此时 nums[L] 的值是 8
nums [ nums[L] - 1 ] = nums[0]
# 此时 nums[L] - 1 的值是 7 , nums[7] 的值就变成了 10
```

从这里例子可以得出，Python 在交换两个数值的时候，会从左向右计算。

这里估计是由于在未交换完成的时候，需要用到交换者本身的数值，所以就没有按照我们常规所想的那样进行交换。


---
title: python list 交换数值遇到bug
date: 2018-09-20 15:03:15
tags: [未解决, bug]
---

# PYTHON list 交换两个元素遇到bug



定义一个变量L

```python
L = 0
nums = [2,1]
#进行交换
nums[L],nums[nums[L]-1] = nums[nums[L]-1], nums[L]
# 列表里的值还是不变
#如果这样，就可以
tmp = nums[L] -1 
nums[L], nums[tmp] = nums[tmp], nums[L]
```

在python 2,7  和 3.7 实验，均无法交换

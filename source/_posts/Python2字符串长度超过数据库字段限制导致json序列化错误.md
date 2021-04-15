---
title: Python2字符串长度超过数据库字段限制导致json序列化错误
date: 2021-03-18 15:44:53
category: Python
tags: [Python]
---

今天突然几个接口报错了。仔细一看是报如下错误：

`**UnicodeDecodeError: 'gbk' codec can't decode bytes in position 8-9: illegal multibyte sequence** `

一看到这个错误立马就想到了 Python2 的编码问题，但是好好的系统看了 GIT 提交记录也没人改过编码方面的代码，接口都是封装好的，突然出现这种情况直接使用 Python2 的字符处理方法可能是处理不了的。 

再看了下，是数据在返回前，要进行 json 序列化，就在序列化这一步报错了。

```
site-packages/simplejson/encoder.py
```

然后就想看看到底是哪些地方序列化失败了，由于数据量非常庞大，这个报错也不会具体指明是哪个数据，所以我就只能使用二分法来调试，最终找到了问题所在，其中某个对象有个name字段，这个name字段出现了乱码。



但是好端端的怎么可能出现乱码呢，顺着猜想打开数据库，desc 了一下表，果不其然，由于 name 字段在代码里没有限制长度，再加上 Python2 直接使用切片是会截断中文造成乱码的，最终存储到数据库里的数据的最后一位就是一个乱码字符，然后在返回的时候json序列化就报错了。



下面我们来看下 Python2 中对中文字符的一些不同：

```python
>>> a = '我是谁'
>>> len(a)
9
>>> len(a.decode('utf-8'))
3
>>>
>>> a.decode('utf8')[0:2].encode('utf8')
```

如果要正确切割中文字符串，应该先 decode 后，再进行切割。

还有就是写代码一定要对输入进行校验。
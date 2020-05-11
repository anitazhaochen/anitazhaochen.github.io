---
title: Python中maketrans源码记录
date: 2019-10-14 16:34:45
tags: [Python]
category: Python
---

## 首先举个例子

```python
from string import maketrans

a = 'abcde'
b = '12345'

trantab = maketrans(a, b)

str = 'abcdefag'

print str.translate(trantab)

# 输出 12345f1g
```

<!--more -->
* maketrans 的作用是生成一张映射表，上面这个例子生成的是 将 a 换为 1， b换为2，c换为3，d换为4，e换为5的。

  需要保证 a 字符串的长度和b字符串的长度是一样的，否则会抛出异常。

* str.translate() 方法的作用是执行一个替换功能，接收一个替换表。

## maketrans 如何生成一张表

源码：

```python
# Construct a translation string
l = map(chr, xrange(256)) # map 接收一个函数和一个迭代器，chr函数是根据数值转换为对应的 ascii 编码
#值为：
# ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', '\xa0', '\xa1', '\xa2', '\xa3', '\xa4', '\xa5', '\xa6', '\xa7', '\xa8', '\xa9', '\xaa', '\xab', '\xac', '\xad', '\xae', '\xaf', '\xb0', '\xb1', '\xb2', '\xb3', '\xb4', '\xb5', '\xb6', '\xb7', '\xb8', '\xb9', '\xba', '\xbb', '\xbc', '\xbd', '\xbe', '\xbf', '\xc0', '\xc1', '\xc2', '\xc3', '\xc4', '\xc5', '\xc6', '\xc7', '\xc8', '\xc9', '\xca', '\xcb', '\xcc', '\xcd', '\xce', '\xcf', '\xd0', '\xd1', '\xd2', '\xd3', '\xd4', '\xd5', '\xd6', '\xd7', '\xd8', '\xd9', '\xda', '\xdb', '\xdc', '\xdd', '\xde', '\xdf', '\xe0', '\xe1', '\xe2', '\xe3', '\xe4', '\xe5', '\xe6', '\xe7', '\xe8', '\xe9', '\xea', '\xeb', '\xec', '\xed', '\xee', '\xef', '\xf0', '\xf1', '\xf2', '\xf3', '\xf4', '\xf5', '\xf6', '\xf7', '\xf8', '\xf9', '\xfa', '\xfb', '\xfc', '\xfd', '\xfe', '\xff']

_idmap = str('').join(l)  # 将列表转化为字符串

del l
...........若干不相关代码.......
_idmapL = None
def maketrans(fromstr, tostr):  #接收两个字符串参数
    """maketrans(frm, to) -> string

    Return a translation table (a string of 256 bytes long)
    suitable for use in string.translate.  The strings frm and to
    must be of the same length.

    """
    if len(fromstr) != len(tostr): #判断长度是否相等
        raise ValueError, "maketrans arguments must have same length"
    global _idmapL
    if not _idmapL:  # 第一次初始化，将刚才生成的 ascii 码赋值给它，以后就不需要初始化了。
        _idmapL = list(_idmap)
    L = _idmapL[:]  # 复制出来一个新列表，对原有列表操作不影响
    fromstr = map(ord, fromstr) # 字符串转 ascii
    for i in range(len(fromstr)): 
        L[fromstr[i]] = tostr[i] # 将对应位置的 ascii 进行替换
    return ''.join(L) # 返回根据位置替换后的列表
```

## 情景1：

如果 a = 'aabbcc'， b = '123456' ，生成 c = maketrans(a, b) ，那么替换 a 的结果是：  224466。

如果出现重复的，源码告诉我们，后面的值会覆盖前面的值。

## 应用

可以用在一些加密的场景之中。

```python
def get_table(key):
    m = hashlib.md5()
    m.update(key)
    s = m.digest()
    (a, b) = struct.unpack('<QQ', s)
    table = [c for c in string.maketrans('', '')] # 生成一张 ascii 码列表
    for i in xrange(1, 1024): # 混合排序 1024遍
        table.sort(lambda x, y: int(a % (ord(x) + i) - a % (ord(y) + i))) 
    return table 

encrypt_table = ''.join(get_table('foobar!'))  # 加密的时候按照这张表进行替换 明文 ——-> table 替换
decrypt_table = string.maketrans(encrypt_table, string.maketrans('', '')) # 解密按照这种表进行替换  密文 --> 明文 
```


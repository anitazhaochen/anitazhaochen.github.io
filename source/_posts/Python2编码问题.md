---
title: Python2编码问题
date: 2019-10-24 10:10:28
tags: [Python, unicode]
category: Python
---

最近工作的老项目使用的是 Python2，在处理中文的时候，遇到了一些编码错误，在这里总结一下。

在 Python2 中，一个字符串可能为 str 或者 unicode 。 

```python
a = '你好'
type(a) # 输出 <type 'str'>
repr(a) # 输出 "'\\xe4\\xbd\\xa0\\xe5\\xa5\\xbd'"
a = u'你好'
type(a) # 输出 <type 'unicode'>
repr(a) # 输出 "u'\\u4f60\\u597d'"
```

<!--more -->
我们发现，在字符串前面加 ’u‘ 和不加，它的类型及原始字符串都是不一样的。

```python
a = u'你好'
repr(a)  # 输出 "u'\\u4f60\\u597d'"
a.encode('unicode-escape').decode('string_escape')
# 输出 '\\u4f60\\u597d'
# 上面是 unicode 转为 str

a = '你好'
repr(a)  # 输出 "'\\xe4\\xbd\\xa0\\xe5\\xa5\\xbd'"
a.decode('unicode-escape') 
# 输出  u'\xe4\xbd\xa0\xe5\xa5\xbd'
```

str 类型通过 decode 可以变成字节类型，但是在 Python2 中是不区分 str 和 byte 的。比如：

```python
a = b'abc'
type(a)  # 输出 <type 'str'>

a = 'abc'
type(a)   # 输出 <type 'str'>
```

而在 Python3 中：

```python
a = b'abc'
type(a) # 输出  <class 'bytes'>
a = 'abc'
type(a) # 输出  <class 'str'>
```

## 概念

* 字符

character 构成文本的最小组成单元， 即每一个字符。

* 字节

byte 数据在计算机内部的存储单元，一个字节等于一个8位的比特，计算机中所有数据都是由字节组成。如：在UTF-8编码下，一个字符可能由多个字节构成，而在 ASCII 编码下，每个字符都是由一个字节构成。

一个字节等于 8个 比特位， 每个比特位只能表示 0 或者 1 ，所以 1 个字节可以表示最多255种组合，ASCII 只有一百多个字符，所以完全够了。而 UTF-8 需要表示的是全世界的字符，比如中文字符（一个汉字），英语、法语、俄语等等，所以一个字节是肯定不够的，中文字符都几万个。所以就出现了 unicode ，而 UTF-8、UTF-16 都只不过是 unicode 的一种实现，这里不去深究。

[UTF-8和Unicode的区别](https://www.jianshu.com/p/36d20de2a1ee)

* 字符集

比如 gb2312， Unicode、 ASCII 他们都是字符集，就是由多个字符组成的一个集合。每个集合的映射关系并不是完全相同的。

* 字符编码值

不同的字符集规定了不同的编码规则，编码规则中规定了字符对应的编码值 code point，一个整数值。

* 编码

将字符集中的字符码根据 code point 映射为字节流（byte sequence）的一种实现。 简而言之就是通过映射关系，将人看的懂的字符转化为计算机能识别的二进制字符。举个例子： 如 ’严' 的码值在 UTF-8 中对应的是 4E25 ，这是一个16进制的数字， 占两个字节，编码后翻译成二进制就是 100111000100101 。而具体到底最后翻译成什么样的数值和形式， 需要看编码具体实现，这里不去深究。

* 解码

将字节流解析为字符集中的字符

## 实际中遇到的问题

先总结一下，在 Python2 中抛出异常，我们遇到的错误基本是是这两种错误：

*  UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)
*  UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)

我们发现，不是 UnicodeDecodeError 就是UnicodeEncodeError 。

如何去解决问题：需要知道在什么情况下才会这样。 你可能知道，一个浮点数和一个整数做运算的时候，它不会报错，但是它会把整数转换为浮点数，然后在进行计算。而字符串也是同理，在 Python2 中有着 str 和 unicode 两种类型的字符串，甚至还可以像下面这样做：

```python
'%sabc%s'%(123.0, 'abc')
```

直接拼接一个浮点数，和一个字符串都可以，就是因为它先帮我们把所有类型统一成一个类型，然后再进行拼接。

下面分析一下在交互式环境中：

```python
'%sabc%s'%(123, u'哈哈')
# 这句话是不会报错的

'%s你好%s'%(123, u'123')
# 而这句话，就会抛出异常，发现是 UnicodeDecodeError 异常
```

这个时候，不要着急，异常已经给你指明了方向，你不需要去查看这句代码之外的地方，首先告诉你的是 DecodeError ，什么时候才会发生 解码呢，应该是 str 类型变成原来的unicode 的时候，所以，问题就出在了 "你好" 这两个字符上面，因为 Python2 默认的编码是 ASCII ，在 ASCII 字符集里面并没有 ”你好“ 这两个字符的映射关系，所以就报错了。

```python
'%s123%s'%(u'你好', '哈哈')
# 这句话也户报错， 因为同样是 在对 ’哈哈‘ 进行 decode 的时候 默认的 ascii 没有这个字符。

'%s123%s'%(u'你好', u'哈哈')
# 如果改成这样，除了 ascii 字符（’123‘），其他字符都是 unicode，拼接的时候，不做任何处理，是不会报错的，因为不涉及转换问题。

# 验证我们的猜想，错误是因为 系统对 '哈哈' 替我们使用了 ascii 进行了编码

'%s123%s'%(u'你好', '哈哈'.decode('utf-8'))
# 这样执行时没问题的。

# 得出结论，我们执行的是第一种情况，实则是执行的，这样的代码

'%s123%s'%(u'你好', '哈哈'.decode('ascii'))

# 再次验证看看 上面这行代码，返回的结果类型是 unicode 还是 str。
c = '%s123%s'%(u'你好', '哈哈'.decode('utf-8'))
type(c)  # 输出 unicode
```

结论，当字符中包含 unicode 和 str 的时候， Python 会帮我们把 非 unicode 转换为 unicode，而使用过的编码为默认的 ascii 编码，所以在含有 ascii 之外的字符的时候，就会出现 UnicodeDecodeError 。

## 总结

当遇到编码错误的时候，首先错误的原因一定是使用了错误的字符集进行了 编码或者解码。

调试的时候，通过查看变量的类型，大概可以知道哪个值发生隐式转换的时候，发生了错误。然后在手动对它进行额外的操作即可解决。

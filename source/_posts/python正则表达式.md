---
title: Python之正则表达式
date: 2017-08-12 01:58:23
tags: [python, 正则表达式]
category: Python
---

~~~python
# coding=utf-8

# 导入re模块
import re

# 使用match方法进行匹配操作
result = re.match(匹配规则,要匹配的内容)

<!-- more -->

# 如果上一步匹配到数据的话，可以使用group方法来提取数据
result.group()
~~~

re.match() 是用来进行正则匹配检查的方法，若字符串匹配正则表达式，则match方法返回匹配对象（Match Object），否则返回None（注意不是空字符串""）



匹配对象Match Object具有group方法，用来返回字符串的匹配部分。

示例1：匹配以apple开头的语句：

~~~python
#coding=utf-8

import re

result = re.match("apple","appleorange banana")
result.group()
# 运行结果
# apple
~~~

说明：

* re.match() 能够匹配出以xxx开头的字符串



# 表示字符



字符			功能

.				匹配任意1个字符（除了\n)

[]				匹配[]中列举的字符

\d				匹配数字，即0--9

\D				匹配非数字

\s				匹配空白，即空格，tab键

\w				匹配单词字符，即a-z、A-Z、0-9、_

\W				匹配非单词字符

[^]				表示只要不是集合里的元素就可以

[a-z5-9]			表示26个字母和5、6、7、8、9

\d = [0-9]

~~~
# 表示数量
# 匹配多个字符的相关格式
*			匹配前一个字符出现0次或者无限次
+			匹配前一个字符出现1次或者无限次
？			匹配前一个字符出现1次或者0次
{m}			匹配前一个字符出现m次
{m,}		匹配前一个字符至少出现m次
{m，n}		匹配前一个字符出现从m到n次

~~~

示例1：  匹配出，一个字符串第一个字母为大写字符，后面都是小写字母并且这些小写字母可有可无：

~~~python
# coding=utf-8

import re

ret = re.match("[A-Z][a-z]*")

~~~

示例2：匹配出，变量名是否有效：

~~~python
#coding=utf-8

import re

ret = re.match("[A-Za-z_]+\w*")
~~~

示例3： 匹配出，0到99之间的数字

~~~python
#coding=utf-8
import re

ret = re.match("[1-9]?\d$|^100$")
~~~

示例4：匹配出，8到20位的密码，可以是大小写英文字母、数字、下划线

~~~python
#coding=utf-8
import re

ret = ret.match("[a-zA-Z0-9_]{8,20}","1sdasfsdf2323")
~~~





# 原始字符串

~~~python
s = '\nabc'
re.match("\\\\nabc",s)
re.match(r"\nabc",s)
# 加一个r 表示原始字符串，可以忽略需要转义的地方
~~~

* 说明：

  python中字符串前面加上 r 表示原生字符串，与大多数编程语言相同，正则表达式里使用“\"作为转义字符，这就可能造成反斜杠困扰。假如你需要匹配文本中的字符”\"，那么使用编程语言表示的正则表达式里需要3个反斜杠”\\\\":前两个和后两个分别用于在编程语言里转义程反斜杠，转换成两个反斜杠后再在正则表达式里转义成一个反斜杠。

  python里的原生字符串很好的解决了这个问题，有了原始字符串，再也不用担心是不是漏写了反斜杠，写出来的表达式也更直观。

# 表示边界：

字符				功能

^					匹配字符串的开头

$					匹配字符串的结尾

\b					匹配一个单词的边界

\B					匹配非单词边界

# 表示分组：

~~~
|					匹配左右任意一个表达式
(ab)				将括号中的字符作为一个分组
\num				引用分组num匹配到的字符串
(?P<name>)			分组起的别名
(?P=name)			引用别名为name分组匹配到的字符串

~~~

示例：

~~~python
# 匹配出<html><h1>hello</h1></html>

import re

ret = re.match(r"<(\w*)><(\w*)>.*<(/\1)><(/\2)>","<html><h1>hello</h1></html>")
ret.group()
# 给分组设置别名
ret = re.match(r"<(?P<name1>\w*)><(?P<name2>\w*)>.*</(?P=name1)></(?P=name2)>","<html><h1>hello</h1></html>")
# 注意字母P是大写
~~~



# re模块的高级用法

* search

  如：匹配出文章阅读的次数

  ~~~python
  # coding=utf-8
  import re

  ret = re.search(r"\d+","阅读次数为 1000")
  ret.group()
  ~~~

* findall

  找出所有数字信息：

  ~~~python
  #coding=utf-8
  import re

  ret = re.findall(r"\d+","a = 1 ,b = 20 ,c = 100")
  print(ret)
  ~~~

  ​

* sub将匹配到的数据进行替换

  ~~~python
  # 第一种方法
  #coding=utf-8
  import re

  ret = re.sub(r"\d+",'199','read = 198')

  # 第二种 将匹配得到的结果传入函数replace中，用函数的返回值进行替换
  def replace(result):
      num = int(result)
      return str(num+1)
  re.sub(r"\d+", replace, "a = 2,b = 3")
  ~~~



* split 根据匹配进行切割字符串，返回一个列表

  ~~~python
  import re

  ret = re.split(r":| ","info:haha 22 aabbcc")
  print(ret)
  ~~~

  ​

# python贪婪和非贪婪

python里数量词默认是贪婪的，总是尝试尽可能多匹配字符，非贪婪则相反

解决方式：非贪婪操作符”？”，这个操作符可以用在“*”，“+”，“？”的后面，要求匹配的越少越好。 



题目： 构建一个类Foo 用python的魔法方法实现

class Foo()

print(Foo().welcome.hello.world)

welcome hello world

~~~python
# coding=utf-8

class Foo():
    def __init__(self):
        pass
    
    def __getattr__(self,item):
        print(item,end=" ")
        return self
    
    def __str__(self):
        return ""
~~~



题目：有一些网址，需要如

https://www.baidu.com/1123/332/as.asp?id=32

需要正则后为：

https://www.baidu.com

~~~python
#coding=utf-8
import re

ret = re.match(r"(https://.*?)/.*",lambda x:x.group(1),"https://www.baidu.com/1123/332/as.asp?id=32")
print(ret)

~~~

题目：找出单词

apple orange   banana hello world

~~~python
#coding=utf-8
import re

ret = re.split(r"\s+","apple orange   banana hello world")
~~~




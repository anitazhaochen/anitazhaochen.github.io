---
title: Python装饰器装饰类
date: 2020-03-12 00:08:30
tags: [Python, 装饰器]
category: Python
---



```python
class PrintClassName(object):

    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kwargs):
        """
        如果在类中实现了 __call__ 方法，那么实例对象就是一个可调用对象。 相当于  PrintClassName() 的时候回执行 __call__ 的内容
        """
        print('我是 PrintClassName')
<!--more -->
        print(self._cls.__name__)
        return self._cls(*args, **kwargs)


@PrintClassName
class Person(object):
    def __init__(self, a):
        print('执行 Person __init__')
        self.value = a

    def sing(self):
        print(self.value)


person = Person('今天又是充满希望的一天')
person.sing()
"""输出:
我是Foobar类
我是 PrintClassName
Person
执行 Person __init__
"""

"""
执行流程:  1. 创建 Person 前，先创建 PrintClassName，执行 __init__ 方法
					2. 执行 PrintClassName 的 __call__ 方法
					3. __call__ 返回创建 Person 的 type ，开始创建 Person ，执行 Person 的 __init__方法
					4. person 自己调用 singl() 方法
					
					看一下传入的东西是什么: 加入下面这句话到 PrintClassName 的 __init__ 方法里。
					print(type(cls))
					输出  
					<class 'type'>
					说明传入的是创建 Person 使用的 type 。

"""

```

总结： 

​		装饰器装饰类的时候，其实是在创建类对象之前，执行装饰器里的操作，并且把创建类的 type 对象传递进去， 装饰器执行完后，返回创建对象的东西，然后才会创建对象。


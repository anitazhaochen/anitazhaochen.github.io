---

title: Python新式类及通过继承修改源码
date: 2019-12-13 11:00:36
tags: [Python]
category: Python
---

## 新式类和经典类

在 Python 2.x 中默认都是经典类，在 Pyhton 3.x 中默认都是新式类

**新式类和经典类的区别:**  只有显示继承了 object 才是新式类

用法上的区别:

* 新式类对象可以直接通过  `__class__` 属性获取自身类型为 type

```python
# coding:utf8

# 新式类
class demo(object):
    pass

print demo.__class__

经典类
class demo1:
    pass

print demo1.__class__

<type 'type'>     # 新式类的输出
Traceback (most recent call last):   # 经典类不包含 __class__ 属性
  File "1demo.py", line 13, in <module>
    print demo1.__class__
AttributeError: class demo1 has no attribute '__class__'
```
<!--more -->



* 继承搜索的顺序发生了改变，经典类多继承属性搜索顺序： 先深入数左侧，返回，再开始找右侧； 新式类多继承属性搜索顺序：先水平搜索，然后再向上移动。（经典类采用深度优先搜索的方式，新式类采用广度优先搜索）

  举例：

  ```python
  # 此实验基于 Python2 
  class A:
  
      def test(self):
          print "A_test"
  
  class B:
  
      def test(self):
          print "B_test"
  
  class C(A):
      pass
  
  class D(C,B,A):
      pass
  
  d = D()
  d.test()
  
  # 输出 A_test  ， D 没有继承 object 表示经典类，使用深度优先搜索， 搜索顺序是  D --> C 然后 C --> A
  
  # 如果将D类改一下:
  
  class D(object,C,B,A):
      pass
  
  # 输出 B_test   ,表示先搜索 C ，然后并没有沿着C继续搜索A，而是开始搜索 B ，即广度优先搜索。
  
  ```



* 新式类增加了 `__slots__` 属性， 可以把实例属性的种类锁定到 `__slots__` 规定的范围之中。
* 新式类增加了 `__getattribute__` 方法



## Python2 中初始化父类构造方法

```python
  class MyClass(libClass): 
  		def __init__(self, *args, **kwargs):
          #super(MyStats, self).__init__(*args, **kwargs)
        	libClass.__init__(self, *args, **kwargs)
        
# 使用 super 会报错。
```

[Python super() raises TypeError](https://stackoverflow.com/questions/489269/python-super-raises-typeerror)

* super() 函数是用于调用父类(超类)的一个方法。
* super 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，会涉及到查找顺序，重复调用等种种问题[当心掉进Python多重继承里的坑](https://www.jianshu.com/p/71c14e73c9d9)



当子类继承了父类，子类重写了父类的 `__init__` 方法，但是大多数子类不仅要拥有自己的初始化代码，还要拥有超类的初始化代码。父类的构造方法在子类中是不会被自动调用的，需要子类专门去调用父类的构造方法，这样擦能将父类正确初始化。反之，如果子类不实现自己的 `__init__` 方法， 那么子类就会自动去调用父类的 `__init__` 方法。

* 子类含有 `__init__` 方法的情况下，想要使用父类初始化函数里面的变量.

  ```python
  # python2  经典类, 即未显式继承 object 的类
  class MyClass(libClass):
    def __init__(self, *args, **kwargs):
      libClass.__init__(self, *args, **kwargs)
  
  # python2 父类继承了 object 或者 Python3 默认已经继承object
  class MyClass(libClass):
    def __init__(self):
      super(MyClass,self)__init__(self)
  ```

* 如果是多重继承， python2 和 python3 的 `__init__` 方法调用方式也不一样，是因为查找父类的方式不一样，前面已经说了。 执行隐式方法的查找顺序也不一样，简称 MRO。 不太建议使用多重继承。

* 如果需要在子类中执行父类的`__init__`方法，必须显示执行
* 说 Python3 继承搜索是一种广度表里优先的方式，不太准确[具体遍历方式C3](https://www.cnblogs.com/whatisfantasy/p/6046991.html)



### %r  和 %s 的区别

%r 使用 rper() 方法处理对象

%s 用 str()  方法处理对象

有些情况下两者处理的结果是一样的，比如 Int 对象

```
print "hello %d"%2020  # hello 2020
print "hello %s"%2020  # hello 2020
print "hello %r"%2020  # hello 2020
```

字符串对象就不同了:

```python
print "hello %s"%"world"    # hello world
print "hello %r"%"world"    # hello 'world'
```

可以看出 %r 对 字符串加了 引号。

%r 打印时能够重现它所代表的对象

```python
import datetime
d = datetime.date.today()
print "%s"%d   #  2019-12-17
print "%r"%d   #  datetime.date(2019, 12, 17)
```



### sys.stdout 

可以为一个 io流赋值给 sys.stdout，然后通过 print 就可以像这个流中写入数据。 

```python
sys.stdout = iostream

print "hello"
```








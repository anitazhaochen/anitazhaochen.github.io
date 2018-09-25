---
title: python模块、深浅拷贝、私有化、property
date: 2017-06-05 00:07:36
tags: [python]
category: python
---

# PYTHON 深拷贝浅拷贝等等

进入python交互模式



```  python 
# python 
>>> import sys
>>>sys.path
['', '/usr/local/Cellar/python/2.7.14/Frameworks/Python.framework/Versions/2.7/lib/python27.zip',...]
```

<!-- more -->


在输出结果中可以看到import导包时直接查找的一些路径。


可以使用 sys.path.append("/home")  把/home路径加入搜索路径

* 模块重新导入 
    修改模块之后，加入新功能，需要重新导入模块
    * from imp import *
    * reload(test)
    * 重新加载即可

* 导包应该避免循环导入
* python3 == 和 is  判断内容的时候用 == 来判断两个值是否相同，判断是否同一个的时候用is
```python
    >>> a = [11,22,33]
    >>> b = [11,22,33]
    >>> a == b
    True
    >>> a is b
    False
    >>> id(a)
    4308094128
    >>> id(b)
    4308230800
    >>> c = a
    >>> id(c)
    4308094128
    >>> c=  [22]
    >>> a
    [11, 22, 33]
    >>> id(c)
    4308230944
    >>> id(a)
    4308094128
    >>> a is c
    False
    >>>
```

* 深拷贝、浅拷贝




~~~python
a = [11,22,33]
b = a
id(a)
4308230800
id(b)
4308230800
#两个变量进行赋值，没有真正进行空间的拷贝，而是指向了同一个内存，则是浅拷贝。
import copy
c = copy.deepcopy(a)
id(c)
4308231016
id(a)
4308230800
#通过导入copy模块完成深拷贝，c并没有指向a指向的内存，而是开辟了一个新的空间。
~~~

* 当我们不想进行值共享的时候的拷贝应该用深拷贝。



~~~python
a = [11,22,33]
b = [44,55,66]
c = [a,b]
d =c
id(c)
4306318040
id(d)
4306318040
c is d
True
c 里面存的是 a和b的引用，即c 里面存的是 指向a，指向b
import copy
e = copy.deepcopy(d)
id(e)
4306318256
id(d)
4306318040
a.append(55)
c[0]
[11, 22, 33, 55]
e[0]
[11, 22, 33]
~~~



既然拷贝的是内容，那么深拷贝却没有拷贝c里面的引用，这是因为递归拷贝，就是如果里面存的是引用就会继续拷贝。
如果想要拷贝引用，不进行递归拷贝，仅仅拷贝第一层，则可使用  e = copy.copy(a)
例如：



~~~python
>>>
a = [1,2,3]
b = [4,5,6]
c = [a,b]
e = copy.copy(c)
a.append(10)
c
[[1, 2, 3, 10], [4, 5, 6]]
e
[[1, 2, 3, 10], [4, 5, 6]]
id(c)
4306320056
id(e)
4306320488
a = [1,2]
b = [3,4]
c = (a,b)
d = copy.copy(c)
id(c)
4306146584
id(d)
4306146584
a.append(5)
a
[1, 2, 5]
c
([1, 2, 5], [3, 4])
d
([1, 2, 5], [3, 4])
#如果拷贝的内容是不可变内容，如元祖，则第一层拷贝都不会拷贝，这里d直接指向了c。使用copy模块的copy功能的时候，它会根据当前拷贝的数据类型是可变类型还是不可便类型有不同的处理方式。
~~~



例： 出现这个问题：是因为 在负几到100多之间，是公用的。



~~~python
  a = 100
  b = 100
  a is b
  True
  a == b
  True
~~~



# 私有化

* xx ：公有变量
* _x： 单前置下划线，私有化属性或方法，from module import * 禁止导入，类对象和子类可以访问
* __xx: 双前置下划线，避免与子类中的属性命名冲突，无法再外部直接访问（名字重整所以访问不到），表示私有。
* __xx__:双前后下划线，用户名字空间的魔法对象或属性。例如 __init__ 系统给的，一般不要这么给自己的变量起名
* xx_:单后置下划线，用于避免与Python关键词的冲突
* 通过name mangling （名字重整（目的就是以防子类意外重写基类的方法或者属性）如_Class__object）机制就可以访问private了。python自动把变量名改了，所以就用不到私有变量了，可以通过 _类名__num 来访问。




# 私有属性使用property升级getter和setter方法
~~~ python
class Test(object):
    def __init__(self):
        self.__num = 1
    def setNum(self,newNum):
        self.__num = newNum
        
    def getNum(self):
        return self.__num
        
    num = property(getNum,setNum) #相当于 t.num 调用的就是getNum() 或者setNum()
    
t.num = 2 #就可以用
~~~

property 用法二：

~~~python
class Money(object):
    def __init__(self):
        self.__money = 1
    @property  #相当于 getMoney()
    def money(self):
        return self.__money
    
    @money.setter  #相当于setMoney()
    def money(self,value):
        if isinstance(value,int):
            self.__money = value
        else:
            print("error")
~~~

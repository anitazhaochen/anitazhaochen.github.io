---
title: python单例设计模式
date: 2017-07-29 14:09:56
tags: [python, 设计模式]
category: python
---


<!-- more -->
~~~python

# new 方法执行一次。
class Dog(object):
    __instance = None
    
	def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        	return cls.__instance
		else:
            # return 上一次创建对象的引用
            return cls.__instance
            
a = Dog()
print(id(a))
b = Dog()
print(id(b))

# 版本二  new 方法 和 init 都执行一次
class Dog(object):
    __instance = None
    __inin_flag = False
	def __new__(cls,name):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        	return cls.__instance
		else:
            # return 上一次创建对象的引用
            return cls.__instance
    def __init__(self,name):
        if Dog.__init_flag == False:
        	self.name = name
        	Dog.__init_flag = True
  
            
a = Dog("gou1")
print(a.name)
b = Dog("gou2")
print(b.name) 

~~~

### python异常处理

~~~python
#python2的异常处理
try:
    print(num)
    print("___1____")
except 异常的名字:
    print("如果捕获到异常处理的方式")
    
    
#python3异常处理
try:
    open("xxx.txt")
    print("111")
except (NameError,FileNotFoundError):  #多个异常用元祖
    print("如果捕获到异常后的处理")
except Exception:
    print("如果用了Exception，那么意味着只要上面的except没有捕获到的异常，这个except一定会捕获到")
else:
    print("没有异常会执行的功能")
finally:
    print("一定会执行的代码")
    
#python 抛出自定义异常
class ShortInputError(Exception):
    def __init__(self,mlength,length):
        self.maxlength = mlength
        self.length = length
        
try:       
  s = input("请输入")
  if len(s) > 3:
      rsise ShortInputException(3,len(s))
except ShortInputException as result:
      print('ShortInputException：输入字符串的长度为%d,最大长度为%d'(result.length,result.maxlength))
else:
    print("没有发生异常")

~~~

## 导入模块

~~~python
import xxx  #使用前要加导入的模块名
xxx.xx()
from xxx import aaa   #使用的时候直接用aaa
aaa()
from xxx import * # 不建议使用，如果有两个类有相同名字的方法
from xxx import aaa,bbb,ccc   #可以导入多个方法
import xxx as  bbb   #可以给模块取一个别名进行调用
bbb.xx()

#在一个模块里，使用 __all__ = ["xxx","xxx"]别人 使用 from xx import *的时候，只能用[]里的东西 
~~~



写模块的时候，自己写的一些测试代码不想让别人导入的时候执行可以使用

~~~python
#写代码的格式
import xxx
class ClassName(object):
    """ docstri
    ng for ClassName"""
    def __init__(self,arg):
        super(ClassName,self).__init__()
        self.arg = arg
	def xxx():
        sss
def main():
	pass
if __name__ == "__main__"
 	main()
~~~

给程序传参：

~~~python
import sys
sys.argv  #接收传进来的参数，传进来的是一个列表[]
~~~

列表生成式：

~~~
a = [i for i in range(1,20)]  #生成1到19的列表
c = [i for i in range(1,20) if i%2==0]
d = [i for i in range(3) for j in range(3)]
e = [(i,j) for i in range(2) fro j in range(2)]
~~~


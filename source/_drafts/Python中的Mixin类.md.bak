---
title: Python中的Mixin类
date: 2020-08-18 10:29:40
tags: [Python, Mixin]
category: Python
---

由于 Python 是支持多继承的，而 Mixin 类就是利用了这种特性。

Mixin 类是只包含了一组特定的函数组合，我们将其与其他类进行混合，从而生成一个适用于实际需要的新类。



直接上 code 更好理解：

```python
#!/usr/bin/python env
# coding:utf8

class A(object):
<!--more -->

    def say(self, word):
        print('I am A')
        print('say' + word)


class AMixin(object):

    def eat(self, food):
        print('eat ' + food)

    def say(self, word):
        super().say(word + 'from mixin')
        print('i am AMixin')



class B(AMixin, A):
    pass



b = B()

b.say('hello')


# 这是 Python3 的语法

# 执行结果：

I am A
sayhellofrom mixin
i am AMixin
```

以上执行结果说明了一个问题，就是  AMixin 的父类并不是 A ，但是竟然可以调用 A 的 say 方法。 

是因为 B 同时继承了 AMixin 和 A ， 这就是 Mixin 类的作用。 



而 Mixin 类为什么可以执行到 A 的 say 方法呢，在多重继承的环境下， super() 有相对来说更加复杂的语义。它会查看你的继承链， 使用一种叫做 Methods Resolution Order（方法解析顺序）的方式，来决定调用最近的继承父类的方法。

也就是说super().method() 与 self.method() 是差不多的，只是 super().method() 需要跳过当前类而已。

参考：

感谢 [Python 的 Mixin 类](https://blog.csdn.net/u012814856/article/details/81355935)


---
title: Flask之MethodView解析
date: 2020-03-12 18:27:16
tags: [Python, Flask, MethodView]
category: Flask
---

## 可插拔视图

MethodView 主要可以实现两个功能：

* 基于方法调度

    对于 RSET 式 API 来说，继承 MethodView 后，每个 HTTP 方法都映射到一个同名的函数(函数名称为小写字母)。可以在类里面定义 get、post、delete、put 等方法。使用这种方式，不必提供 methods 属性，它会自动使用相应的类方法。

* 装饰视图

    自 FLask 0.8 版本开始，新加了一种选择：在视图类中定义装饰的列表：

    ```python
<!--more -->
    class UserAPI(MethodView):
      decorators = [user_decorator]
    ```

    请牢记：因为从调用者的角度来看，类的 self 被隐藏了，所以不能在类的方法上单独 使用装饰器。（是这个类里面定义的方法不能使用装饰器吗? 但是我如果继承自 UserAPI 后，新的类里面方法还是可以使用装饰器）

    

[官方文档](https://dormousehole.readthedocs.io/en/latest/views.html)


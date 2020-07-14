---
title: Python常用的测试方法
date: 2020-07-14 17:13:59
tags: [Python, 单元测试]
category: Python
---

## doctest

简介： doctest 是 Python 自带的一个模块，可以嵌入到 Python 源码中，或者放到独立文件中进行测试。

* 嵌入到 Python 源码中

```python
# -*- coding: utf-8 -*-

"""
这是一个测试案例
"""

<!--more -->

def multiply(a, b):
    """

    Args:
        a:
        b:

    Returns:

    >>> mutiply(4, 3)
    12
    >>> mutiply(4, 3)
    13

    """
    return a * b

if __name__ == "__main__":
    import doctest
    # verbose 表示在执行测试的时候会输出详细信息, 包括成功案例 ,设为 False, 只输出失败案例
    doctest.testmod(verbose=True)

```

* 放到单独的文件中

```python
# file_name test.txt
>>> from start import multiply
>>> multiply(3, 4)
12
>>> multiply(4, 3)
13
```

目前，这种测试方法，我用的比较多的地方是在写算法的时候，或者写一个比较简单的函数的时候，可以直接将 测试语句写到函数声明下面来验证函数的对错。

## Pytest

目前较为流行的单元测试框架，上手容易。

* 安装

  `pip install pytest`

* 规则

  测试文件以 test_ 开头（或以 _test 结尾）

  测试类以 Test 开头，并且不能带有 `__init__` 方法

  测试函数以 test_ 开头

  断言使用基本的 assert 即可

* 使用方法

  **作用域方面：**

  fixture 的 scope 参数

  scope 参数有四种

  function: 每个 test 都运行，默认是 function 的 scope

  class: 每个 class 的所有 test 只运行一次

  module： 每个 module 的所有 test 只运行一次

  session： 每个 session 只运行一次

  **执行前和执行后的操作**

  setup 和 teardown 操作

  setup： 在测试函数或类之前执行，完成准备工作

  teardown，在测试函数或者类之后执行，完成收尾工作

  * 执行方法

  ```shell
  pytest # run all tests below current dir
  pytest test_mod.py # run tests in module file test_mod.py
  pytest somepath # run all tests below somepath like ./tests/
  pytest -k stringexpr # only run tests with names that match the
  # the "string expression", e.g. "MyClass and not method"
  # will select TestMyClass.test_something
  # but not TestMyClass.test_method_simple
  pytest test_mod.py::test_func # only run tests that match the "node ID",
  # e.g "test_mod.py::test_func" will be selected
  # only run test_func in test_mod.py
  
  ```


* 其他用法

  通过@pytest.mark控制需要执行哪些feature的test，例如在执行test前增加修饰@pytest.mark.website

  执行的时候，可以通过 -m 执行所有标记的方法

  -m "website"  表示执行所有 website 标记的test方法

  -m "not website" 表示执行没有 website 标记的 test 方法

* 代码实例

  ```python
  # -*- coding: utf-8 -*-
  
  import pytest
  
  
  @pytest.fixture(scope='function')
  def setup_function(request):
      def teardown_function():
          print('teardown_function called.')
  
      print('setup_function called')
  
  
  @pytest.fixture(scope='module')
  def setup_module(request):
      print('setup_module called.')
  
  
  @pytest.mark.website
  def test_1(setup_function):
      print('Test_1 called.')
  
  
  def test_2(setup_module):
      print('Test_2 called.')
  
  
  def test_3(setup_module):
      print('Test_3 called.')
      assert 2 == 1 + 1
  
  ```

  

## Unittest

在 Flask 项目中，使用的是 Flask 官方推荐的测试框架，其底层基于  Werkzeug，我们可以使用 Unittest 进行封装后，实现 GET、POST 方法进行模拟发送请求，进行测试。

这种测试方式，这种测试很方便， 但是也仅仅适用于对接口的测试。必要时候，还是需要使用 Jmeter 进行带有逻辑的测试。



单元测试方面，对于小型项目使用 Unittest 封装就可以在 view 层进行单元测试。




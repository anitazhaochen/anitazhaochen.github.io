---
title: 深入理解GIL
tags: [Python, GIL]
category: [Python]
date: 2018-11-9
---



## 并行与并发的区别

并发： 在一个**时间段**内要处理多个任务。

并行： 在同一**时刻**要同时处理多个任务。比如 CPU 每一个核跑一个线程。

- 并发性(concurrency)，又称共行性，是指能处理多个同时性活动的能力，并发事件之间不一定要同一时刻发生。
- 并行(parallelism)是指同时发生的两个并发事件，具有并发的含义，而并发则不一定并行。

[并发与并行的区别](https://www.jianshu.com/p/b11e251d3dc7)

<!--more -->
> 由于线程是操作系统直接支持的执行单元。Python 的线程是真正的 Posix Thread，而不是模拟出来的线程。

[Python进程和线程基础](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014319272686365ec7ceaeca33428c914edf8f70cca383000)



## GIL 是什么？

官方：

> In CPython, the **global interpreter lock**, or **GIL**, is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once. This lock is necessary mainly because CPython's memory management is not thread-safe. (However, since the GIL exists, other features have grown to depend on the guarantees that it enforces.)

GIL 的全称为 **global interpreter lock** ， 即全局解释器锁。 CPython 的线程库直接封装了操作系统的原生线程。

这是一个用于保护 Python 内部对象的全局锁（在进程空间中唯一），保障了解释器的线程安全。

**注意：**

> GIL 并不并不是 Python 的特性，它是实现 Python 解析器（CPython）时所引入的一个概念。比如 C 语言，它的编译器有 GCC、Visual C++ 等。Python 也一样，解释器 CPython 就是一种实现，JPython 就没有 GIL。之所以大家都喜欢把 Python 和 GIL 放在一起，是因为 CPython 是大部分环境下默认的 Python 执行环境。



**GIL** 的本质就是一把互斥锁，既然是互斥锁，所有互斥锁的本质都一样，都是将**并发运行**变成串行，以此来控制同一时间内共享数据只能被一个“任务”所修改，进而保证数据安全。

在一个 Python 的进程内，不仅有 xxx.py 的主线程或者由该主线程开启的其他线程(多线程)，还有解释器开启的垃圾回收等解释器级别的线程，总之，所有线程都运行在这一个进程内。

如果多个线程的 target=xxxx，那么执行流程是多个线程先通过访问到解释器的代码，即拿到执行权限，然后将 target 的代码交给解释器的代码去执行。



## GIL 的存在导致了什么问题

Python 是支持多线程的。

GIL 保证了线程安全性，但很显然也带来了一个问题：每个时刻只有一个线程在执行，即使在多核架构中也是如此。毕竟，解释器只有一个。如此一来，单进程多线程的 Python 程序便无法利用到多核的优势了。所以 Python 的多线程显得鸡肋。

为了控制变量，可以使用两个线程来串行执行。即一个线程跑完了在开启一个线程在跑一次。

```python
from threading import Thread
import time
import os

def my_counter():
    i = 0
    for _ in range(100000000):
        i = i + 1

def main():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        t.join()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    main()
    # Python 模拟两个线程，一个线程跑完再跑另一个线程，模拟单线程执行。
    
➜  /tmp python 3.py
Total time: 7.85346484184
```



多线程执行。 两个线程同时开启执行。

```python
#! /usr/bin/python

from threading import Thread
import time
import os

def my_counter():
    i = 0
    for _ in range(100000000):
        i = i + 1
    return True

def main():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        t.join()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))

if __name__ == '__main__':
    main()
    
    # Python 多线程执行，两个线程并发执行。
➜  /tmp python 4.py
Total time: 14.8255028725
```

测试环境： MBP 2018款 6 核 CPU

发现，多线程同时执行，速度比串行执行慢了一倍。

总结：GIL 不仅无法利用多核 CPU 实现真正的并行，并且多核还会让速度变得更慢。



继续验证：

```python
from threading import Thread
a = 0
def test():
    global a
    for _ in range(1000000):
        a = a+1
def test2():
    global a
    for _ in range(1000000):
        a = a-1

t1 = Thread(target=test)
t2 = Thread(target=test2)
t1.start()
t2.start()
t1.join()
t2.join()
print a

```

运行结果：

```shell
➜  /tmp python 5.py
time = 0.164122104645
-206968   
```

竟然不是0，而是 -206968。每次运行结果都可能不一样。

我们修改一下代码：

```python
from threading import Thread, Lock
import time

a = 0
def test():
    global a
    for _ in range(1000000):
        if mutex.acquire(True):
            a = a+1
            mutex.release()
def test2():
    global a
    for _ in range(1000000):
        if mutex.acquire(True):
            a = a-1
            mutex.release()

mutex = Lock()
t1 = Thread(target=test)
t2 = Thread(target=test2)
start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print "time = "+str(end - start)
print a
```

运行结果：

```shell
➜  /tmp python 5.py
time = 3.93809294701
0
```

这个结果是 0 ，结果是对了，但是一看时间，足足慢了 25 倍左右。

就是因为加了一个锁。我们在改一下代码，看看就用主线程单线程来跑相同的运算会是什么样的。

```python
import time

a = 0
start = time.time()
for _ in range(1000000):
    a = a + 1
for _ in range(1000000):
    a = a - 1
end = time.time()
print a
print "time=" + str(end-start)
```

运行结果：

```shell
➜  /tmp python 7.py
0
time=0.134548902512
```

结果肯定是正确的 0，时间比第一次的还快一点点呢。

由于 GIL 的存在，本来多线程可以节省时间的事情，变得比单线程还慢了，究其原因为什么会这样呢，

加锁之后，就会存在锁的性能开销，并且也会存在上下文切换的耗时。



## 为什么要使用 GIL ？

通过前面的验证，我们发现， GIL 存在以下问题：

​	多线程程序运行在多核 CPU 上面却无法得到性能的提升，并且性能还会下降。

 它是**解释器全局锁**，但是它并不是用来加锁保证用户级数据的安全，而是线程之间的执行安全。

由于 Python 是解释形动态语言，所以在实现线程时，需要 PyThreadState 结构来保存一些信息：

当前的 stack frame (对 Python 代码)
当前的递归深度
线程ID
可选的 tracing/profiling/debugging hooks

PyThreadState 其实是C语言实现的一个结构体。

可以简单的理解为控制上面的这些数据安全来实现线程与线程间的安全。



## 继续探索，GIL 到底是什么呢？

这些问题也是曾经我不停追问，一定要弄懂的问题。

首先：先说锁的问题，为什么有了 GIL 我们还需要加锁？

​	其实对于这个问题，一开始就搞错了，我们对我们的数据比如 `a = a+1` 加锁，这可以理解为用户级数据，我们通过加用户级锁来保护我们的数据的安全。而 GIL 是什么？ 它是**全局解释器锁**，解释器是干什么的？ 它是执行 Python 字节码的。所以问题就清楚了， GIL 的出现时为了保证线程与线程之间的执行安全，而保证我们数据安全则需要我们自己加其他的锁。

> 用户级互斥与同步：
>
> ​	Python 的线程在 GIL 的控制之下，线程之间，对整个 Python 解释器，对 Python 提供的 C API 的访问，都是互斥的，这可以看作是 Python 内核级的互斥限制，但是这种互斥是我们不能控制的，我们还需要另一种可控的互斥机制——用户级互斥。内核级通过 GIL 实现的互斥保护了内核的共享资源，同样，用户级互斥保护了用户程序中的共享资源。       
>
> 《Python源码剖析》



说白了就是 GIL 锁和我们编程的时候用的锁，并不是同一个概念。

GIL 是为了保证线程与线程之间的安全，要保存线程的状态，以及其他关于线程的属性。

而我们需要用用户级锁来保证数据安全。（我们担心线程竞争我们的资源造成数据有误）

##   GIL 很不完美，却迟迟没有废除，原因如下：

Python 的应对很简单，以不变应万变。在最新的 python 3 中依然有 GIL。

CPython 的 GIL 本意是用来保护所有全局的解释器和环境状态变量的。如果去掉 GIL，就需要多个更细粒度的锁对解释器的众多全局状态进行保护。或者采用 Lock-Free 算法。无论哪一种，要做到多线程安全都会比单使用 GIL 一个锁要难的多。而且改动的对象还是有 20 年历史的 CPython 代码树，更不论有这么多第三方的扩展也在依赖 GIL。对 Python 社区来说，这不异于重新来过。

有位牛人曾经做了一个验证用的 CPython，将 GIL 去掉，加入了更多的细粒度锁。但是经过实际的测试，对单线程程序来说，这个版本有很大的性能下降，只有在利用的物理 CPU 超过一定数目后，才会比 GIL 版本的性能好。这也难怪。单线程本来就不需要什么锁。单就锁管理本身来说，锁 GIL 这个粗粒度的锁肯定比管理众多细粒度的锁要快的多。而现在绝大部分的 python 程序都是单线程的。再者，从需求来说，使用 python 绝不是因为看中它的运算性能。就算能利用多核，它的性能也不可能和 C/C++ 比肩。费了大力气把 GIL 拿掉，反而让大部分的程序都变慢了，这不是南辕北辙吗。

关于如何解决 GIL 的问题：下面文章有提到。

[python之GIL与多线程](https://blog.csdn.net/nbaDWde/article/details/80713819)

[从伪并行的 Python 多线程说起](https://segmentfault.com/a/1190000013646127)

[知乎Python有GIL为什么还需要线程同步？](https://www.zhihu.com/question/23030421)

[Stack Overflow 关于 GIL 的讨论](https://stackoverflow.com/questions/40072873/why-do-we-need-locks-for-threads-if-we-have-gil/40072999#40072999)

[知乎-线程与全局解释器锁（GIL）](https://zhuanlan.zhihu.com/p/42327048)

[简书Python GIL深入浅出](https://zhuanlan.zhihu.com/p/42327048)

[Python（CPython）为什么存在 GIL？](https://blog.windrunner.me/python/gil.html)

## 如果一个进程里面每一个线程都有一个全局解释器锁会怎么样？

为什么不直接用多进程呢！！

关于 Python 的字节码：

[Python字节码](https://docs.python.org/3/library/dis.html#python-bytecode-instructions)

参考：

[GIL权威解答 PDF](http://www.dabeaz.com/python/GIL.pdf)

[Python 官网 GIL](https://wiki.python.org/moin/GlobalInterpreterLock)


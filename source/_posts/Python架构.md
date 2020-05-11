---
title: Python 架构
tags: [Python]
category: Python
date: 2018-11-6
---

## Python 的总体架构


<!--more -->
![image-20181221145237786](/images/image-20181221145237786-5375157.png)
Python 的整体架构分为三个主要部分。

左边：是 Python 提供的大量的模块、库以及用户自定义的模块，比如在执行 import os 时，这个 os 就是 Python 内建的模块。

右边： 是 Python 的运行时环境，包括对象/类型系统、内存分配器和运行时状态信息。运行时状态维护了解释器在执行字节码时不同的状态（比如正常状态和异常状态）之间的切换动作。

中间：Python 的核心——解释器，或者称为虚拟机。在解析器中，箭头的方向指示了 Python 运行过程中的数据流方向。Scanner 对应此法分析，将文件输入的 Python 源代码或从命令行输入的一行行 Python 代码切分为一个个的 token； Parser 对应语法分析，在 Scanner 的分析结果上进行语法分析，建立抽象语法树 （AST）; Compiler 是根据建立的 AST 生成指令集合 —— Python 字节码。一次， Code Evaluator 又可以成为虚拟机。

在解释器与右边的对象/类型系统、内存分配之间的箭头表示“使用”关系；而与运行时状态之间的箭头表示“修改”关系，即 Python 在执行的过程中会不断修改当前解释器所处的状态，在不同的状态之间切换。

Python 源代码中：

![image-20181221150049860](/images/image-20181221150049860-5375649.png)

Include: 该目录包含了 Python 提供的所有头文件，如果用户需要自己用 C 或者 C++ 来编写自定义模块扩展 Python，那么就需要用到这里提供的头文件。

Lib： 该目录包含了 Python 自带的所有标准库，Lib 中的库都是用 Python 语言编写的。

Modules：该目录办函了所有用 C 语言编写的模块，比如 random，cStringIO 等。这个模块中是那些对速度要求非常严格的模块，而又一些对速度没有太严格要求的模块，比如 os，就是用 Python 编写，并且放在 Lib 目录下的。

Parser： 包含了 Python 解释器中的 Scanner 和 Parser 部分，即对 Python 源代码进行词法分析和语法分析的部分。除了这些，Parser 目录下还包含一些有用的工具，这些工具能够根据 Python 语言的语法自动生成 Python 语言的词法和语法分析器，与 YACC 非常相似。（yacc，是Unix/Linux上一个用来生成编译器的编译器。yacc生成的编译器主要是用C语言写成的语法解析器）

Objects：包含了 Python 的所有内建对象，包括整数、list、dict 等。同时，该目录还包括了 Python 在运行时需要的所有内部使用对象的实现。

Python：包含了 Python 解释器中 Comiler 和执行引擎部分，是 Python 运行的核心所在。



## Python 内的对象

在 Python 中，对象就是为 C 中的结构体在堆上申请的一块内存，一般来说，对象是不能被静态初始化的，并且也不能在栈空间上生存，唯一的例外就是类型对象， Python 中所有的内建的类型对象（如证书类型对象，字符串类型对象）都是被静态初始化的。

Python 中，一个对象一旦被创建，它在内存中的大小就是不变的了，这就意味着那些需要容纳可变长度数据的对象只能在对象内维护一个指向一块可变大小的内存区域的指针。



## 对象机制的基石- PyObject

在 Python 中所有东西都是对象，而所有的对象都拥有一些相同的内容，这些内容在 PyObject 中定义， PyObject 是整个 Python 对象机制的核心。

```c
[object.h]
typedef struct _object {
	PyObject_HEAD
} PyObject;

// PyObject_HEAD 指向的是一个宏定义
```

实际发布 Python 中，PyObject 定义如下：

```c
[object.h]
typedef struct _object {
    int ob_refcnt;
    struct _typeobject *ob_type;
}
```

在 PyObject 的定义中，整型变量 ob_refcnt 与 Python 的内存管理机制有关，它实现了基于引用计数的垃圾收集机制。 ob_type 是指向 _typeobject 结构体的指针，这个结构体对应着 Python 内部的一种特殊对象，它用来制定一个对象类型的类型对象。

总结对象机制的核心： 一个引用计数，一个就是类型信息。

在 PyObject 中定义了每一个 Python 对象都必须有的内容，这些内容将出现在每一个 Python 对象所占有的内存的最开始的字节中。但是，还有可能包含其他内容，如整数对象：

```c
[intobject.h]
typedef struct {
	PyObject_HEAD
	long ob_ival;
} PyIntObject
```

ob_ival 用来保存这个 int 对象的具体数值。

其他对象，如字符串、list、dict 对象、成千上万的其他对象，都在 PyObject 之外保存了属于自己的特殊的信息。



## 定义变长对象

Python 在 PyObject 对象之外，还有一个表示这类对象的结构体----PyVarObject:

```c
[object.h]
#define PyObject_VAR_HEAD \
	PyObject_HEAD
	int ob_size;

typedef struct {
    Pyobject_VAR_HEAD
} PyVarObject;
```

整数对象不包含可变长度数据的对象称为 “定长对象”，而字符串对象包含可变长度数据的对象称为“变长对象”。

在 Python 内部，每一个对象都拥有相同的对象头部，这就使得 Python 中，对对象的引用变得非常的统一，我们只需要使用一个 PyObject * 指针就可以引用任意的一个对象。而不论该对象实际是一个什么对象。

![image-20181221142141595](/images/image-20181221142141595-5373301.png)



## 类型对象

内存中存在某一个 Python 对象时，该对象开始的几个字节的含义一定会复合我们的预想。但是，当分配内存时，需要申请多大的空间，这显然在 PyObject 中没有这样的信息。其实，它是隐藏于 PyObject 之中。它出现在对象所属类型的对象中。即 _typeobject 中：

```c
[object.h]
typedef struct _typeobject {
	PyObject_VAR_HEAD
	char *tp_name;
	int tp_basicsize, tp_itemsize;
	...
	destructor tp_dealloc;
	printfunc tp_print;
	...
	hashfunc tp_hash;
	ternaryfunc tp_call;
	...
} PyTypeObject;
```

在 _typeobject 的定义中包含了许多信息，主要分为4类：

* 类型名， tp_name ，主要是 Python 内部以及调试的时候使用；
* 创建该类型对象时分配内存空间大小的信息，即 tp_basicsize 和 tp_itemsize;
* 与该类型对象相关联的操作信息（诸如 tp_print 这样的许多的函数指针）
* 类型的类型信息

实际上，一个 PyTypeObject 对象就是 Python 中面向对象理论中“类”这个概念的实现。



## 对象创建

一类为： AOL (Abstract Object Layer)。这类 API 都具有诸如 PyObject_ *** 的形式，可以应用在任何 Python 对象身上。

如： `PyObject* intObject = PyObject_New(PyObject, &PyInt_Type)`。

另一类: COL (Concrete Object Layer)。这类 API 通常只能作用在某一种类型的对象上，对于每一种内建对象，Python 都提供了这样的一组 API。比如对于整数对象，可以这样创建： `PyObject *intObj = PyInt_FromLong(10)`

这样就创建了一个值为 10 的整数对象。



## 对象的行为

在 PyTypeObject 中定义了大量的函数指针，这些函数指针最终都会指向某个函数，或者指向 NULL。这些函数指针可以视为类型对象中所定义的操作，而这些操作直接决定着一个对象在运行时所表现出的行为。

## 类型的类型

在 Python 中，任何一个东西都是对象，而每一个对象都是对应一种类型的，那么类型对象的类型对象是什么呢？ 实际上，是 PyType_Type。

```
<type 'type'> 就是 Python 内部的 PyType_Type ，它是所有 class 的 class，所以它在 Python 中被称为 metaclass 。如在 Django ORM 中就使用了元类(metaclass)。
```












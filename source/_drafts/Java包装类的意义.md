---
title: Java包装类的意义
date: 2019-10-11 11:33:31
tags: [java]
category: [java]
---

## Java是一门面向对象的语言

为什么包装/封装原始类呢?

广义上,对于封装而言，一个对象它所封装的是自己的属性和方法，所以它是不需要依赖其他对象就可以完成自己的操作。

使用封装有如下好处：

1、良好的封装能够减少耦合。

2、类内部的结构可以自由修改。

3、可以对成员进行更精确的控制。

4、隐藏信息，实现细节。



包装类与原始类不同。例如，在Java中，变量可以声明为数据类型(double、short、int等)，而包装类则**创建继承但隐藏原始数据类型的实例化对象和方法，而不是分配数据类型值的变量**。

因此，术语[基本包装类]并不意味着包装类是原始类。**它应该被理解为一个包装原始类型的类。**包装类可以用来存储与原始类型变量相同的值，但是包装类本身的实例/对象本身是非原始的。我们不能说包装类本身是原始类型。他们只是包装原始类型。

Byte、Short、Integer、Long、Float和Double包装类都是Number类的子类。

包装类BigDecimal和BigInteger不是原始包装类之一，而是不可变的。

------





狭义上举个栗子:

int 是基本数据类型（面向过程留下的痕迹，不过是对java的有益补充），Integer 是一个类，是int的扩展，定义了很多的转换方法。

类似的还有：float Float;double Double;string String等，而且还提供了处理 `int` 类型时非常有用的其他一些常量和方法

举个例子：当需要往ArrayList，HashMap中放东西时，像int，double这种内建类型是放不进去的，因为容器都是装Object的，这是就需要这些内建类型的外覆类/包装类了。

Java中每种内建类型都有相应的外覆类/包装类。

Java中int和Integer关系是比较微妙的。关系如下：

　　1、int是基本的数据类型；

　　2、Integer是int的封装类；

　　3、int和Integer都可以表示某一个数值；

　　4、int和Integer不能够互用，因为他们两种不同的数据类型；

举例说明

　　ArrayList al=new ArrayList();

　　int n=40;

　　Integer nI=new Integer(n);

　　al.add(n); //不可以

　　al.add(nI); //可以

并且泛型定义时也不支持int: 如：

List<int> list = new ArrayList<int>(); //不可以

List<Integer> list = new ArrayList<Integer>(); //可以 

总而言之：如果我们定义一个int类型的数，只是用来进行一些加减乘除的运算or作为参数进行传递，那么就可以直接声明为int基本数据类型，但如果要像对象一样来进行处理，那么就要用Integer来声明一个对象，因为java是面向对象的语言，**因此当声明为对象时能够提供很多对象间转换的方式，与一些常用的方法。**自认为java作为一们面向对象的语言，我们在声明一个变量时最好声明为对象格式，这样更有利于你对面向对象的理解。

[知乎](https://www.zhihu.com/question/22775729)



## 基本数据类型

int 、 float、double、boolean、long、short、byte、char

Java 八中基本数据类型。基本数据类型！！说明这些不属于对象。

而 Integer 等属于对象。





大致就是 面向过程的语言有面向过程的好处，面向对象有面向对象的好处，在某些时候， 把两种东西用在同一个原材料上面，会更好。
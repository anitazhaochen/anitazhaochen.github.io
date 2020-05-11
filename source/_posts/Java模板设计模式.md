---
title: Java模板设计模式
date: 2019-01-19 19:08:09
tags: [Java, 设计模式]
category: Java
---



# 模板设计模式

模板（Template）设计模式：

模板模式就是定义一个算法的骨架，而具体的算法延迟到子类中来实现

**优点**

使用模板方法模式，在定义算法骨架的同事，可以很灵活的实现具体的算法，满足用户灵活多变的需求

**缺点**
<!--more -->

如果算法骨架有修改的话，则需要修改抽象类



### 示例

**计算代码执行时间**

```java
package com.enjoyms.template;


public class Main {

    public static void main(String[] args) {


        long start = System.currentTimeMillis();
        for (int i = 0; i < 100000; i++) {
            System.out.println(i);
        }
        long end = System.currentTimeMillis();
        System.out.println("总耗时: "+ (end-start) +"毫秒");

        // 如何计算 for 循环代码块的耗时，或者计算一个 方法的耗时。 通过模板设计模式实现

        /*
        *  设计一个计算耗时的模板
        * */

        Test test = new Test();
        System.out.println(test.getScheduleTime());

    }
}


abstract class TimeTemplate {
    // 获取执行的时间
    public long getScheduleTime(){
        long start = System.currentTimeMillis();
        code();
        long end = System.currentTimeMillis();
        return end-start;
    }

    public abstract void code();
}

class Test extends TimeTemplate {

    @Override
    public void code() {

        for (int i = 0; i < 1000000; i++) {

            System.out.println(i);
        }

    }
}

```


---
title: Java工厂模式
tags: [Java, 设计模式]
category: Java
date: 2019-1-19
---



## 工厂方法模式的概述和使用

### 工厂方法模式概述

​	工厂方法模式中抽象工厂类负责定义创建对象的借口，具体对象的创建工作由继续抽象工厂的具体类实现。

**优点**

​	客户端不需要再负责对象的创建，从而明确了各个类的职责

​	如果有新的对象增加，只需要维护一个具体的类和具体的工厂类即可，不影响已有的代码
<!--more -->

​	后期维护容易，曾倩了系统的扩展性

**缺点**

​	需要额外的编写代码，增加了工作量

**示例演示**

工厂方法模式中抽象工厂负责定义创建对象的接口。

创建 AnimalFactory 接口：

```java
package com.enjoyms.Factory;

public interface  AnimalFactory {

    public Animal createAnimal();
}

```

创建 Animal 抽象类：

```java
package com.enjoyms.Factory;

public abstract class Animal {
	
    public abstract void eat();
}

```

创建 Dog 类：

```java
package com.enjoyms.Factory;

public class Dog extends Animal{

    @Override
    public void eat() {

        System.out.println("吃狗粮");
    }
}

```

创建 Pig 类：

```java
package com.enjoyms.Factory;

public class Pig extends Animal{
    @Override
    public void eat() {
        System.out.println("吃猪粮");

    }
}

```

创建狗工厂实现类 DogFactory：

```java
package com.enjoyms.Factory;

public class DogFactory implements AnimalFactory {
    @Override
    public Animal createAnimal() {
        Dog dog = new Dog();
        return dog;
    }
}

```

创建猪工厂实现类 PigFactory：

```java
package com.enjoyms.Factory;

public class PigFactory implements AnimalFactory{
    @Override
    public Animal createAnimal() {
        Pig pig = new Pig();
        return pig;
    }
}

```

Main 方法进行对象创建：

```java
package com.enjoyms.Factory;

public class Main {
    public static void main(String[] args) {

        // 以前创建对象的方式
        Dog dog = new Dog();
        dog.setName("阿黄");
        dog.setColor("黄色");
        Pig pig = new Pig();
        pig.setName("佩奇");
        pig.setColor("粉色");
        dog.eat();
        pig.eat();

        // 使用工厂方法模式创建对象

        System.out.println("-----------");
        DogFactory dogFactory = new DogFactory();
        Dog dog1 = (Dog) dogFactory.createAnimal();
        PigFactory pigFactory = new PigFactory();
        Pig pig1 = (Pig) pigFactory.createAnimal();
        dog1.eat();
        pig1.eat();
        
    }
}

```

在 Animal 类中添加两个属性：

```java
package com.enjoyms.Factory;

public abstract class Animal {

    private String name;
    private String color;
    public abstract void eat();

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }
}

```



如果需要多次创建对象那么每次都需要手动设置属性，并且无法做到改一处达到所有地方都修改，所以可以把属性交给工厂来做，修改 DogFactory 和 PigFactory：

```java
package com.enjoyms.Factory;

public class DogFactory implements AnimalFactory {
    @Override
    public Animal createAnimal() {
        Dog dog = new Dog();
        dog.setColor("黄色");
        dog.setName("小黄");
        return dog;
    }
}

```

PigFactory 略。

这样还会存在一个问题，就是必须 new 出对应的工厂，然后调用方法进行对象获取。

###  简单工厂模式

**简单工厂模式概述**

又称静态工厂方法模式，它定义一个具体的工厂类负责创建一些类的实例

**优点**

客户端不需要再负责对象的创建，从而明确了各个类的职责

**缺点**

这个静态工厂类负责所有对象的创建，如果有新的对象增加，或者某些对象的创建方式不同，就需要不断的修改工厂类，不利于后期维护

**示例演示**

创建 AnimalFactory 静态工厂类 AnimalFactoryStatic：

```java
package com.enjoyms.Factory;

public class AnimalFactoryStatic {

    public static Dog createDog() {
        Dog dog = new Dog();
        return dog;
    }

    public static Pig createPig(){
        Pig pig = new Pig();
        return pig;
    }
}

```

通过简单工厂模式创建对象：

```java

        Dog dog3 = AnimalFactoryStatic.createDog();
        Pig pig3 = AnimalFactoryStatic.createPig();
```


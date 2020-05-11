---
title: Java 类加载及反射
date: 2019-01-19 16:14:42
tags: [Java, 类加载流程,反射机制]
category: Java
---



## 类加载

当程序要使用某个类时，如果该类还未被加载到内存中，则系统会通过 <u>加载，连接，初始化三步</u> 来实现对这个类进行初始化。

**加载**

是指将 class 文件读入内存，并为之创建一个 Class 对象。 任何类被使用时系统都会建立一个 Class 对象。

![image-20190119164554374](/images/image-20190119164554374.png)

**连接**
<!--more -->

* **验证** 是否有正确的内部结构，并和其他类协调一致

* **准备** 负责为类的静态成员分配内存，并设置默认初始化值

* **解析** 将类的二进制数据中的符号引用替换为直接引用

  > 符号引用：符号引用以一组符号来描述引用的目标，符号可以是任何形式的字面量，只要使用时能够无歧义的定位到目标即可。
  >
  > 直接引用： 直接指向目标的指针、相对偏移量、一个能间接定位到目标的句柄
  >
  > 直接引用是和虚拟机内存的布局相关的，童一个符号引用在不同的虚拟机示例上翻译出来的直接引用一般会不同。如果有了直接引用，那么引用的目标必定已经被载入内存中了。
  >
  > 在编译时，Java 类并不知道所引用的类的实际地址，因此只能使用符号引用来代替。
  >
  > 各种虚拟机实现的内存布局可能有所不同，但是它们能接受的符号引用都是一致的，因为符号引用的字面量形式明确定义在 Java 虚拟机规范的 Class 文件格式中。



### 类加载的时机

* 创建类的实例 

  new Person()

* 访问类的静态变量，或者为静态变量赋值

  Integer.MAX_VALUE

* 调用类的静态方法

  Executors.newCachedThreadPool()

* 初始化某个类的子类

  new Person() 。 Person extends Human

* 直接使用 java.exe 命令来运行某个主类

  java HelloWrold

* 使用反射形式来强制创建某个类或接口对应的 java.lang.Class 对象

  Classs.for("com.enjoyms.Person")

遵循原则 **需要时才加载**

### 类加载器

类加载器负责将 .class 文件加载到内存中，并为之生成对应的 Class 对象。

**类加载器的分类**

* Bootstrap ClassLoader 根类加载器

  也被称为引导类加载器，负责 Java 核心类的加载

  比如 System.String 等。在 JDK 中 JRE 的 lib 目录下 rt.jar 文件中

* Extension ClassLoader 扩展加载器

  负责 JRE 的扩展目录中 jar 包的加载

  在 JDK 中 JRE 的 lib 目录下 ext 目录

* System ClassLoader 系统类加载器

  负责在 JVM 启动时加载来自 java 命令的 class 文件，以及 classpath 环境变量所指定的 jar 包和类路径

  比如我们自己写的 class 文件就是这个加载器负责加载

  

## 反射

JAVA 反射机器是在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法

对于任意一个对象，都能通过反射调用它的任意一个方法和属性

这种动态获取信息以及动态调用对象的方法的功能称为 java 语言的反射机制

要想解刨一个类，必须先要获取到该类的字节码文件对象

解刨使用的就是 Class 类中的方法，所以先要获取到每一个字节码文件对应的 Class 类型的对象 

**通过反射加载类的三种方式**

* Object 类的 getClass() 方法，判断两个对象是否是同一字节码文件
* 静态属性 class，锁对象
* Class 类中静态方法 forName() 读取配置文件



**演示**

先创建一个 Person 类来演示：

```java
package com.enjoyms.reflect;

public class Person {

    private String name;
    public int age;

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                '}';
    }

    public Person(String name) {
        this.name = name;
    }
}

```

创建 Main 方法类通过三种不同方式创建：

```java
package com.enjoyms.reflect;

import java.io.BufferedReader;
import java.io.FileReader;

public class Main {
    public static void main(String[] args) throws Exception {

        // 1. Object 类的 getClass() 方法
        Person person1 = new Person();
        Class clz1 = person1.getClass();

        // 2. 静态属性 class
        Class clz2 = Person.class;

        // 3. Class 类中的静态方法 forName()
        Class clz3 = Class.forName("com.enjoyms.reflect.Person");

        // 通过打印 hashCode 来判断是同一 Class 对象
        System.out.println(clz1.hashCode());
        System.out.println(clz2.hashCode());
        System.out.println(clz3.hashCode());

        // Class 类中静态方法 forName() 读取配置文件,直接写死文件,这样不好，应该把 className 放在配置文件中。
        
        String className = "com.enjoyms.reflect.Person";
        Class clz = Class.forName(className);
        
        // 在同一个包中创建 info.txt 文件，并写入 com.enjoyms.reflect.Person
        // 通过读取配置文件 info.txt 文件内容获取 className，更加灵活
        FileReader fr = new FileReader("info.txt");
        BufferedReader br = new BufferedReader(fr);
        String className1 = br.readLine();
        Class clz11 = Class.forName(className1);

    }
}
```

**通过反射获取构造方法**

```java
package com.enjoyms.reflect;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
// 如果是 java.lang 包内的类，不需要导入，直接可以使用。 但是如果是它的内部的其他包，则需要导入。

public class Main1 {
    public static void main(String[] args) throws NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        // 通过反射获取带参数构造方法并使用
        /*
        *
        * 反射： 用于获取类的方法和属性
        * 1. 先要获取字节码对象
        * 2. 通过字节码对象的 getConstructor() 方法
        * 3. 构造方法对象 (Contructor)，有个 newInstance() 方法创建这个字节码对象
        * 4. 反射在 import java.lang.reflect 这个包中
        * */

        // 1. 获取字节码对象
        Class clz = Person.class;

        // 2.1 获取构造方法
        Constructor c1 = clz.getConstructor();

        // 2.2 通过构造方法创建对象
        Person person = (Person) c1.newInstance();
        System.out.println(person);

        // 2.3 获取有参构造方法,参数写数据类型，如 String.class、double.class 等等
        Constructor c2 = clz.getConstructor(String.class);
        Person person1 = (Person) c2.newInstance("小明"); // 相当于调用 new Person("小明")
        System.out.println(person1);

    }
}

```

**通过反射获取成员属性和设置成员属性**

```java
package com.enjoyms.reflect;

import java.lang.reflect.Field;

public class Main3 {
    public static void main(String[] args) throws NoSuchFieldException, IllegalAccessException {
        // 通过反射获取成员变量（属性）并使用

        // 1. 获取字节码对象
        Class clz = Person.class;

        // 2. 使用 getField() 只可以获取公共字段（public 字段） age 字段。
        Field ageFiled = clz.getField("age");
        System.out.println(ageFiled);

        //3. 通过反射给字段赋值
        Person person = new Person();
        ageFiled.set(person,30);
        System.out.println(person);

        // 4. 获取私有属性
        Field nameField = clz.getDeclaredField("name");
        System.out.println(nameField);

        //5. 通过反射给私有属性赋值
        nameField.setAccessible(true);
        nameField.set(person,"小红");
        System.out.println(person);

        // 如果 Person 类没有 get、set 方法，依旧可以利用反射进行赋值

        //6. 通过反射获取私有属性的值
        Object value = nameField.get(person);
        System.out.println(value);


    }
}

```

通过反射获取方法，并且越过泛型检查：

```java
package com.enjoyms.reflect;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

public class Main2 {
    public static void main(String[] args) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        // 通过反射越过泛型检查

        // 1. 声明泛型集合
        List<Integer> list = new ArrayList<Integer>();

        list.add(1);
        list.add(2);
        list.add(3);

        // list.add("hello") 会报错

        // 通过反射向集合添加字符串
        // 2.1 获取字节码对象 （Class）
        Class clz = list.getClass();

        // 2.2 通过反射获取方法
        Method method = clz.getMethod("add", Object.class);

        // 2.3 调用方法
        method.invoke(list,"hello");
        System.out.println(list);

        // 输出  [1, 2, 3, hello]
    }
}

```

**通过反射写一个通过的方法，设置对象属性**

```java
package com.enjoyms.reflect;

import java.lang.reflect.Field;

public class Main4 {
    // 通用方法，设置对象属性

    // 通过反射给私有属性赋值
    public static void setFieldValue(Object obj, String fieldName, String fieldValue){
        // 1. 获取字节码
        Class clz = obj.getClass();

        try {
            // 2. 获取属性 Field
            Field field = clz.getDeclaredField(fieldName);

            //3. 设置权限
            field.setAccessible(true);

            //4. 赋值属性
            field.set(obj, fieldValue);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

```


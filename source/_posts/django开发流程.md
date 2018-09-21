---
title: django开发流程
date: 2017-08-14 22:13:16
tags: [python, Django, 开发]
category: python
---

* 开发流程

  step1：创建虚拟环境

  step2：安装django

  step3：创建项目

<!-- more -->

  step4：创建应用

  step5：在model.py中定义模型类

  step6：定义视图

  step7：配置url

  step8：创建模板

* ORM简介

  * MVC框架中包括一个重要的部分，就是ORM，它实现了数据模型与数据库的解耦，即数据类型的设计不需要依赖于特定的数据库，通过简单的配置就可以轻松更换数据库。
  * ORM是“对象-关系-映射”的简称，主要任务是：
    * 根据对象的类型生成表结构
    * 将对象、列表的操作，转换为sql语句
    * 将sql查询到的结果转换为对象、列表
  * 这极大的讲清了开发人员的工作量，不需要面对因数据库变更而导致的无效劳动
  * Django中的模型包含存储数据的字段和约束，对应着数据库中唯一的表



# 开发流程

1. 在models.py中定义模型类，要求继承自models.Model
2. 在应用中加入settings.py文件的installed_app项
3. 生成迁移文件
4. 执行迁移生成表
5. 使用模型类进行crud操作



# 定义模型

* 在模型中定义属性，会生成表中的字段
* django根据属性的类型确定以下信息：
  * 当前选择的数据库支持字段的类型
  * 渲染管理表单时使用的默认html控件
  * 在管理站点最低限度的验证
* django会为表增加自动增长的主键列，每个模型只能有一个主键列，如果使用选项设置为主键列后，则django不会再生成默认的主键列
* 属性命名限制
  * 不能是python的保留关键字
  * 由于django的查询方式，不允许使用连续的下划线

# 定义属性

* 定义属性时，需要字段类型
* 字段类型被定义在djgango.db.models.fields 目录下，为了方便使用，被导入到django.db.models中
* 使用方式
  * 导入from django.db. import models
  * 通过models.Field 创建字段类型的对象，赋值给属性
* 对于重要的数据都做逻辑删除，不做物理删除，实现方法是定义isDelete属性，类型为BooleanField，默认值为False

字段类型：

* AtuoField：一个根据实际ID自动增长的IntegerField，通常不指定

  * 如果不指定，一个主键字段将自动添加到模型中

* ​

* BooleanField：布尔字段,管理工具里会自动将其描述为checkbox

  CharField：字符串字段，单行输入，用于较短的字符串，如要保存大量文本, 使用 TextField，CharField有一个必填参数：

  > CharField.max_length：字符的最大长度，django会根据这个参数在数据库层和校验层限制该字段所允许的最大字符数。

  TextField：一个容量很大的文本字段


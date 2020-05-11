---
title: Django学习笔记
date: 2017-04-04 16:47:56
tags: [Python, Django]
category: 学习笔记
---

# Django开发



## MVC 是什么？ 

M 表示 model 主要用于对数据库层的封装

V 表示 view ，用于向用户展示结果

C 表示 controller ，是核心，用于处理请求，获取数据，返回结果。

## MVT

与 MVC 不同的是， V 就是 view 在 Django 是核心，承担了处理请求、获取数据、返回结果。

T 则是 MVC 中的 view 的替代。

> - 命令 django-admin startproject myproject 创建名为 myproject 的项目
>
> - manage.py ： 命令行工具，可以使用多种方式对 Django 项目进行交互
> - `__init__.py`: 一个空文件，它告诉python这个目录应该被看做一个 Python 包
> - settings.py: 项目的配置
> - urls.py: 项目的URL 声明
> - wsgi.py: 项目与WSGI兼容的Web服务器入口。可以在部署的时候跟 uwsgi 对接。
> - Django 自身实现了用于调试的 WSGI 服务器，但是仅仅用于调试，不要用在生产环境。

<!-- more -->

## 数据库配置

在 settings.py 文件中，通过 DATABASES 项进行数据库配置，这个是 MySQL 配置，首先使用 pip 安装 MySQL 的包，
` pip install python-MySQL `

## 创建应用

在一个项目中可以创建一个或者多个应用，每个应用进行一种业务处理
创建应用的命令：

 ` python manage.py startapp myapp `

## 定义模型类

一个模型类就对应数据库里面的一张表
在 models.py 文件中定义模型类
引入包` from django.db import models `
模型类需要继承 models.Model 类
可以重写类的，str方法，输出对象的时候，默认调用 def __str__(self)方法    

模型类竟然可以这样生成？  很神奇，它使用了 mateclass

## 生成数据表

1. 将 booktest 应用加入到 installed_apps 中

2. 模型类定义完了之后需要激活模型：编辑 settings.py 文件

```python
INSTALL_APPS = (
........,
.......,
......,
'booktest',
)
```

执行 

```python
python manager.py makemigrations 

然后执行
python manager.py migrate
```

makemigrations 和 migrate ： 一个是名词一个是动词。 就是 前者只是生成了 sql 语句，但是还没有对数据库进行操作，后者是对数据库进行 SQL 语句执行。

## 开启服务器

` python manage.py runserver ip:port `

## 后台管理操作：

- 使用django的管理：

- 创建一个管理员用户

    `python manage.py createsuperuser` 

     按照提示输入上面创建的用户名和密码，完成创建。

     进入管理站点，默认地址：http://127.0.0.1:8000/admin

     默认可以对groups、users进行管理

## 界面本地化：

编辑settings.py文件，设置编码、时区

```python
# 添加设置时区信息
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
```

## 向admin注册myapp的模型

打开myapp/admin.py文件，注册模型

```python
# 注册app
from django.contrib import admin
from models import hello
admin.site.register(hello)
```

 重新打开管理页面，可以对hello的数据进行增删改查操作，



> 如果在str方法中返回中文，会报错ascii错误	
>
> 解决：在str()方法中，将字符串末尾添加 .encode('utf-8')
> ​    

## 

## 视图：

在django中，视图对WEB请求进行回应
视图接受request对象作为第一个参数，包含了请求的信息
视图就是一个python函数，被定义在views.py中
定义完成视图后，需要配置 urlconf 即路由，否则无法处理请求



## URLconf

在Django中，定义URLconf包括正则表达式，视图两部分
Django使用正则表达式匹配请求的URL，一旦匹配成功，则调用应用的视图
在myproject/urls.py插入myapp，使主urlconf连接到myapp.urls模块

```python
url（r'^',include('booktest.urls'))
在myapp中的urls.py中添加urlconf
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^([0-9]+)/$',views,detail)
]
```



## 模板

模板是html页面，可以根据视图中船体的数据填充值
可以在和manage.py同级目录创建templates目录，然后在里面分别创建对应的app的模板目录

然后修改settings.py文件，设置TEMPLATES的DIRS值

- 在模板中访问视图传递的数据
```
  {{输出值，可以是变量，也可以是对象.属性}}
  {%执行代码段%}
  如定义一个简单的模板：

  <!DOCTYPE html>
  <html>
  <head>
      <title>首页</title>
  </head>
  <body>
  <h1>hello列表</h1>
  <ul>
  <%for hello in hellolist%>
  <li>
      <a href="{{hello.a}}">
      {{hello.b}}
      </a>
  </li>
  {%endfor%}
  </ul>
  </body>
  </html>
```

  ## 使用模板

  在views.py文件，在方法中调用模板

  ```python
  from django.http import HttpResponse
  from django.template import RequestContext,loader
  from models import hello
  
  def index(request):
      hello = Hello.objects.get(pk=id)
      template = loader.get_template('myapp/index.html')
      context = RequestContext(request,{'hello',hello})
      return HttpResponse(template.render(context))
  ```

  

  ## 去除模板的硬编码

```
  - 在index.html 模板中，超链接是硬编码的，此时请求地址为"127.0.0.1/1/"
    如果改一下url就找不到地址了，比如加一个”127.0.0.1/abc/1"
  - 问题：如果在模板中地址硬编码，将来urlconf修改后，地址将失效
  - 解决：使用命名的url设置超链接
  - 修改myproject/urls.py文件，在include中设置namespace
    url(r'admin/',include(admin.site.urls,namespace="myapp")
  - 修改myapp/urls.py文件，设置name
    url(r'^book/([0-9]+)/$,views.detail,name='detail') 
  - 修改index.html模板中的链接
     <a href="{{%url 'booktest:detail' book.id%}}>" 

```
  ## Render简写

- Django提供了函数Render（）简化视图调用模板、构造上下文

  ```python
  from django.shortcuts import render 
  from models import Hello
  
  def index(request):
      hello = Hello.objects.all()
      return render(request, 'myapp/index.html',{'hello',hello})
  ```

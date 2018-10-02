---
title: Mac上搭建基于Github博客教程
date: 2017-04-18 14:20:01
tags: [Git, Blog, Diy]
category: Mac
---

# Mac 上搭建基于Github的博客




2016年的时候，自己用阿里云买了一个服务器，和一个域名，然后利用他给的脚本，自己在阿里云linux上搭建了一个基于wordpress的博客，但是，这个阿里云学生机，每个月要签到，才有优惠价，所以，由于老是忘记，就没续费了。

2017年4月16号开始，准备写点东西，平时学习，要不然以后又忘记了。今天先记一下我用mac搭建这个博客的详细步骤。

<!-- more -->


## 前期准备

1.安装Hexo，这个就不介绍了，自己可以去官网看一看。

2.安装Node.js。一路安装即可。

3.安装GIt，xcode自带Git

## 正式开始

打开终端，执行如下命令

`$ sudo nom install -g hexo&#39;&#39;&#39;`
`$ sudo nom install -g hexo`

 

### 初始化你的博客

用终端cd到你选定放你的博客的目录，然后执行命令如下：

`$ hexo init blog`
`$ hexo init blog`

其中，blog 是你建立博客文件夹的名称，他会自动创建一个 blog的文件夹

然后 cd 到 blog文件夹下，执行:

~~~$ npm install~~~
$ npm install
~~~

执行如下命令，开启hexo服务器：

~~~ $ hexo s~~~
$ hexo s
~~~

然后，不出意外的话，你打开你的浏览器，输入网址，[http://localhost:4000](http://0.0.0.0:4000/)，就可以看到如下页面：

![](http://image.gonghonglou.com/firstblog/hexo4000.png)

好了，至此，我们本地博客已经搭好了，然后我们即将把我们的博客推送到互联网上。

## GIthub配置



在Github上 新建仓库，

名字格式为```用户名.github.io```

![](http://i1.piimg.com/567571/a38acf382c0ef74a.png)

在本地的blog文件夹中，打开_config.yml

打开后，到最后一行修改deploy：

~~~~~~
deploy:
	type: git
	repository: https://github.com/anitazhaochen/anitazhaochen.github.io.git
    branch: master

~~~~~~

repository: 在这里 ：

![](http://i2.muimg.com/567571/3e01235fadb57f2d.png)

注意：_config.yml里 配置的时候 在：后面有一个空格。



然后在blog文件夹下生成静态页面：

~~~~~~
$ hexo g
~~~~~~

如果出错，请执行这条命令

~~~~~~
$ npm install hexo-deployer-git --save   
~~~~~~

在执行 

~~~~~~
$ hexo g
~~~~~~

然后执行

~~~~~~
$ hexo d
~~~~~~

此时要注意，如果你本地没有关联你的github账号，他会让你输入账号和密码，才可以。

如果你执行此命令，你没关联过你的github账号，但是也没提示你输入，那就说明， 你的_config.yml文件配置的有问题，仔细检查，比如我喜欢自己手打，就打错了一个字符。



### 为本地配置github

这样可以免除你每次hexo d 都要输入账号和密码的问题

1.生成ssh key

把代码里的邮箱换成自己的

~~~~~~
$ ssh-keygen -t rsa -C "your_email@example.com"

~~~~~~

然后在终端 执行如下命令

~~~~~~
vim ~/.ssh/id_rsa.pub
~~~~~~

然后把里面的内容复制

进入你的网页端 github—>Settings—>SSH keys —>add SSH key :

任意取个名字，然后复制进去保存就行。



## 发布文章



终端cd 到blog文件夹下，执行命令，新建文章

~~~~~~
hexo new "name"
~~~~~~

然后他会把蚊帐的文件放在 /blog/source/_posts下，你可以用你的markdown编辑器编辑文章，然后保存



完成之后，

使用

~~~~~~
hexo g
hexo d
~~~~~~

不出错，等两分钟，你就可以输入你的网址进入你的博客了

![](http://i1.piimg.com/567571/eddd54863c6567e9.jpg)

## 你还可以去HEXO官网主题页选择你感兴趣的主题进行安装



如果觉得域名不好看，你可以去买一个域名，然后在你的主题下的source文件夹内新建一个文件叫做CNAME，里面写上你的域名

然后在hexo g  hexo d  一般会等一会，不要着急

注：参照地址[更多功能请移步](http://gonghonglou.com/2016/02/03/firstblog/) 



在写mrkdown 插入图片的时候发现了一个 好的网站，直接把图片上传上去，就可以获得网址

[markdown上传图片网站](http://jiantuku.com/#/)

记：CNAME 文件应该存放在 本主题所在的source文件夹中。

安装主题后，有两个文件，一个是 主目录的 _config.yml 一个是主题里的 /theme/主题/_config.yml   需要一些配置，才能改变主页上的某些东西。 得兼顾一下



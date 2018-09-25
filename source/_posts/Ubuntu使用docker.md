---
title: docker使用
date: 2018-03-19 12:52:14
tags: [docker]
category: Docker
---



#					Ubuntu使用docker

Docker是一个开源的应用引擎，基于Go语言并遵从Apache2.0开原协议



Docker可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的Linux机器上，也可以实现虚拟化。

容器是完全使用沙箱机制，相互之间不会有任何借口，而且容器开销极低。

<!-- more -->


docker的应用场景

 web应用的自动化打包和发布

自动化测试和持续集成、发布

在服务型环境中部署和调整数据库或者其他后台应用

从头编译或者扩展现有的openshift或者cloud foundry平台来搭建自己PaaS环境。



## Docker架构

docker使用客户端-服务器（C/S）架构模式，使用远程API来管理和创建Docker容器。

Docker容器通过Docker镜像来创建。

容器与镜像的关系类似于面向对象编程中的对象和类。





![img](http://www.runoob.com/wp-content/uploads/2016/04/576507-docker1.png)docker架构图



在ubuntu上面使用 apt即可安装，不过好像更新比较麻烦。

~~~
# sudo apt install docker.io
~~~

通过sudo service docker start 启动docker



网络问题，拉去镜像很慢，可以换源解决，可以使用网易的镜像地址：

http://hub-mirror.c.163.com

在key.json 中加一条 

{

"registry-mirrors" :  ["http://hub-mirror.c.163.com"]

}



首先，第一步， 使用 docker run  命令来在容器内运行一个已用程序。输出hello world

~~~
# docker run ubuntu:15.10 /bin/echo "Hello world"
~~~

docker : docker 的二进制执行文件

run：与前面的docker组合来运行一个容器。

ubuntu:15.10 指定要运行的镜像，Docker首先从本地主机查找镜像是否存在，如果不存在，Docker就会从镜像仓库 Docker Hub 下载公共镜像。

/bin/echo "Hello world" : 在启动的容器里执行的命令



* 运行交互式的容器

  * 通过参数 -i 和 -t ，

  * ~~~
    # docker run -i -t ubuntu:15.10 /bin/bash
    ~~~

    -t ： 在新容器内指定一个伪终端或者终端

    -i：允许对容器内的标准输入（STDIN）进行交互。

  * -d : 以进程方式运行容器，并且在后台执行

* ~~~
  # docker ps      //查看容器运行状态
  ~~~

  ~~~
  # docker logs 容器ID
  ~~~

  查看容器内的标准输出

  ~~~
  # docker stop 停止容器
  ~~~

  ~~~
  # docker pull 镜像名字   //  当拉取镜像时候，如果本地不存在，docker就会自动从docker 镜像仓库中下载，默认是从Docker Hub公共镜像源下载
  ~~~

  ~~~
  # docker port 容器ID // 查看容器的端口映射情况
  ~~~

  ~~~
  # docker logs -f 容器ID  //查看容器内部的标准输出日志信息，犹如 tail -f 一样
  ~~~

  ~~~
  # docker top 容器  //查看容器内部运行的进程
  ~~~

  ~~~
  # docker inspect 容器  // 查看docker底层信息，它会返回一个json文件记录docker容器的配置和状态信息
  ~~~

  ~~~
  # docker start|restart|stop|status
  ~~~
  ~~~
  # docker rm 容器  //删除容器时，容器必须是停止状态，否则会报错
  ~~~

* Docker镜像

  * ~~~
    # docker images //查看本机上本地的镜像
    ~~~

  * ~~~
    # docker pull REPOSITORY:TAG //如果不指定镜像的版本标签，则默认使用 ubuntu：latest镜像
    ~~~

  * ~~~
    # docker search httpd // 查找镜像
    ~~~

  * 更新镜像：

    * 首先创建一个容器，然后 对容器内的内容进行修改，完成操作之后使用exit退出容器， 然后使用 docker commit 来提交容器副本

      ~~~
      # docker commit -m=" update" -a="myself" 容器ID mysql/ubuntu:v2
      ~~~

* 构建镜像

  * 使用docker build 。

    * 创建一个 Dockerfile  文件，其中包含一组指令老告诉Docker如何构建镜像

      * 如：

      * ~~~
        runoob@runoob:~$ cat Dockerfile 
        FROM    centos:6.7
        MAINTAINER      Fisher "fisher@sudops.com"

        RUN     /bin/echo 'root:123456' |chpasswd
        RUN     useradd runoob
        RUN     /bin/echo 'runoob:123456' |chpasswd
        RUN     /bin/echo -e "LANG=\"en_US.UTF-8\"" >/etc/default/local
        EXPOSE  22
        EXPOSE  80
        CMD     /usr/sbin/sshd -D
        ~~~

        每一条指令都会在镜像上创建一个新的层，每一个指令的前缀都必须大写的。

        第一条FROM，指定使用哪个镜像源

        RUN 指令告诉docker 在镜像内执行的命令，安装了什么….

        然后，使用Dockerfile 文件，通过docker build 命令来构建一个镜像。

        ~~~
        runoob@runoob:~$ docker build -t runoob/centos:6.7 .
        Sending build context to Docker daemon 17.92 kB
        Step 1 : FROM centos:6.7
         ---&gt; d95b5ca17cc3
        Step 2 : MAINTAINER Fisher "fisher@sudops.com"
         ---&gt; Using cache
         ---&gt; 0c92299c6f03
        Step 3 : RUN /bin/echo 'root:123456' |chpasswd
         ---&gt; Using cache
         ---&gt; 0397ce2fbd0a
        Step 4 : RUN useradd runoob
        ......
        ~~~

      *  -t : 指定要创建的目标镜像名

      * . : Dockerfile 文件所在目录，或者指定绝对目录

      * ~~~
        # docker tag  容器ID  myself/ubuntu:dev //使用tag命令，为镜像添加一个新的标签
        ~~~

* Docker 容器连接

  * 网络端口映射

    * ~~~
      # docker run -d -P traning/webapp python app.py
      ~~~

    *  -P : 容器内部豆蔻随机映射到主机的高端口

    * -p : 是容器内部端口绑定到指定的主机端口

    * ~~~
      # docker run -d -p 5000:5000 training/webapp python app.py
      ~~~

  * docker 容器连接

    * 端口映射并不是唯一把docker连接到另一个容器的方法，docker有一个连接系统允许将多个容器连接在一起，共享连接信息，docker连接会创建一个父子关系，其中父容器可以看到子容器的信息

    * 创建容器的时候，docker会自动对它进行命名，可以使用 —name表示来命名容器，例如： 

      ~~~
      docker run -d -P --name myself ubuntu:15.10 
      ~~~

      ​

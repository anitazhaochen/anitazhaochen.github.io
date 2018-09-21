---
title: mysql5.7.1安装遇到的错误和解决
date: 2017-07-07 21:53:04
tags: [mysql, error, 经验]
category: 数据库
---

# Mysql 5.7.18安装遇到的问题

本机操作系统 win8.1

<!-- more -->

1.首先从官网下载压缩包

[下载地址](https://dev.mysql.com/downloads/mysql/)

本人下载 ： mysql 5.1.18 win64位

2. 解压mysql压缩包

   选择mysql数据库存储路径

   比如我直接街压在了D盘里

3. 配置环境变量

   具体方法：计算机——> 右键——>高级——>环境变量，在系统变量里找到一个名为path 的，在后面追加

   你安装的位置：比如我自己的 D:\mysql57\bin

4. 进行初始化操作，在mysql 安装的文件夹下面建立 my,ini 文件，添加如下代码：

   ```
   [mysql]
   # 设置mysql客户端默认字符集
   default-character-set=utf8 
   [mysqld]
   #允许登陆时以root空密码登陆，否则无法登陆
   skip-grant-tables
   #设置3306端口
   port = 3306 
   # 设置mysql的安装目录
   basedir=D:\mysql57
   # 设置mysql数据库的数据的存放目录
   datadir=D:\mysql57\data
   # 允许最大连接数
   max_connections=200
   # 服务端使用的字符集默认为8比特编码的latin1字符集
   character-set-server=utf8
   # 创建新表时将使用的默认存储引擎
   default-storage-engine=INNODB
   ```

   然后 进入cmd，切换到mysql下的bin目录，输入

   ```
   mysqld —initalize —user=mysql --console
   ```

   然后再输入

   ```
   mysqld --install
   ```

   如果提示 Service successfully installed 

   证明安装成功

5. 启动mysql服务

   输入

   ```
   net start mysql 
   ```

   就可以启动mysql

   我安装的时候在这里遇到过两个错误，（如果没有错误，请跳过）

   一个是 提示 mysql 无法访问 ，查了些资料，还是无法解决，就索性全部删除重装了。

   二是 先出现 mysql 服务正在启动.... 过一会又出现 mysql服务无法启动。

   第二个的解决方法是使用初始化命令解决

   mysqld —initalize —user=mysql --console

   执行完后CMD控制台上会显示一堆东西，不用管它。

   然后再次输入 net start mysql 启动服务

6. 如果实在解决不了，重装吧。

   使用 net stop mysql 停止服务

   在mysql 下的bin目录下 执行

   mysqld remove mysql 

   即可删除名为mysql 的服务

   然后自己进入注册表，查找名为mysql的值 都删除，有些删除不了的不用管它，直接下一个就行。


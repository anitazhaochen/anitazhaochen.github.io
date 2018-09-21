---
title: osx error(1045)解决方法
date: 2017-08-14 23:51:07
tags: [mysql, 环境变量]
category: Mac
---

我的mac 电脑安装完mysql后，无法正常通过 command进行连接。

显示  error(1045) access denied for user root '@ localhost

解决方法如下：

<!-- more -->

1. Open a Terminal window, and stop the mysql if it's already running. You can also check this System Preferences > MySQL > see if it is running

    ` $ sudo /usr/local/mysql/support-files/mysql.server stop`

2. Start MySQL with this command

    `$ sudo /usr/local/mysql/bin/mysqld_safe --skip-grant-tables`

3. Open a new terminal window/tab..

    `$ sudo /usr/local/mysql/bin/mysql -u root`

This should open "mysql" prompt. Execute the below command:

`mysql> UPDATE user SET Password=PASSWORD('my_password') where USER='root';`

If you see unknown "Password" field error, then run this command:

`UPDATE USER SET AUTHENTICATION_STRING=password('NewPassword') WHERE user='root'; $mysql> FLUSH PRIVILEGES; $mysql> EXIT`

4. Stop MySql server

`sudo /usr/local/mysql/support-files/mysql.server stop`

5. Restart MySQL, either through System Preferences > MySql or using a command.

6. then i meet this error

   ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.

    `mysql> SET PASSWORD = PASSWORD('your_new_password');`  

 Query OK, 0 rows affected, 1 warning (0.01 sec)

it works.






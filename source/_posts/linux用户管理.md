---
title: linux用户管理
date: 2017-11-17 14:25:31
tags: [linux, useradd, 用户组]
category: linux
---

* linux如何把普通用户添加到sudo组
    
    1. 先cd到/etc/sudoers目录下 
    2. 由于sudoers文件为只读权限，所以需要添加写入权限，chmod u+w sudoers 
    3. vim sudoers 
    4. 找到root ALL = (ALL) ALL这一行，在下一行加入username ALL = (ALL) ALL。username指代你想加入sudo组的用户名。 
    5. 把sudoers文件的权限修改回来。chmod u-w sudoers 
    6. 这样普通用户可以执行sudo命令了。
<!-- more -->

* Linux 给用户赋予自己的目录的文件创建修改权限
    
    `# chown -R test:test /home/test'

    赋予/home/test目录给test用户

    chmod 760 /home/test

    赋予test目录读写权限给test，别的用户对这个目录没有任何权限。

* 查看当前登陆的用户信息

    `# who`
    输出包括用户名、终端类型、登陆日期、以及远程主机
    `who /var/log/wtmp` 
    可以查看自从wtmp文件创       建以来的每次登陆情况
    `who -b`
    查看系统最近一次启动时间
    `who -H` 
    打印每列的标题 
    
* 查看命令历史
    每个用户都有一份命令历史记录 

    查看$HOME/.bash_history 

    或者在终端输入： history
    
* last命令
    查看用户登录历史 

    此命令会读取 /var/log/wtmp文件；/var/log/btmp可以显示远程登陆信息。 

    last默认打印所有用户的登陆信息。 

    如果想打印某个用户的登陆信息，可以使用 

    last 用户名
 选项： 

    （1）-x：显示系统开关机以及执行等级信息 

    （2）-a：将登陆ip显示在最后一行 

    （3）-f ：读取特定文件，可以选择 -f /var/log/btmp文件 

    （4）-d：将IP地址转换为主机名 

    （5）-n：设置列出名单的显示列数 

    （6）-t：查看指定时间的用户登录历史 

    例如： 

    last -t 20150226160404 

    显示这个时间戳之前的登陆历史
 



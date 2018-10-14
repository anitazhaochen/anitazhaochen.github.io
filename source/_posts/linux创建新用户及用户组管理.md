---
title: linux创建新用户及用户组管理
date: 2017-11-15 22:13:40
tags: [linux, 用户, 用户组]
category: linux
---


# linux创建新用户及用户组管理


* 用户管理


useradd  命令创建用户
adduser  也可以创建用户

<!-- more -->

`# useradd -m test~`
创建用户名为test的用户，并且为他创建家目录/home/test

-d 命令是指定用户的家目录
`# useradd -d /test -m test  `
创建test用户，并且指定test的家目录是 /test,若/test目录不存在，则创建

useradd -g 指定用户所属的用户组
useradd -G  指定用户所属的附加组
useradd -s  指定用户的登陆shell
`# useradd -s /bin/sh test`
创建用户test，指定他登陆的shell为sh
等等

passwd  命令为用户设置密码
`passwd test`
为用户test设置密码
passwd -l  锁定口令，禁用账号
passwd -u  口令解锁
passwd -d 是账号无口令
passwd -f 强迫用户下次登陆时修改口令
passwd   如果没有参数，默认修改当前用户的口令
passwd 参数 用户名  来修改用户的密码


userdel  删除用户
`# userdel -r test  `
基本删除用户test的家目录，等等一些文件

usermod 命令改变用户所属组
`# usermod -g groupA user `
不要直接用，这样做会使user离开其他组，仅仅成为了groupA组的成员。
如果需要为user添加groupA组，需要使用
`# usermod -a -G groupA user`
只使用-G参数时候，组与组之间可以用’，’分割
如： -G, --groups GROUPS           
新的附加组列表 GROUPS
这个命令还可以修改用户名，用户家目录，用户登陆名称等等


查看用户所属的组使用命令：
`# groups user `
或者直接查看文件
`  # cat /etc/group`
finger user 
查看user的用户信息

id user 
查看用户UID、GID及所归属的用户组

普通用户sudo命令，像root用户一样执行操作。执行su 需要知道root密码，这样就很不安全
sudo被称为受限的su。
可以设置一个工作组，让特别的用户称为工作组成员，设置组  sudo 可以执行的命令，root用户通过修改文件 /etc/sudoers 来进行授权
例如：
要 test1 这位用户负责管理网站数据，一般Apache Web Server的进程httpd的所有者是www，你能设置用户 test1 和www为同一工作组，并设置Apache默认存放网页目录 /usr/local/httpd/htdocs的工作组权限为可读、可写、可执行，这样属于此工作组的每位用户就能进行网页的管理了。

sudo的公式：
授权用户 主机=[(转换到哪些用户或用户组)] [是否需要密码验证] 命令1,[(转换到哪些用户或用户组)] [是否需要密码验证] [命令2],[(转换到哪些用户或用户组)] [是否需要密码验证] [命令3]......
例如：
test ALL=(ALL) ALL
这个条目是的用户test可以sudo执行所有命令
如果遇到普通用户拥有了执行所有sudo命令的权限，但是执行的时候却还是说命令不存在，那么肯定是此用户的环境变量是不包含系统命令所在的路径，这个时候，最后写绝对路径
如：
sudo /usr/sbin/ifconfig
也可以把 /usr/sbin 添加到用户环境变量里，然后在执行
sudo ifconfig

可以通过whereis ifconfig 来查看命令的二进制文件的路径，
这个时候不能使用which ifconfig 来查看，因为which 找不到这个命令。
例：
test2  ALL=/usr/sbin/reboot, /usr/sbin/shutdown
写命令最好都写绝对路径，避免造成安全隐患。


例：
=前面的ALL是主机，一般我们就写ALL
其中主机，指的是服务器的主机名，并不是客户机的用户名。
例：
test3 ALL=(root) /bin/chown, /bin/chmod
表示test3 用户可以出现在所有主机名中以root用户的方式对所有文件进行chown操作，能转换到所有用户执行chmod命令

test4 ALL=(root) NOPASSWD  
test4可以以root身份执行命令，并且不用输入自己的密码
sudo -l  可以显示用户哪些命令不能执行
sudo命令匹配支持 ’*’ 号 ， ‘!’ 是不能执行的意思，加在路径开头
还可以设置别名等等 


如果你想对一组用户进行定义，能在组名前加上%，对其进行设置，如：
%cuug ALL=(ALL) ALL


凡是[ ]中的内容，是能省略；命令和命令之间用,号分隔；通过本文的例子，能对照着看哪些是省略了，哪些地方需要有空格；在[(转换到哪些用户或用户组)] ，如果省略，则默认为root用户；如果是ALL ，则代表能转换到所有用户；注意要转换到的目的用户必须用()号括起来，比如(ALL)、(test)




* 管理用户组

我们为了让一些用户有权限查看某一文件，比如是个时间表，而编写时间表的人要具有读写执行的权限，我们想让一些用户知道这个时间表的内容，而不让他们修 改，所以我们能把这些用户都划到一个组（用chgrp命令），然后来修改这个文件（用chmod命令）的权限，让用户组可读（用chgrp命令将此文件归 属于这个组），这样用户组下面的每个用户都是可读的，其他用户是无法访问的。
这些事面向文件
chgrp  是用来修改用户所属的组
chomd 是用来修改文件的权限


groupadd  添加用户组
groupdel  删除用户组
groupmod  修改用户组信息
groups   显示用户所属组

如果一个用户同时属于多个用户组，那么用户能在用户组之间转换，以便具有其他用户组的权限。用户能在登录后，使用命令newgrp转换到其他用户组，这个命令的参数就是目的用户组。
例如：
newgrp root
这条命令将当前用户转换到root用户组，前提条件是root用户组确实是该用户的主组或附加组。类似于用户账号的管理，用户组的管理也能通过集成的系统管理工具来完成。









---
title: linux系统及进程管理
date: 2018-03-04 16:38:12
tags: [linux, 进程]
category: linux
---

# Systemd：

POST --> Boot Sequence --> Bootloader --> kernel + initramfs(initrd) --> rootfs --> /sbin/init
    init:
        CentOS 5 : SysV init
        CentOS 6: Upstart
        CentOS 7: Systemd
        
    Systemd新特性：
        系统引导时实现服务并行启动：
        按需激活进程：
        系统状态快照：
        基于依赖关系定义服务控制逻辑：

<!-- more -->
        
    核心概念： unit
        配置文件进行表示和配置： 文件中主要包含了系统服务、监听socket、保存的系统快照以及其他与init相关的信息：
        保存至：
        /usr/lib/systemd/system
        /run/systemd/system
        /etc/systemd/system
    Unit 的类型：
        Service unit： 文件扩展名为.service ，用于定义系统服务
        Target unit：文件扩展名为.target,用于模拟实现“运行级别”：
        Device unit： .mount，定义文件系统挂载点：
        Socket unit： .socket,用于标识进程间通信用的socket文件：
        Snapshot unit： .snapshot，管理系统快照
        Swap unit： .swap,用于标识swap设备
        Automount： .automount,文件系统的自动挂载点：
        Path unit： .path，用于定义文件系统中的一个文件或目录

关键特性：
    基于socket的激活机制：socket与服务程序分离：
    基于bus的激活机制
    基于device的激活机制
    基于path的激活机制：
    系统快照：保存各unit的当前状态信息于持久化存储设备中
    向后兼容sysv init脚本

不兼容：
    systemctl命令固定不变
    非由systemd启动的服务，systemctl无法与之通信

管理系统服务：
    CentOS 7： service unit
        注意：能兼容早起的服务脚本
        
        命令：systemctl COMMAND name.service 
        
    启动： service name start ==> systemctl start name.service
    停止： service name stop ==> systemctl stop name.service
    重启： service name restart ==> systemctl restart name.service
    状态： service name status ==> systemctl status name.service
    条件式重启： service name condrestart ==> systemctl try-restart name.service 服务启动了，就重启，服务没启动就不启动
    重载或重启服务： systemctl reload-or-restart name.service
    重载或条件式重启服务： systemctl reload-or-try-restart name.service    
    禁止设定为开机自启：systemctl mask name.service
    取消禁止设定为开机自启：systemctl unmask name.service
    
    查看某服务当前激活与否的状态： systemctl is-active name.service
    查看所有已激活的服务：
        systemctl list-units --type service 
    查看所有服务
        systemctl list-units --type service --all
        
    chkconfig 命令的对应关系：
        设定某服务开机自启： chkconfig name on ==> systemctl enable name.service
    查看服务是否开机自启：
        systemctl is-active name
    
    其他命令：
        查看服务的依赖关系：systemctl list-dependencies name

target units:
    unit 配置文件： .target 

    运行级别：
        0 ==> runlevel0.target,poweroff.target 设定为关机
        1 ==> runlevel1.target, rescue.target 单用户模式
        2 ==> runlevel2.target , multi-user.target 
        3 ==> runlevel3.target , multi-user.target 
        4 ==> runlevel4.target , multi-user.target
        5 ==> runlevel5.target , graphical.target
        6 ==> runlevel6.target , reboot.target
        
    级别切换：
        init N ==> systemctl isolate name.target
        systemctl isolate graphical.target
    查看级别：
        runlevel ==> systemctl list-units --type target
        
    默认运行级别：
        /etc/inittab ==> systemctl get-default
        
    修改默认级别：
        /etc/inittab ==> systemctl set-default multi-user.target
        
    切换至紧急救援模式：
        systemctl rescue
    
    切换至emergency模式：
        systemctl emergency  比rescue更彻底，如连驱动都不加载

其他常用命令：
    关机：systemctl halt 
    重启：systemctl reboot
    挂起：systemctl suspend
    快照：systemctl hibernate 
    快照并挂起：systemctl hybrid-sleep

函数： 模块化编程

    function f_name {
        ...函数体...
    }
    
    f_name() {
        ...函数体...
    }
    
    return 命令：
    参数：
        函数体中调用参数：$1,$2,...
        $*,$@,$#
        向函数传递参数：
            函数名 参数列表

systemd:系统及服务
    unit：
        类型：service,target
        .service,.target
    systemctl

bash脚本编程：

    变量：存储单个元素的内存空间：
    数组：存储多个元素的连续的内存空间：
        数组名
        索引：编号从0开始，属于数值索引
            注意：索引页支持使用自定义的格式，而不仅仅是数值格式：
        
        引用数组中的元素： ${ARRAY_NAME[INDEX]}
        
    声明数组：
        declare -a ARRAY_NAME
        declare -A ARRAY_NAME: 关联数组：kv 键值列表
        
    数组元素的赋值：
        （1）一次只赋值一个元素：
            ARRAY_NAME[INDEX]=VALUE
         (2)一次赋值全部元素：
            ARRAY_NAME=("VAL1" VAL2"...)
         (3)只赋值特定元素：
            ARRAY_NAME=([0]="VAL1" [3]="VAL2")
            
    引用数组元素： ${ARRAY_NAME[INDEX]}
        注意： 省略[INDEX]表示引用下标为0的元素：
        
    数组的长度： ${#ARRAY_NAME[*]}, ${#ARRAY_NAME[@]}
    
    引用数组中的元素：
        所有元素： ${ARRAY[@]} , ${ARRAY[*]}
        
        数组切片： ${ARRAY[@]:offset:number}
            offset:要跳过的元素个数
            number：要取出的元素个数
            
        ${ARRAY[@]:offset}： 取偏移量之后的所有元素
    
    想数组中追加元素：
        ARRAY[${#ARRAY[*]}]
        
    删除数组中的某元素：
        unset ARRAY[INDEX]
    关联数组：
        declare -A ARRAY_NAME
        ARRAY_NAME=([index_name1]="VAL1" [index_name2]="VAL2" ...)
        
    bash字符串处理工具：
        字符串切片：
            ${var:offset:number}
            取字符串的最右侧几个字符：${var: -lengh}
                注意：冒号后必须有一个空字符：
                
    基于模式取子串：
        ${var#*word} ：其中word可以是指定的任意字符：功能：自左而右查找var变量所存储的字符串中，第一次出现的word，删除字符串开头至第一次出现word字符之间的所有字符：
        ${var##*word} 同上，不过，删除的是字符串开头至最后一次由word指定的字符之间的所有内容：
        ${var%word*}: 同上相反，自右向左
        
    查找替换：
        ${var/pattern/substi}:查找var所表示的字符串中，第一次被pattern所匹配到的的字符串，以substi替换之;
        ${var//pattern/substi}:查找var所表示的字符中，所有能被pattern所匹配到的字符，以substi替换之。
        ${var/#pattern/substi}:查找var所表示的字符中，行首被pattern所匹配到的字符串，以substi替换
        ${var/%pattern/substi}:查找var锁表是的字符中，行尾被pattern所匹配到的字符串，以substi替换
        
    查找并删除：
        ${var/pattern}:查找var字符中，第一次匹配到的pattern，然后删除
        ${var//pattern}:查找var字符中，所有匹配到pattern，删除所有
        ${var/#pattern}：同上行首        
        ${var/%pattern}：同上行尾
        
    字符大小写转换：
        ${var^^}:把var所有字符转换为大写
        ${var,,}:把var所有字符转换为小写
        
    变量赋值：
        ${var:-value}:如果var为空或未设置，那么返回value，否则，返回var的值
        ${var:=value}:如果var为空或者未设置，那么返回value，并且把var设置为value
        ${var:+value}:如果var不空，则返回value
        ${var:?error_info}:如果var为空或者未设置，返回error_info到错误信息流中,否则返回val自身的值
        
    命令：
        mktemp命令：
            mktemp [OPTION] ... [TEMPLATE]
                TEMPLATE: filename.XXX
                    XXX至少出现三个
                OPTION:
                    -d:创建临时目录：
                    --tmpdor :指明临时文件目录位置
                    
        install命令: 文件复制命令
            install [OPTION]... [-T] SOURCE DEST
            install [OPTION]... SOURCE... DIRECTORY
            install [OPTION]... -t DIRECTORY source...
            install [OPTION]... -d DIRECTORY...
                选项：
                    -m MODE
                    -o OWNER
                    -g GROUP


​    
​    

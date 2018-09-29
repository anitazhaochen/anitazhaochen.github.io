---
title: iptables
date: 2018-02-04 22:10:52
tags: [linux, iptables, 防火墙]
category: linux
---

# iptable

iptables：
    Firewall：防火墙，隔离工具：工作于主机或网络的边缘，对于进出本主机或网络的报文根据事先定义好的检查规则作匹配检测，对于能够被规则匹配到的报文做出相应的处理的组件
        主机防火墙
        网络防火墙

iptables/netfilter
    framwork: netfilter
<!-- more -->
        hook function
    rule utils: iptables

功能：
    filter：过滤，防火墙
    nat：network address translation，网络地址转换
    mangle：拆解报文，做出修改，封装报文
    raw：关闭nat表上启用的连接追踪机制

链（内置）：
    PREROUTING
    INPUT
    FORWARD
    OUTPUT
    POSTROUTING

流入：PREROUTING --> INPUT
流出：OUTPUT --> POSTROUTING
转发：PREROUTING --> FORWARD --> POSTROUTING

各功能的分别实现：
    filter：INPUT，FORWARd，OUTPUT
    nat：PREROUTING（DNAT），OUTPUT，POSTROUTING（SNAT）
    mangle：PREROUTING，INPUT，FORWARD，OUTPUT，POSTROUTING
    raw：PREROUTING，OUTPUT

路由发生的时刻：
    报文进入本机后：
        判断目标主机
    报文发出之前：
        判断经由哪个接口送往下一跳


iptables：四表五链
    添加规则时的考量点：
        （1）要实现哪种功能：判断添加在那张表上
        （2）报文流经的路径：判断添加在哪个链上
        
    链：链上的规则的次序，即为检查的次序，因此隐含一定的法则
        （1）同类规则（访问同一应用），匹配范围小的放上面：
        （2）不同类规则（访问不同应用），匹配到报文频率较大的放上面
        （3）合并可以由一条规则描述的多个规则合并为一个
        （4）设置默认策略
    功能优先级次序：raw--> mangle --> nat --> filter

规则：
    组成部分：报文的匹配条件，配到到之后的处理动作
        匹配条件：根据协议报文特征指定匹配条件
            基本匹配条件
            扩展匹配条件
        处理动作：
            內建处理机制
            自定义处理机制
        
        注意：报文不会经过自定义链，只能在内置链上通过规则引用后生效

iptables：规则管理工具
    添加、修改、删除、显示等

    规则和链有计数器：
        pkts：有规则或链所匹配到的报文的个数
        bytes：由规则或链匹配到的所有报文大小之和

iptables命令：
       iptables [-t table] {-A|-C|-D} chain rule-specification

       ip6tables [-t table] {-A|-C|-D} chain rule-specification

       iptables [-t table] -I chain [rulenum] rule-specification

       iptables [-t table] -R chain rulenum rule-specification

       iptables [-t table] -D chain rulenum

       iptables [-t table] -S [chain [rulenum]]

       iptables [-t table] {-F|-L|-Z} [chain [rulenum]] [options...]

       iptables [-t table] -N chain
       iptables [-t table] -X [chain]
    
       iptables [-t table] -P chain target
    
       iptables [-t table] -E old-chain-name new-chain-name
    
       rule-specification = [matches...] [target]
    
       match = -m matchname [per-match-options]
    
       target = -j targetname [per-target-options]


​       
       -t table:
            filter,nat,mangle,raw
       链管理：
            -F: flush，清空规则链，省略链表示清空所有表上的所有链
            -N: new，创建新的自定义规则链
            -X: delete 删除用户自定以的规则连（空链才行，先使用-F清空规则）
            -Z: zero，清零，置零规则计数器
            -P: Policy，为指定链设置默认策略，对filter表中的链而言，默认策略通常有ACCEPT，DROP，REJECT
            -E: rEname，重命名自定义链，引用计数不为0的自定义链，无法改名，也无法删除
       
       规则管理：
            -A: append, 将新规则追加于指定链尾部
            -I: insert，将规则插入到指定链的指定位置
            -D: delete，删除指定链上的指定规则
                有两种指定方式：
                    （1）指定匹配条件
                    （2）指定规则编号
            -R：replace，替换指定链上的指定规则
        查看：
            -L：list，列出指定链上的所有规则
                -n：number，以数字格式显示地址和端口号
                -v：verbose，显示详细信息
                        -vv，-vvv （v越多显示结果更详细）
                --line-numbers:显示规则编号
                -x：exactly，显示计数器计数结果的精确值
                
        匹配条件：
            基本匹配：
                [!] -s, --src, --source IP|Netaddr：检查报文中源IP地址是否符合此处指定的地址范围
                [!] -d, --dst, --destination IP|Netaddr: 检查报文中目标IP地址是否符合此处指定的地址范围
                -p， --protocol {tcp|udp|icmp}:检查报文中的协议，即ip首部中的protocols所标识的协议
                -i, --in-interface IFACE: 数据报文的流入接口，仅能用于PREROUTING，INPUT及FORWARD链上
                -o，--output-interface IFACE：数据报文的流出接口：仅能用于FORWARD，OUTPUT及POSTROUTING链上
                
            扩展匹配：-m match_name --spec_options
                    例如：-m tcp --dport 22
                隐式扩展：对-p protocol指明的协议进行扩展，可省略-m选项
                    -p tcp
                        --dport PORT [-PORT]:目标端口，可以是单个端口或者多个端口
                        --sport PORT [-PORT]
                        --tcp-flags LIST1 LIST2: 检查LIST1所指明的所有标志位，且这其中，LIST2所表示出的标志位必须为1，而余下的必须为0：没有LIST1中指明的，不做检查
                        SYN，ACK，FIN，RST，PSH，URG
                        
                        --tcp-flags SYN，ACK，FIN，RST，SYN  检查是否为新建tcp连接的第一次连接
                        --syn
                    -p udp
                        --dport
                    -p icmp
                        --icmp-type
                            可用数字表示其类型：
                                0：echo-reply
                                8：echo-request
            
        目标：
            -j TARGET： jump至指定的TARGET
                ACCEPT：接受
                DROP：丢弃
                REJECT：拒绝
                RETURN：返回调用链
                REDIRECT：端口重定向
                LOG：记录日志
                MARK：做防火墙标记
                DNAT：目标地址转换
                SNAT：源地址转换
                MASQUERADE: 地址伪装
                ...
                自定义链：由自定义链上的规则进行匹配检查


复习：
    iptables/netfilter
        netfilter: kernel framwork
        iptables
        
        四表：filter，nat，mangle，raw
        五链：PREROUTING，INPUT，FORWARD，OUTPUT，POSTROUTING
    
    iptables：
        子命令：
            链： -F -X -N -E -Z -P -L
            规则： -A -I -D -R
            
            -j TARGET:
                ACCEPT,DROP,REJECT,RETURN,LOG,MARK,DNAT,SNAT,MASQEARDE,...
                
            匹配标准：
                通用匹配： -s，-d，-p，-i，-o
                    扩展匹配：
                        隐含扩展：
                            -p tcp --dport, --sport, --tcp-flag, --syn (--tcp-flags SYN,ACK,FIN,RST SYN)
                            -p icmp --icmp-type
                    显式扩展： -m
                    
    iptables：
        
            显式扩展：必须显式指明使用的扩展模块（rpm -ql iptables | grep "\.so")
            
                CentOS 6: man iptables
                CentOS 7: man iptables-extensions
                
        1.multiport扩展
            以离散方式定义多端口匹配：最多定义15个端口
            
            [!] --source-ports,--sports port[,port|,port:port]...
            [!] --destination-ports,--dports port[,port|,port:port]...
            [!] --ports port[,port|,port:port]...
                
        2.iprange扩展
            指明连续的（但一般是不能扩展为真个网络）ip地址范围时使用
            [!] --src-range from[-to]
            [!] --dst-range from[-to]


​    
​    
​        
​        

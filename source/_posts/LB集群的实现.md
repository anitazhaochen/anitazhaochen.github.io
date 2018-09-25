---
title: LB集群的学习笔记
date: 2018-03-08 22:12:25
tags: [linux, 运维, LB, 集群, 笔记]
category: linux
---

# LB集群的实现
硬件：
    F5 BIG-IP
    Citrix NetScaler
    A10 A10
    Array
    Redware

<!-- more -->
软件：
    lvs
    haproxy
    nginx
    httpd
    varnish
    ats(apache traffic server)
    perlbal
    
    基于工作的协议层次划分：
        传输层：
            lvs，haproxy（mode tcp）
        应用层：
            haproxy，nginx，ats，perlbal

lvs：
    章文嵩：正明：
    lvs：Linux Virtual Server
    
    l4：四层交换，四层路由
        根据请求报文的目标IP和PORT将其转发至后端主机集群中的某一台主机（根据挑选算法）
        
        netfilter:
            PREROUTING --> INPUT
            PREROUTING --> FoRWARD --> POSTROUTING
            OUTPUT --> POSTROUTING
            
    lvs
        ipvsadm/ipvs
        
        ipvsadm: 用户控件的命令行工具，用于管理集群服务
        ipvs：工作内核中的netfilter INPUT钩子上
        
        支持TCP， UDP， AH， EST ， AH_EST ， SCTP等诸多协议
        
    lvs arch：
        调用度器：director , dispatcher, balancer
        RS：Real Server
        
        Client IP：CIP
        Director Virtual IP ：VIP
        Director IP：DIP
        Real Server IP： RIP
        
    lvs type：
        lvs-nat
        lvs-dr（direct routing）
        lvs-tun（ip tunneling）
        lvs-fullnat
        
        lvs-nat：
            多目标的DNAT（iptables）：它通过修改请求报文的目标IP地址（同时可能会修改目标端口）至挑选出某RS的RIP地址实现转发
            
            （1）RS应该和DIP使用私有网址，且RS的网关要指向DIP
            （2）请求和响应报文都要经由director转发，极高负载场景中，director可能成为系统瓶颈
            （3）支持端口映射
            （4）RS可以使用任意OS
            （5）RS的RIP和Director的DIP必须在同一IP网络
            
        lvs-dir：direct routing
            它通过修改请求报文的目标mac地址进行转发
                Director：VIP，DIP
                RSs： RIP，VIP
            （1）保证前端路由将目标IP为VIP的请求报文发送给director
                解决方案：
                    静态绑定
                    arptables
                    修改RS主机内核的参数
            （2）RS的RIP可以使用私有地址，但也可以使用公网地址
            （3）RS跟Director必须在同一物理网络中
            （4）请求报文经由Director调度，但响应报文不一定经由Director
            （5）不支持端口映射
            （6）RS可以大多数OS
            （7）RS的网关不能指向DIP
            
    LVS-TYPE：
        lvs-nat : MASQUERADE
        lvs-dr: GATEWAY
        lvs-tun: IPIP
        lvs-fullnat
        
    lvs-nat: 请求和响应报文都经由director
    lvs-dr： 仅请求报文经由director，响应报文是由RS直接响应给Client


ipvs（2）
    lvs-type:
        lvs-nat: RIP与DIP必须在同一网段
        lvs-dr： Director与RS必须在同一物理网络
        lvs-tun：
            不修改请求报文的ip首部，而是通过在原有的ip首部（cip <--> vip）之外，再封装一个ip首部（dip<-->rip）：
            （1）RIP,DIP,VIP 全得是公网地址
            （2）RS的网关不能指向DIP
            （3）请求报文必须经由director调度，但响应报文必须不能经由director
            （4)不支持端口映射
            （5）RS的OS必须支持隧道功能
            
        lvs-fullnat：
            director通过同时修改请求报文的目标地址和源地址进行转发：
                （1）VIP是公网地址，RIP和DIP是私网地址，二者无需在同一网络中
                （2）RS接收到的请求报文的源地址为DIP，因此要响应给DIP
                （3）请求报文和响应报文都必须经由Director
                （4）支持端口映射机制
                （5）RS可以使用任意OS

http: stateless
    session保持：
        session绑定：
            source ip hash
            cookie
        session集群：
            
        session服务器：

lvs scheduler：
    静态方法：仅根据算法本身进行调度：
        RR: round robin, 论调
        WRR：weighted rr
        SH：source hash 实现session保持的机制，将来自同一个ip的请求始终调度到同一RS
        DH：destination hash，将对同一个目标的请求始终发往同一个RS
    动态方法：根据算法及各RS的当前负载状态进行调度：
            Overhead=
        LC：Least Connection 
            Overhead= Active*256+Inactive
        WLC： weight LC
            Overhead=（Active*256+Inactive）/weight
        SED：Shortest Expection Delny
            Overhead=（Active+1）*256/weigth
        NQ： Never Quenu
            SED算法的改进
        LBLC：Locality-Based LC，即为动态的DH算法
            正向代理情形下的cache server调度
        
        LBLCR：Locality-Based Least-Connection with Replication，带复制功能的LBLC算法

ipvs的集群服务：
    tcp，udp，ah，esp，ah_esp，sctp
    （1）一个ipvs主机可以同时定义多个cluster service
            tcp， udp
    （2）一个cluster service上至少应该一个real server
        定义时：指明lvs-type，以及lvs scheduler

ipvsadm的用法：
    管理集群服务
        ipvsadm -A|E -t|u|f service-address [-s scheduler]
        ipvsadm -D -t|u|f service-address
        ipvsadm -C
        ipvsadm -L|l [options]             
        
        service-address:
            tcp: -t ip:port
            udp: -u ip:port
            fwm: -f mark  
        
        -s scheduler:
            默认为wlc 
    
    管理集群服务中的RS
        ipvsadm -a|e -t|u|f service-address -r server-address
        ipvsadm -d -t|u|f service-address -r server-address
    
        server-address:
            ip[:port]
            
        lvs-type :
            -g: gateway, dr
            -i: ipip, tun
            -m: masquerade, nat


    清空和查看：
        ipvsadm -C
        ipvsadm -L|l [options]
        
    保存和重载：
        ipvsadm -R
        ipvsadm -S [-n]
        
    置零计数器：
        ipvsadm -Z [-t|u|f service-address]


lvs-nat：

    nat模型实现http和https两种负载均衡集群：
        ssl：
            RS：都要提供同一个私钥和同一个证书
            
    lvs-dr:
        两个

---
title: 蜜罐透明代理研究
date: 2018-08-10 11:55:03
tags: [honeypot, haproxy, tproxy]
category: 网络安全
---

# 蜜罐做透明代理



## 透明代理是什么

- 透明代理（简单代理）：透明代理的意思是客户端根本不需要知道有代理服务器的存在，它改编你的request fields（报文），并会传送真实IP。通俗来说就是，如果我们的网络是内网，访问网站，网站服务器看到的ip是我们内网的出口ip，而不是内网的ip，而使用透明代理，则可以实现向我们访问的服务器传达真实的内网ip。

- 研究目的：已有项目因在同一台机器上面部署一个docker容器管理平台Rancher， 并且需要获取源连接主机的源IP，所以需要部署HAProxy做透明代理，一般而言，HAProxy稳定的运行需要尽可能少的启用其他无关进程。
- HAProxy用到了一些iptables做转发，并且rancher也用到了一些，就难免不冲突，导致了问题，在不增加机器的前提上，做了此调研，能否有所改进。

<!-- more -->
## LVS

- LVS-NAT 原理： 通过修改源目的IP实现，进入时DNAT，出去时SNAT
- LVS-FullNAT： NAT加强版，通过修改源目的IP实现，进入时DNAT+SNAT，出去时SNAT+DNAT
- 原理对比
- NAT包修改： 在入包时，进行目的地址转换，出包时进行源地址转换，为了让出去的数据包经过LVS，需要添加策略路由。
- FullNAT实现原理：在入包时修改目的地址，同时把源地址改为内网地址，这样包就可以完全无限制的在整个内外路由，出包时修改源地址为vip地址，目的地址为真实的ClientIP地址，从而实现回包到目的地。
- 优缺点对比
  - LVS-NAT： 
  - 优点：
    - rs可以在整个内网中，没有vlan的限制
    - 支持端口映射
  - 缺点：
    - rs的网关必须是lvs机器，如果不是，则需要配置静态路由
  - LVS-FullNAT
    - 优点：
      - 数据包可以在整个内外中任意路由
      - 交换机和路由器无需任何特殊配置
    - 缺点：
      - windows无法获取client ip
- FULLNAT实现功能如下：
  - 数据包从外部进来的时候，目标ip更换为realserver ip， 源ip更换为lvs local ip
  - 数据包发送出去的时候，目标ip更换为client ip，源ip更换为vip（lvs自己的ip）
- 总结： 因为 FULLNAT 既更改了源IP 和目的IP ，所以realserver 可以和 lvs机器不在同一个内网，而NAT只修改了DNAT，和SNAT ，所以realserver和 lvs机器 需要在同一内网。



## TProxy

- tproxy 是iptables的一种附加控件，在一个控件中同时实现了多种透明代理功能。在mangle表的PREROUTING链中使用，不修改数据包包头，直接把数据传递给一个本地socket（即不对数据包进行任何nat操作）。在tproxy工作过程中，首先，tproxy向netfilter注册一个target，该target能够在不对数据包修改的情况下，将数据包代理到本地套接字上，他的关键点在于通过获得数据包的目的端口和目的地址，再通过nf_proxy_get_sock_v4函数，获得监听套接字，最后把skb->sock = sk。
- 流程：
  - 运用ip数据包过滤器（规则）将去往外部网络的ip会话报文重定向到本地进程（由本地诸如haproxy这样的相关进程再处理）
  - 尽可能地让一个进程去监听联系着外部IP地址的连接。
  - 尽量让一个进程去发起如同拥有一个类似客户端外部原IP地址的关联（就是实现IP欺骗，使用代理过程对两次数据包的传输过程，如同没有代理环节的存在。数据包出入对比）
- 总结：tproxy 为基础组件，可以作为haproxy的基础。





## 常见的负载均衡

- 四层负载均衡和七层负载均衡

  - 在七层（应用层）负载均衡的模式下，负载均衡器与客户端及后端的服务器会分别建立一次TCP连接，而在四层（传输层）负载均衡模式下，仅建立一次TCP连接。由此可知，七层负载均衡对负载均衡设备的要求更高，而七层负载均衡的处理能力也必然低于四层模式的负载均衡。[详情](https://www.cnblogs.com/skyflask/p/6970151.html)

- LVS 和HAProxy的异同

  - 两者都是软件层面的负载均衡技术，HAProxy是基于四层和七层，可提供TCP和HTTP应用等的负载均衡
  - LVS是基于四层，linux操作系统实现的一种负载均衡，因其工作在第四层，所以状态监测单一，而HAProxy在状态监测方面功能强大，可支持端口、URL、脚本等多种状态检测方式。
  - HAProxy功能强大，但是整体处理性能低于第四层模式的LVS负载均衡，而LVS拥有接近硬件设备的网络吞吐量和连接负载能力

  

## HAProxy

- 在tproxy的基础上，与 HAProxy 结合实现透明代理

- 参考 [haproxy原理与部署](http://blog.51cto.com/yjy724/1840795)

- 其他:如[内网穿透工具frp](https://github.com/fatedier/frp)

  
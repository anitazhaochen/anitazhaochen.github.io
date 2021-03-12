---
title: LVS负载均衡模型及实际应用
tags: [负载均衡, Linux, 架构, 透明代理]
category: LVS
date: 2018-11-26
---

## 前言

通过树莓派做流量转发至后端服务器，通过 ip_forward 来进行流量转发，可以转发到不同网段。

![image-20181127113006330](/images/image-20181127113006330-3289406.png)

可以在网络的前端防止嗅探器，实质是一个流量转发的工具。

然后在同一个网段，将树莓派做成一个类似路由器的东西，但是不是路由器，开启 IP 转发，将所有包转发至后端的一台 Docker 集群。

但是这样的话， client 的 ip 就会丢失，我们并无法确定是谁访问了嗅探器。

在后端服务器上面拿到的 IP 只是嗅探器的 IP。

使用 LVS 的 DNat 就可以解决问题。

> [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server) 是直接工作在内核的负载均衡器，调度能力很强。

## lVS 的调度方法

### 静态方法：仅根据算法本身进行调度

* Round Robin（轮询）

* Weighted Round Robin（加权轮询）
* Source Hash（源地址哈希）： 实现 session 保持的机制，将来自同一个 IP 的请求始终调度至同一个服务器。
* Destination Hash（目标地址哈希）

`源地址哈希` 反向代理时为缓存做负载均衡。针对客户端经常访问的资源做缓存

`目标地址哈希`正向代理的时候对缓存做负载均衡，针对服务端经常被访问到的资源做缓存

动态方法（考虑是否是持久连接）： lc，wlc，，sed，nq，lblc，lblcr

​	overhead：active connections，inactive connections

* Least Connection（最少连接数）

  Overhead = Active * 256 + Inactive

* Weighted LC （加权轮询）

  Overhead = （Active * 256+Inactive）/ weight

* Shortest Expection Delay（最短期望延迟）

  Overhead = （Active+1）*256/weight

* Never Queue

​	`最短期望延迟` 算法的改进（第一轮各分一个，然后根据 `最短期望延迟` 算法继续）

* LBLC： Locality-Based LC，即为动态的 `目标地址哈希` 算法

​	实现正向代理情形下的 cache server 调度

* LBLCR：Locality-Based Least-Connection with Replication，带复制的 LBLC 算法。



## LVS 模式

* 一类是请求报文和响应报文都经由 Director 进行调度，在极高的负载场景中，Director 可能会成为性能瓶颈。
* 另一类是请求报文经由 Director ，响应报文一定不经由 Director，曾经有人做过测试，LVS 的并发可以达到百万级，HAproxy 是远达不到这个量级的。 

### LVS-Nat 模型

多目标的 DNAT（iptables）：它通过修改请求报文的目标 IP 地址（同时可能会修改目标端口）

`Web服务器`应该和 `调度器` 使用私网地址，且 `Web服务器` 的网关要指向 `调度器 `

`请求报文`和`响应报文`都要经由 `LVS` 转发：极高负载的场景中， `LVS` 可能会成为系统瓶颈，支持端口映射

`Web服务器` 可以使用任意 OS

`Web服务器`的IP地址必须和` LVS` 的某个网卡地址在同一个局域网内。

### LVS-DR 模型

预知原理详情请参考： [lvs-dr 详解](https://blog.csdn.net/brad_chen/article/details/47807281)

由于 LVS-DR 配置较复杂，这里简要概括下， 主要是利用了数据在二层网络传输的特性，在数据包到达 LVS 时，这个包的 MAC 地址其实是 LVS 的 MAC 地址，然后 LVS 准备将这个包转发给Web服务器的时候，将这个包的目标 MAC 地址修改为其中某个 Web服务器的 Mac 地址，然后再将包发送出去，这时身处同一个物理网络下对应mac地址的 Web 服务器就会收到数据包。

这里需要保证的是： 数据包流入这个物理网络后，会通过 IP 来查找 MAC 地址，所以我们通过静态绑定来实现将包只发给 LVS， 因为此时，这个网络下所有主机的 IP 地址都是一样的。但是 Linux 是不允许一个网段内有相同的 IP 地址的，并且这些地址还会广播，所以要做的就是重新编译 Web服务器的 Linux 内核，将 IP 地址监听在本地回环地址上，并且只监听，不会向网络发送广播。

* 通过静态绑定，保证路由器将目标 IP 为 VIP 的请求报文发送给 `LVS`
* 修改 Web服务器内核参数，让其监听某个IP地址（公网私网都可以），关闭广播功能
* Web服务器和LVS必须处于同一物理网络中
* 不支持端口映射
* Web服务器可以是大多OS

* 请求报文经由 LVS 调度，但响应报文一定不能经由 LVS（Web服务器的网关不能指向 LVS）

### lVS-TUN 模式

不修改请求报文 IP 首部，而是通过在原有的 IP 首部，再封装一个 IP 首部。

`Web服务器` IP 地址必须是公网IP，LVS至少需要两个公网地址

`Web服务器` 的网关不能指向 `LVS`

请求报文必须经由 `LVS` 调度，但响应报文一定不能经由 `LVS`

不支持端口映射

`Web服务器` 的 OS 必须支持隧道功能

### LVS-FULLNAT 模式

* 请求流程

  客户端对 `Web服务器` 发送请求，这里的 `Web服务器` 并不是真实的 `Web服务器`，而是 LVS简称调度器（Director），`调度器` 收到请求后，将请求从另一块网卡的内网地址发出，并且将包的源地址改为 客户端IP地址变更为调度器的私有地址，将目标地址改成集群中某台服务器的IP地址，然后经过内网路由器路由到真实的Web服务器进行处理。

* 响应流程

  Web服务器发送响应请求时，会把目标地址改为调度器的地址，源地址改为自己的IP地址，然后经过路由器路由后到达调度器，调度器在把响应发送给客户端前将包的目标地址改为客户端IP地址，把源地址改为自己的IP地址。

* 特性：

  LVS 其中一块网卡地址需要是公网地址

  `Web服务器` 和 `LVS`的某张网卡需要都是私网地址，二者无需在同一网段中

  `Web服务器` 接收到的请求报文的原地址为 `LVS 私有地址`，因为要响应给 LVS

  请求报文和响应报文都必须经由 LVS

  支持端口映射

  Web服务器可以使用任意 OS






---
title: 配置docker-openvpn转发指定网段流量
date: 2020-10-28 21:04:05
tags: [openvpn, tun, tap]
category: vpn
---

[Github-docker-openvpn地址](https://github.com/kylemanna/docker-openvpn)

新增加一台服务器，于是就把以前的虚拟机删除了，关一台性能低的服务器（考虑到节约用电），重新配置下vpn服务，才可以轻松愉快的访问家里的服务器。

## openvpn 两种模式的区别

* tap 模式： 这种模式可以实现桥接功能，处于网络层中比较底层的地位，就相当于你直接拿网线连接上了路由器，或者你就在家里通过 wifi 连接了路由器。如果你的 vpn 服务器是直连路由器（大概意思就是你在路由器上面看到的ip 和你在你电脑上看到的内网ip 是一致的），那么远在其他地方的设备连接上了vpn，你可以在路由器上面发现一个IP，这个IP既不是wifi连接的，也不是网线连接的，而是通过 vpn 连接的。即使你不在路由器旁边，依旧可以通过 vpn 实现在同一个网段。

  这种方式比较底层，会接收到一些群发的包，可能会导致耗费流量增大。

  使用场景：这个应该是在数据链路层打通了一条通路，所以主要是用在某些需要数据链路层支持的应用。 比如 Itunes，我可以在 nas 服务器上面放很多歌曲，然后使用 itunes 去读取，并且作为歌曲的播放器，因为这种模式需要处于同一网段，不能是子网，所以需要使用这种桥接来进行实现。

* tun模式： 相当于打通了一条隧道，拿到的ip是vpn分配的私有ip，就相当于在路由器子网中的子网，一般来说去访问家里的内网设备是没有问题的，但是如果家里的设备要反向来访问就不行了，而 tap 模式可以实现，在tap模式下甚至，我在连接 vpn 的情况下，晚上回到家里，打开家里的电脑可以直接连接公司的电脑。
<!--more -->



关于两种模式的选择，还是比较推荐 tun 模式，简单易用。 一般是用不到 tap 模式的。



## docker-openvpn

由于以前的机器及tap模式的限制，索性直接用了一台虚拟机来实现vpn服务，现在对 tap 也没有那么大的需求了，所以就简单点，直接使用 docker 来实现 vpn 服务。

概括一下步骤，以及需要注意的地方：

```
# 直接在终端里对一个变量进行赋值，这个值将是你的 vpn 配置文件存储的地方
# 这种方式也是 docker 推荐的方式，可以手动命名，如果你没有命名的话，
# 他存储的位置都是一样的，但是是一串不知名的乱码，虽然以后可以通过其他 docker 命令
# 进行查看具体是哪个名称，存储在哪里，但是容器多了后还是比较麻烦。
1. 命名
OVPN_DATA="ovpn-data-example"
# 创建一个名字为 ovpn-data-example 的存储空间，位于 /var/lib/docker/volumes/ovpn-data-example， 提醒，在修改原来的配置文件的时候记得备份，否则可能造成不必要的麻烦。
2. 创建存储空间（我重建了一次，然后我先手动先删除了这个文件夹，第二次告诉我创建成功，然而我去指定文件夹却没看到，最终手动创建(mkdir)才搞定）
docker volume create --name $OVPN_DATA
3. 初始化：
	3.1 将 udp://VPN.SERVERNAME.COM 中的 VPN.SERVERNAME.COM 改成你自己的地址
	docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_genconfig -u 				udp://VPN.SERVERNAME.COM
	3.2 
	docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm -it kylemanna/openvpn ovpn_initpki
4. 开启vpn服务
docker run -v $OVPN_DATA:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN kylemanna/openvpn
5. 生成客户端证书 (生成证书的时候，如果要图方便省事，让你输入任何东西，你都输入同样的就可以了)
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm -it kylemanna/openvpn easyrsa build-client-full CLIENTNAME nopass
6. 导出客户端证书 
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_getclient CLIENTNAME > CLIENTNAME.ovpn
7. 然后将 CLIENTNAME.ovpn（可以改变文件名） 传输到客户端，导入 openvpn 就可以使用了，如有问题可以 docker logs id 查看日志。


```



## 选择性的转发流量

因为家里的宽带虽然给了公网IP，但总不能开个服务就暴露出来吧。所以还是需要一个内网环境来进行使用。

比如某台 192.168.1.100 的机器开了一个 nginx 服务，我需要访问，我可以直接输入 192.168.1.100 就去访问了，而不需要配置内网穿透或者是端口转发。

所以目标也很明确了，只需要转发 192.168.1.1/24 这个网段的流量。然后就和以前一样开始在 CLIENTNAME.ovpn 中修改配置了：

```
route-nopull
route 192.168.1.0 255.255.255.0
```

服务端配置其实不需要动，重试了很多次还是全部流量都走vpn，怎么找都找不到，最后又回到 GitHub 仓库的文档一看，发现了问题，生成出来的客户端配置文件，里面默认设置了转发所有流量，而我的配置都加在前几行，所以也就没有生效，解决方法就是删除最后一行（藏得真够深）的 `redirect-gateway def1` 即可。



## 全量转发

如果你就是需要全部流量都走vpn，那么可能会发现连上了 vpn 后，可能可以访问你的内网服务，但是无法访问其他网站了，ping 一下 114.114.114.114 可能是正常的，但是ping baidu.com 可能就不正常了，这个其实作业也已经提到了（认真读文档的重要性！！），因为设置了默认全量转发，所以你的 DNS 如果设置的是内网 DNS，那么可能就会出现 DNS 失效的情况，解决方法，设置 DNS 为一些公共（公网）的 DNS，如 114.114.114.114、8.8.8.8 等等。

如何确定我的 DNS 是内网 DNS？ 可以看下网络设置里面 DNS 是否是自动，如果是自动可能就是内网，如果 DNS的IP和你的ip地址属于同一个网段，也就是内网了，这里不多阐述了。

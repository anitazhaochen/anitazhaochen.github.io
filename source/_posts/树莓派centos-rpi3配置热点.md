---
title: 树莓派centos-rpi3配置热点
tags: [ARM, 树莓派]
category: 树莓派
date: 2018-11-15
---


最开始的准备：如安装系统可参考

[为树莓派装上 CentOS 7 系统](https://sspai.com/post/42793)



2018.11.20日更新： 通过下面的方法，有一个问题，就是我发现 WIFI 第一次可以连上，然后过一会就连不上了，通过 Wireshark 抓包分析，可以看出一直在发送广播请求，比如 DHCP 请求，导致 DHCP 一直无法成功获取 IP ，所以，有两种可能，第一 DHCP 配置有问题，第二，不兼容导致。 

解决方法： 使用 dnsmasq 替换 dhcpd。

------
<!--more -->


![image-20181115175027268](/images/image-20181115175027268.png)

## 一：添加 EPEL 软件源

EPEL 软件源收录了很多自带软件源没有的常用的软件。在 x86 版 CentOS 上，我们可以很方便地用 `yum -y install epel-release` 来添加 EPEL 软件源，但是在 ARM 版 CentOS 上就行不通了。
不过我们可以通过手动修改 `yum` 源的配置文件来添加它。

执行如下命令：

<!--more -->
<!--more -->
```shell
cat << EOF > /etc/yum.repos.d/epel.repo
[epel]
name=Epel rebuild for armhfp
baseurl=https://armv7.dev.centos.org/repodir/epel-pass-1/
enabled=1
gpgcheck=0
EOF
```



## 二：安装需要的软件

- **hostapd** : 至今为止用得最广泛的无线热点程序，稳定而强大，几乎你能想到的无线路由器都在使用它。
- **dhcpd** : 强大的 DHCP 服务器（动态主机服务），适合用于管理多个大型网络的主机地址自动分配。

注意：

开热点需要有能够支持 AP 模式的无线网卡，如果你不确定的话可以这样查看

`iw list`

如果没有 iw 命令，可以使用 yum 安装一下。

如果里面 **Supported interface modes:** 有　"AP" 那么意味着你的网卡支持。

* 安装 hostapd 

  ```shell
  yum install hostapd
  ```

* 安装 dhcpd

  ```shell
  yum install dhcp
  ```

* 安装完成后，可以使用 systemctl 很方便的管理

  ```shell
  systemctl start|stop|enable|disable hostapd|dhcpd
  ```



## 三： 配置安装的软件

首先我们需要配置 hostapd ，它的默认配置文件在 `/etc/hostapd/hostapd.conf` 。

```shell
#hostapd 提供一个控制终端 hostapd_cli，这里配置终端接入的细节
ctrl_interface=/var/run/hostapd
ctrl_interface_group=whell

#一些比较普通的配置。。。。
macaddr_ac1=0
#这里配置使用哪一种认证方式，0 就是开放， 1 使用 WPA 系列，2 为任意，建议选 1
auth_algs=1
ignore_boardcast_ssid=0

#下面配置 WPA 和 WPA2 的选项
wpa=3
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

#这里配置你的 WI-FI 密码
wpa_passphrase=SomePassword

#配置驱动，这里一般不需要更改
driver=nl80211

#配置 WI-FI 硬件，这里改成你 WI-FI 硬件的设备名称，可以用 nmcli device show 或者 ifconfig 查找
interface=wlp2s0
#这里配置频率模式
hw_mode=g
#频道
channel=7
#SSID，WI-FI 名称
ssid=SSID_NAME
#是否用 UIF-8 编码 WI-FI 名称，启用的话就能使用各种字符来命名 WI-FI 了，但在 Windows 上面普遍会出现 WI-FI 名称乱码问题
utf8-ssid=1

```



保存之后别急着启动，因为默认情况下网卡受 NetworkManager 托管，所以 hostapd 无法管理无线网卡。执行下面命令以让 NetworkManager 不再托管无线网卡。

```shell
nmcli device set wlan0 managed no // wlan0 是我的网卡名字，名字不同自己替换
```

然后可以通过 下面命令进行启动 hostapd 如果没有报错，则成功。

```shell
systemctl start hostapd 
```

接下来先给启动了的无线网卡配置 IP 地址

```shell
ip addr add 192.168.2.1/24 dev wlan0
```

但是这个是临时的。找了一会试了好几种静态无限网卡设置静态IP 的方法，都不怎么奏效，最后的解决方法：

`vim /etc/rc.local`

如果有 `exit 0` 请在它的上面添加(没有的话，直接在最后添加就行)

使用 `which ip`先查看一下 ip 的路径。

`/usr/sbin/ip addr add 192.168.2.1/24 dev wlan0 `

最后不要忘了，要给rc.local可执行权限。

 `chmod +x /etc/rc.d/rc.local`

然后每次重启都可以生效。

这个地址相当于平时配路由器的路由器地址，可以根据你的需要改成其他的，不过注意下面的所有配置都得跟着改动。

*后面的 `/24` 是 `255.255.255.0` 的缩写，如果想改动请自行查询子网掩码的格式

dhcpd 的配置文件默认在 `/etc/dhcp/dhcpd.conf`，这个文件夹需要 root 权限才能进入。

```shell
#让 DDNS 自动刷新，适合用在这种经常变动的网络中
ddns-update-style interim;

#监听 192.168.2.0 这个子网
subnet 192.168.2.0 netmask 255.255.255.0 {

        #设置自动派 IP 的范围
        range 192.168.2.10 192.168.2.250;

        #默认的 DNS 服务器
        option domain-name-servers 223.6.6.6,223.5.5.5;
        #告诉客户端路由器地址
        option routers 192.168.2.1;
        #告诉客户端子网掩码
        option subnet-mask 255.255.255.0;
        #告诉客户端广播地址
        option broadcast-address 192.168.2.255;

        #IP 默认租期和最大租期
        default-lease-time 86400;
        max-lease-time 172800;

}

```

保存之后启动 dhcpd 服务，启动没有问题就可以了。

```shell
systemctl start dhcpd
```

> 在这里并没有考虑使用 nftables ，因为它对内核的某些模块有要求。所以我就直接使用了 ipbtales 进行下面的 nat 操作。



参考[hostapd + dhcpd + nftables 在 CentOS 7 上开 WLAN 热点](https://www.jianshu.com/p/d1616623cf35)



## 设置 IPV4 转发

在我们成功的转发我们的包之前，还需要做最后一件事。使用如下命令，可以立即生效不用重启：

`sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`

但是上面的重启之后就失效了。

我们可以打开`sysctl.conf`文件`vim /etc/sysctl.conf`

如果没有此字段（net.ipv4.ip_forward）则添加，如果有的话，把它的值改为 1

`net.ipv4.ip_forward=1`

我们需要将PI的WIFI连接分享出去，通过配置NAT在wlan0和eth0之间。使用下面命令实现。

```shell
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE 

sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT 

sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT 
```

然而，我们需要这些规则去应用于我的Pi在每次重启机器的时候，所以

`sh -c "iptables-save > /etc/iptables.ipv4.nat`

去保存这些规则在` /etc/iptables.ipv4.nat` 文件中。现在我们需要每次重启机器时都要去启用这些规则，所以还需要配置这个文件

`vim  /etc/rc.local`

在这个文件的"exit 0"这行的上面加入下面的内容：

`iptables-restore < /etc/iptables.ipv4.nat `

**差不多成功了！**

现在我们只需要去重启一下我们的服务就好了：

`systemctl restart hostapd`

[使用HOSTAPD使你的树莓派3成为WiFi热点（AP）](http://www.embeddedlinux.org.cn/emb-linux/entry-level/201703/18-6294.html#)

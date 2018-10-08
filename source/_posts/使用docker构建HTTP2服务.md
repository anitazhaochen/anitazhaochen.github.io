---
title: 使用Docker构建 HTTP2 服务
date: 2018-10-8 13:00
tags: [docker, HTTP2, NGINX]
category: HTTP2
---

国庆假期折腾了半天，把 NGINX 卸载了又装，一次又一次重新编译，来配置 HTTP2 和 基于 OPENSSL 的 TLS1.3 以及 HTTP2 的一些特性，如 HTTP2_PUSH 等等。总之就是很麻烦。于是就想到了 Docker。

## 拉取 NGINX 镜像

使用

`# docker search nginx`

可以看到以下内容：

![image-20181008143929082](/images/image-20181008143929082.png)

我们可以用第一个官方的就可以。
<!-- more -->

使用

`# docker pull nginx `



![image-20181008144227285](/images/image-20181008144227285.png)

不写版本号，它默认拉取最新的。

使用

`# docker run -d -p 80:80 nginx`

![image-20181008144413912](/images/image-20181008144413912.png)

就可以运行了。

使用

`# docker ps`

查看是否运行成功，如果是这样就成功了。

![image-20181008144559621](/images/image-20181008144559621.png)

如果什么都没有，那就是出错了。可以使用

`# docker logs 镜像ID `

来查看，镜像ID 就是运行 docker run 之后会出来很长的一串字符串

![image-20181008144751519](/images/image-20181008144751519.png)

其中 `77ea9bc399a1c9123bc0adb77cdcc52c5777fca53cacc325dd94e06f5234392a` 就是容器 ID

通过

`# docker exec -i 容器ID nginx -v `

来查看 nginx 版本

![image-20181008144915169](/images/image-20181008144915169.png)

我这里是最新的 nginx 版本，它是支持 HTTP2 、HTTP2_PUSH 的。

好了，至此 NGINX 版本的 Docker 就配置完成了。



## 配置我的博客



我的博客是基于 HEXO 的，以前托管在 GITHUB ， 但是 GITHUB 毕竟服务器在国外，访问异常的慢，所以就搞了一台阿里云服务器，在 github 和 我的服务器各方一份配置。在 GITHUB 备份我的源文件， 在服务器上面放 hexo 生成好的文件，这样就可以加速访问，相当于自己搭了静态网站服务器。



我的博客的目录是 /home/git 

因为 HTTP2 强烈建议使用 HTTPS ，所以我在 cheapname 上面买了一个证书，来完成 HTTPS。

我的 nginx 配置

```shell
  server {
  listen 80;
  server_name enjoyms.com;
  rewrite ^(.*)$ https://${server_name}$1 permanent;
}

server {
	listen 443 ssl http2 default_server;
	listen [::]:443 ssl default_server;
  	server_name enjoyms.com;
  	ssl_certificate new.crt;
  	ssl_certificate_key server.key;
  	ssl_session_timeout  5m;
  	ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;      #指定SSL服务器端支持的协议版本
  	ssl_ciphers  TLS13-AES-256-GCM-SHA384:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-128-CCM-8-SHA256:TLS13-AES-128-CCM-SHA256:EECDH+CHACHA20:EECDH+CHACHA20-:EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
  	ssl_prefer_server_ciphers   on;    #在使用SSLv3和TLS协议时指定服务器的加密算法要优先于客户端的加密算法
	location / {
	  	root /home/git;
    	http2_push /images/myself.jpg;
	}
}
```

在我的 nginx 的配置文件我直接放在了主目录下：

/root/nginx_docker.conf

证书文件：

/root/new.crt

/root/server.key

一切都准备好之后，就可以把本机的文件挂载到 docker 里面，然后启动容器。

```shell
docker run  -d -p 80:80 -p 443:443 -v /home/git:/home/git -v /root/nginx_docker.conf:/etc/nginx/conf.d/nginx.conf  -v /root/server.key:/etc/nginx/server.key -v /root/new.crt:/etc/nginx/new.crt  --privileged=true --restart=always nginx
```

因为使用了 HTTPS，NGINX 对访问 80端口的重定向到了 443 端口，所以暴露出了两个端口，分别是 80 和 443， 否则别人访问80端口就无法显示了。



关于配置 http2_push 的时候的一些问题：

​	http2_push 的文件需要被当前页面所需要，否则在 chrome 浏览器的 network 是看不到服务器 push 文件的。

## 本博客支持 HTTP2 、 TLS1.3



### 关于 TLS 1.3的新特性

- 支持0-RTT数据传输 
- 废弃了3DES、RC4、AES-CBC等加密组件。废弃了SHA1、MD5等哈希算法。 
- 不再允许对加密报文进行压缩、不再允许双方发起重协商，密钥的改变不再需要发送change_cipher_spec报文给对方。 
- 握手阶段的报文可见明文大大减少。

[TLS1.3 参考](https://zhuanlan.zhihu.com/p/28850798)

我的 VPS 是阿里云的，系统是 ubuntu 16.04 TLS。

nginx 在 1.13.9 之后 就支持 http2_push 了。

 [nginx 参考](https://www.nginx.com/blog/nginx-1-13-9-http2-server-push/)

openssl 升级到 1.1.1 就支持 TLS 1.3 

[OpenSSL 参考](https://www.openssl.org/blog/blog/2018/02/08/tlsv1.3/)

nginx 底层 是基于 openssl 库的，所以在编译的时候指定 OpenSSL 即可。



### 关于 namecheap 给的两个证书文件

如果直接无视`ca-bundle`文件，那么用`crt`文件和之前生成的`key`文件配置`ssl`后，会发现有的浏览器提示不安全，查了下问题后，发现证书链不完整导致的，感觉不能忽视`ca-bundle`文件。

首先需要将颁发的`crt`和`ca-bundle`文件合并成一个新`crt`文件，登录`vps`运行命令：

```
cat xxx.crt xxx.ca-bundle > new.crt  #crt和ca-bundle文件位置填对
```

然后用新的`crt`做证书文件，`key`还是用之前生成的！


---
title: requests中的sni
date: 2019-11-07 19:12:13
tags: [Python, requests, TLS]
category: Python
---

使用 Python2 中的 requests 访问 https 网站的时候，会出现这样的错误：

```python
requests.exceptions.SSLError: [Errno 1] _ssl.c:503: error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed
```

原因是： Python 2.x 不支持 SNI。

## SNI

全称 Server Name Indication。 **SNI 是 TLS 的一个扩展**

了解 https 的人都知道，https 会首先建立 SSL 握手，然后才会传输数据。
<!--more -->

SNI 的作用是 在请求头部headers 中加入一个 Host 字段，这样就可以让 Nginx、Apache等 http 服务器可以通过Host字段来判断请求是要访问哪一个站点。这样就可以实现一台服务器上面部署多个不同域名的网站。而使用 https 后， 在 ssl 握手的过程中，是需要服务器提供证书的，而服务器并不知道这个请求请求的是哪一个host， 所以就就无法挑出对应的整数来供客户端校验。

有了 SNI 后，服务器可以通过 SSL 过程中的 Client Hello 中的 SNI 扩展拿到用户要访问网站的 Server Name，进而发送与之匹配的整数，顺利完成 SSL 握手。

而对于 Python 2.x 是不支持 SNI 的。

[Python  Requests throwing SSLError](https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror)



## 临时解决方法

1. 关闭校验，就是不校验服务器端的证书

   ```python
   response = requests.get(url, verify=False)
   ```

2. 安装 requests 的时候，安装额外的支持 

   ```python
   pip install requests[security]
   # 或者已经安装requests了执行下面的
   pip install pyopenssl ndg-httpsclient pyasn1
   ```

   ```python
   # 在requests 2.22.0 版本中，会自动帮我们尝试获取 SNI 的支持
   
   # Attempt to enable urllib3's SNI support, if possible
   try:
       from urllib3.contrib import pyopenssl
       pyopenssl.inject_into_urllib3()
   
       # Check cryptography version
       from cryptography import __version__ as cryptography_version
       _check_cryptography(cryptography_version)
   except ImportError:
       pass
   ```

   


---
title: Cookie不分协议和端口
date: 2020-07-31 17:38:41
tags: [http, cookie]
category: http
---

最近在写自己的端口上测试一些功能的时候，发现偶尔需要登录，偶尔不需要登录，有些情况下，只想看下 api 是否正确，也就没有搭建前端的代码。

经测试： 发现 Cookie 只跟域名有关，不区分协议和端口。

比如你在 127.0.0.1:8080 端口登录了一个网页，如果你的服务端的 session 是放在如 memcache 里面即共享的，那么你再开一个其他端口相同的服务，你会发现状态和8080端口的状态是一样的， 就是因为，浏览器把 8080 的 cookie 也发送到了另一个端口上。因为 Cookie 跟 协议及端口无关。

Cookie 的作用域： Domain 和 Path 。

Domain 指定了哪些主机可以接受 Cookie，如果不指定，默认不包含子域名。如果指定了 Domain， 则一般包含子域名，因此指定 Domain 比省略它的限制要少。但是，当子域名需要共享相关用户信息时，可能会有包住。

例如：

```
<!--more -->
Domain=mozilla.org   
则 Cookie 也包含在子域名中如  dev.mozilla.org
```

Path 属性：Path 标识了主机下的哪些路径可以接受 Cookie （该 URL 路径必须存在于请求 URL 中），义字符 `%x2F` 作为分隔符，子路径也会被匹配。例如：设置 `Path=/docs`, 则以下地址都会匹配：

* /docs
* /docs/web/
* docs/web/http
* ......

[MDN 参考_HTTP_COOKIE](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Cookies)

Cookie 一般来说相对比较敏感，如果服务端不想让前端的 js 访问 Cookie 怎么办呢， 其实可以加一个 httponly 字段。


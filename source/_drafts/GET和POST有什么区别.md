---
title: GET和POST有什么区别
date: 2018-10-15
tags: [HTTP, 网络协议]
category: HTTP
---

> 没想到一个也算是大厂的大厂竟然也问了这个问题，然后我说了一些普遍的回答，并且告诉她是错的，竟然被扔来了鄙夷的眼神，接下来就是，好了你回去等通知吧。   （想当年我回答这种问题的时候，还是对 http 一知半解的时候，现在了解了，却被人鄙视了。）



GET 和 POST 的区别？

1. POST比GET安全，因为数据在地址栏上不可见。

​	就因为 GET 的参数可以放在 URL 地址上， POST 参数放在 BODY 里，所以 GET 就比 POST 安全？  这和五十步笑百步有什么区别？ 要安全，那用 https 啊，这根本就不是 GET 和 POST 关心的事情。	

​	GET 和 POST 在 **实践** 上有很大的区别。非要让我咬文嚼字，说在 **实践** 上的区别，然后再解释一遍实践是什么吗

**HTTP 是应用协议！！！！不是传输协议！！！！！！！！**

如果站在应用协议的角度，任何应用程序都少不了“增删改查”功能，HTTP 协议的方法除了 POST、GET外还有 DELETE和PUT，他们刚好是对应的：POST是添加，DELETE是删除，PUT是修改，GET是查询，至于增删改查的具体内容每个应用都不同，但是他们都可以用URL定位，内容在 HTTP 里叫做“资源”，所以 URL 叫“统一资源定位符”。RESTful API 正是按照这种方式来定义的，大家都用 HTTP 协议提供 API 不是偶然，而是就是为此而设计的。



还有诸如以下的答案：

1. GET使用URL或Cookie传参。而POST将数据放在BODY中。

2. GET的URL会有长度上的限制，则POST的数据则可以非常大。

从浏览器的角度：

​	HTTP 协议对 GET 和 POST 都没有对长度的限制。

​	HTTP 协议明确指出了， HTTP 头和 Body 都没有长度的要求。

而对于 URL 长度上的限制，有两方面的原因造成：

  1.浏览器的限制。

 	2. 服务器的限制。（安全性、稳定性考虑）

而 GET 也可以在 Body 中存放数据，但是这样貌似就违反了 HTTP 协议。



 RFC 文档并没有说这两种方法的区别，区别在于我们平时怎么去使用它。

​     我对于GET和POST的理解，是纯粹地来源于 HTTP 协议。他们只有**一点**根本区别，简单点儿说，一个用于获取数据，一个用于修改数据。

​	GET 是幂等的，POST 不是幂等的。

​	[知乎](https://www.zhihu.com/question/31640769?rf=37401322)

​	[一篇博客](http://www.cnblogs.com/nankezhishi/archive/2012/06/09/getandpost.html)

​	[RFC规范](https://tools.ietf.org/html/rfc2616)
---
title: 本博客更新日志
tags: [Nginx, Blog]
category: Blog
date: 2018-1-10
---

## Nginx1.15.6

| 2018-11-06 | [nginx-1.14.1](http://nginx.org/en/download.html) stable and [nginx-1.15.6](http://nginx.org/en/download.html) mainline versions have been released, with fixes for[vulnerabilities in HTTP/2](http://nginx.org/en/security_advisories.html) (CVE-2018-16843, CVE-2018-16844) and [the MP4 module](http://nginx.org/en/security_advisories.html)(CVE-2018-16845). |
| ---------- | ------------------------------------------------------------ |
|            |                                                              |

[nginx官网](http://nginx.org/)

在 2018-11-06 爆出了 http2 的一些问题。

  

## Nginx 1.15.8

2019-12-28 重新编译 Nginx ，及 TLS1.3 升级到 Nginx 1.15.8。



2019-1-1 重新编译 Nginx，加入 OpenResty 里面的一些库，支持 lua 可以通过写 lua 来写 Nginx 扩展。

[源码](https://github.com/anitazhaochen/generate_http2_push_config.git)

2019-1-3 通过 lua 脚本，配合 http2_push 实现，自动 push 功能。



考虑到两点：

 	1. http2_push 如果是动态网站，完全可以在渲染后返回通过 header 加上 Link 字段来决定哪些资源需要推送
 	2. 不管是自动推送还是手动推送都需要人工参与，进行决定推送哪些。静态网站，则比较麻烦。


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


## 搭建了GitLab服务器


2020-4-20 搭建了基于 Docker 的 GitLab 服务器

想把博客迁移到自己私有的GitLab上面进行托管

需求：不使用 GitLab page， 还是把博客独立出来，通过 nginx做服务器 访问

坑点：GitHub 的 page 其实可以理解为一种特殊的仓库，设置默认 master 分支后，利用 hexo 的发布插件，它只会将生成的静态文件,
即 public 目录下的内容推送到 github page 的 Master 分支。其他分支可以设置 .gitignore 来忽略如 public 文件等，来作为博客
源码备份使用。

而 GitLab 这里，我原本以为和 Github 差不多的，然后经历了各种配置，每次都发现，除了 .gitignore 忽略的文件，其他文件都原封不动的
推送到了我设置的推送分支上，简而言之就是推送的都是源文件。

阅读了一些关于 GitLab Page 的文档，发现 GitLab Page 和 GitHub Page 定位是不同的，

GitHub Page：本地生成静态文件，然后推送， Page 完成。

GitLab Page: 直接将所有代码推送到仓库，然后通过 ci 操作进行生成静态文件，进而 Page 完成。 这里的 GitLab 仓库思想更侧重保存源码。



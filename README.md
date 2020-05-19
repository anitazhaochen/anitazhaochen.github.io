---
title: 本博客更新日志
tags: [Nginx, Blog]
category: Blog
date: 2018-1-10
---

## 2020-5.19 更新

部署博客方式, 启用 `hexo d`
使用 sh hexod.sh 进行部署


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


## 弃用 hexo 的 deployer 插件

备份！！！ 十分重要
以前使用在 github 上另外建立新分支来保存源代码, 我总觉得不是那么的方便，要想实现每次更新，需要如下两步操作:
1. hexo d 先上传静态文件到 仓库的 master 分支
2. 备份：执行 `git add . && git commit -m "xxx" && git push origin branch`
在日常使用的过程中，我经常忘记备份这个操作,久而久之就以为一个 `hexo d` 就实现了所有操作。
而这次转移 GitLab，发现 hexo 的那个 git 插件如果上传的是 gitlab，执行一次之后，必须删除 `.deploy` 开头的文件夹, 否则再次执行就会报错
上面的问题，暂时还没有找到好的解决方法。

3. 另一方面，本着折腾的精神。既然有了私有GitLab，那就用了它除了托管其他的一些功能，
这里用到了 webhook, 简而言之这个东西就是，仓库发生操作的时候，会给你发一条 http 请求，
然后，你可以决定应该干什么事。配合一个部署令牌，可以实现权限仅限这个仓库，并且可以设置只读。
我这里做的很简单，就是代码提交后，自动拉 public 文件夹里的文件到服务器上，重新进行
部署。这样，我的博客就更新了。
为何如此麻烦，直接一个 rsync 或者 服务器上建一个 git 家目录不行吗， 其实在这之前，
我用的就是在服务器上面建一个 git 家目录，然后 nginx 配置到这个目录，难过于 aliyun
把我4年前读大一时候，申请的 ICP 备案号给我注销了。我的网站就访问不了了。 目前因为
家里宽带有公网IP，加端口映射，反向代码，访问正常。
但是呢，服务器是一台群晖，rsync 免密ssh， 需要设置家目录权限，而群晖某些软件又依赖
这个权限，所以两者不可兼得，最后只好关闭了 ssh 登录功能，另一方面也处于安全考虑
既然 GitLab 在内网，博客服务器也在内网，那就 webhook 加自动拉代码部署吧。
webhook 请求地址, 写了一个简单 flask 项目,然后封装成 Docker 来进行热更新博客。
（有的时候我在想，用那么麻烦吗，为啥要买这个群晖，直接搞台Linux 服务器不好嘛！！）


## hexo 改进方案

尝试了 hugo，速度确实很快，但是皮肤很少，没有找到自己喜欢的皮肤

~~ 1. 通过命令的方式手动推送 public 里的文件到 GitLab Master 分支 ~~

~~ 2. 通过命令手动推送 dev 分支的博客原文件到 GitLab dev 分支 ~~

~~ 3. 通过 webhook 功能, 让 Docker 自动拉取 Master 分支进行热部署 ~~

~~ 4. 命令太多，更新一次太累，把命令写成脚本执行 ~~

上面的方法在实践的时候遇到一些问题，觉得不太合适。

新的方法：

1. 推送包含 public 的源文件到 GitLab Master 分支

2. Docker 拉取 Master 分支后，将 public 文件夹里的内容进行热部署














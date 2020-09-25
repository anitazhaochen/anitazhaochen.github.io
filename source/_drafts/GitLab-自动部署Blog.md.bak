---
title: GitLab 自动部署Blog
date: 2020-09-25 11:31:20
tags: [GitLab, Docker]
category: Blog
---

首先在 GitLab 上面创建项目，打开项目，然后在左侧页面点击 Setting --> Integrations 然后输入回调的 url 以及设置在发生哪些事件时通知， 因为我这里主要是想实现我推送新的内容到 GitLab， 然后我的博客服务器可以收到 GitLab 发送过来的通知， 进而实现 我的博客服务器可以去自动拉取代码进行部署。



不过，如果你输入的是一个私有地址，如 192.168.xxx.xxx 这样的一看就是内网地址，会提示你： **url is blocked requests to the local network are not allowed** 。解决方法： 需要先登陆管理员账号--> Admin area --> Setting --> NetWork 找到 **Outbound requests ** 把  Allow requests to local network from hooks and services 打上勾保存就可以了。



从 GitLab 发请求到 服务器时，会让你设置一个 token ， 这个 token 是让你用来验证这个请求是来自 GitLab 服务器的。



服务器收到请求后，接下来会从 GitLab 拉取代码，如果直接放 ssh，是否会权限有点大了，可以在 setting 里面点击 Repository 然后在 Deploy Tokens 里面申请一个 Token 。
<!--more -->
<!--more -->

注意，这个申请后的结果 包含一个 username、一个 token ，这两个都需要用，并且是特定格式拼接在 gitl clone  请求的 url 上面。 具体细节可以看 gitlab 文档，这里给一个示例：

```
git clone https://${username}:${token}@gitlab.enjoyms.com/anita/blog.git
```

以上： `{$username} 需要替换成你的， ${token} 也换成你的，然后@之后的就是你的仓库地址了`。设置成上面这种的后就可以拉取代码了。

关于后面的部署也就是几个命令执行一下而已，就不阐述了。


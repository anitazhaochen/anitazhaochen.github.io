---
title: 配置grafana使用GitLab-OAuth认证
date: 2020-10-28 21:03:12
tags: [GitLab, Grafana, OAuth]
category: GitLab
---

## GitLab

关于 GitLab 方面的问题，其实以前已经写过了，以前是在黑群晖上面使用，但是这个黑群晖越使用越发恶心，动不动死机系统无响应，终于在某天开机的过程中告诉我需要重装系统（可能和我直接暴力ssh上去操作了一波又一波有关）。最终的结果就是应用数据全丢，因为 GitLab 是以Docker形式部署的，所以也没了，不过还好，电脑的原始资料还在，就是费点时间重建一下。

并且这个黑群晖的机器性能也不行，蜗牛星际矿机。干啥啥不行，我都问我自己为啥不直接装个 Linux。念在我还是几T数据在上面，还是先忍忍了。换台机器吧。

## Ubuntu 20.04 部署 GitLab

还有人说自己搞 Linux 部署会比较麻烦， 这个我肯定，但是也不是那么麻烦，毕竟现在不跟以前一样了，部署过程不叙述了，GitLab 文档写的十分清楚，就是一些配置可以说一下。

由于我是内网主机部署，但是我有公网IP，所以几乎所有的服务我都需要进行转发。

在转发的基础上，还是不能通过域名进行到底给内网的哪个服务，所以在路由器做了端口转发后，还需要一个反向代理，我使用Nginx做了反向代理。
<!--more -->

然后问题就来了，编辑 `/etc/gitlab/gitlab.rb` 配置文件中的 external_url：

`external_url https://xxxxx.com`

简单解释一下，这个其实就是为了让你在 Clone 的时候，如果通过 http/https 进行clone 看到的地址， 它这里会判断你的 url 是以 http 还是 https 开头的，并且还会对 https 为开头的做证书校验，我就是在校验这一步一直不通过，我原本以为某些功能不通过不影响总体功能，其实错了，后面的配置基本失效，GitLab 是可以跑起来的。

如果你和我一样，做了反向代理，那么现在一般都会使用 https 了，直接在反向代理那里使用 https， 在反向代理和 gitlab服务器通信的时候直接http就好。而你改成 http 开头的，那么 Clone 那里就会显示 http 开头的地址，虽然试了下也可以使用，但是不美观（哈哈），继续查文档，发现其实别人早就想好了这种情况，对反向代理也加了一些配置，具体配置:

```
external_url 'https://gitlab.xxxx.com'

##! **Override only if you use a reverse proxy**
##! Docs: https://docs.gitlab.com/omnibus/settings/nginx.html#setting-the-nginx-liste
nginx['listen_port'] = 80

##! **Override only if your reverse proxy internally communicates over HTTP**
##! Docs: https://docs.gitlab.com/omnibus/settings/nginx.html#supporting-proxied-ssl
nginx['listen_https'] = false
```

然后你再重新 gitlab-ctl reconfigure 应该就不会报证书错误了。

## Grafana

GitLab 安装完成后，因为有了 nas 的使用经验，以及丢数据的经历，所以想要监控下服务器的健康状态。发现 GitLab 本身就集成了 Grafana、prometheus、node_exporter 等服务，并且 Grafana 本来就存在一些仪表，所以还是很方便的，当即卸载了树莓派上、Docker 上（哈哈）部署的 Grafana， 当时是为了对比下哪种更好，所以都部署了，其实所有机器部署一个就行。并且 GitLab 还能支持OAuth 登录，以及本身就包含一套仪表组合。



在配置 Grafana 通过 GitLab 的 OAuth 登录的时候，出现了一点问题，可以通过去看日志分析一下：

日志文件：`/var/log/gitlab/grafana/current`

配置步骤：

1. GitLab 以管理员身份登录，点击上面的一个扳手图标，中文为管理中心

2. 左侧一栏点击应用

3. 新建应用： 名称自己填、注意 Redirect URI 为 `https://xxxx.com/-/grafana/login/gitlab` , 注意 https、http 以及把 xxx.com 换成你的gitlab域名。

4. 最好第一次把所有权限都选择上，其实好像只需要一个 api 的权限即可，不过 api 的权限也挺大。

5. 提交保存会出现应用的信息，复制 应用程序ID 到 gitlab.rb 配置文件中，下面是 grafana 在 gitlab.rb 中的配置

   ```
   grafana['enable'] = true
   grafana['gitlab_application_id'] = 应用程序id
   grafana['gitlab_secret'] = 密码
   # 将下面这个设置为 true
   grafana['gitlab_auth_sign_up'] = true
   # 这群组其实是做权限控制的，先在gitlab 上面创建群组，然后把可以访问grafana 的人拉到这个群组里。
   grafana['allowed_groups'] = ['grafana']
   
   # 多往下拉点，GitLab 里装的其他服务基本都是监听127.0.0.1的，把它所有ip都可以访问
   grafana['http_addr'] = '0.0.0.0'
   ```

6. 然后跑  gitlab-ctl reconfigure 没有报错即可。



下面说说我遇到的问题：当时跳转一直报错，然后去看了下 grafana 的日志，日志也不是非常详细，发现了这个 dial tcp 192.168.123.188:443: connect: connection refused" ， 我明明访问的是域名，但是这里却显示的是我 gitlab 的 ip 地址，并且是 443 端口的，这可不行，我反向代理是通过 http 跟 gitlab 通信的，这样估计也访问不了，最终发现，某次配置中我在 /etc/hosts 中配置了 ip: domain 导致的， 然后将其删除即可。

还有一点就是，反向代理记得设置上游需要 gitlab 监听的是一致的

```
2020-10-28_12:54:06.07982 t=2020-10-28T12:54:06+0000 lvl=eror msg="Request Completed" logger=context userId=0 orgId=0 uname= method=GET path=/login/gitlab status=500 remote_addr=192.168.123.2 time_ms=1 size=1754 referer=https://gitlab.enjoyms.com/-/grafana/login
2020-10-28_12:54:58.01519 t=2020-10-28T12:54:58+0000 lvl=info msg="Request Completed" logger=context userId=0 orgId=0 uname= method=GET path=/login/gitlab status=302 remote_addr=192.168.123.2 time_ms=0 size=338 referer=https://gitlab.enjoyms.com/-/grafana/login
2020-10-28_12:54:58.36805 t=2020-10-28T12:54:58+0000 lvl=info msg="state check" logger=oauth queryState=71a4e10b2fc558d19c3bf991043dfd9d43020b8fc0e892e3307aec6f4ae824dd cookieState=71a4e10b2fc558d19c3bf991043dfd9d43020b8fc0e892e3307aec6f4ae824dd
2020-10-28_12:54:58.36902 t=2020-10-28T12:54:58+0000 lvl=eror msg=login.OAuthLogin(NewTransportWithCode) logger=context userId=0 orgId=0 uname= error="Post \"https://gitlab.enjoyms.com/oauth/token\": dial tcp 192.168.123.188:443: connect: connection refused"
2020-10-28_12:54:58.36917 t=2020-10-28T12:54:58+0000 lvl=eror msg="Request Completed" logger=context userId=0 orgId=0 uname= method=GET path=/login/gitlab status=500 remote_addr=192.168.123.2 time_ms=1 size=1754 referer=https://gitlab.enjoyms.com/-/grafana/login
```




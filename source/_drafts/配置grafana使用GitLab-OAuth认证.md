---
title: 配置grafana使用GitLab-OAuth认证
date: 2020-10-28 21:03:12
tags:
category:
---



日志文件

/var/log/gitlab/grafana/current



2020-10-28_12:54:06.07982 t=2020-10-28T12:54:06+0000 lvl=eror msg="Request Completed" logger=context userId=0 orgId=0 uname= method=GET path=/login/gitlab status=500 remote_addr=192.168.123.2 time_ms=1 size=1754 referer=https://gitlab.enjoyms.com/-/grafana/login
2020-10-28_12:54:58.01519 t=2020-10-28T12:54:58+0000 lvl=info msg="Request Completed" logger=context userId=0 orgId=0 uname= method=GET path=/login/gitlab status=302 remote_addr=192.168.123.2 time_ms=0 size=338 referer=https://gitlab.enjoyms.com/-/grafana/login
2020-10-28_12:54:58.36805 t=2020-10-28T12:54:58+0000 lvl=info msg="state check" logger=oauth queryState=71a4e10b2fc558d19c3bf991043dfd9d43020b8fc0e892e3307aec6f4ae824dd cookieState=71a4e10b2fc558d19c3bf991043dfd9d43020b8fc0e892e3307aec6f4ae824dd
2020-10-28_12:54:58.36902 t=2020-10-28T12:54:58+0000 lvl=eror msg=login.OAuthLogin(NewTransportWithCode) logger=context userId=0 orgId=0 uname= error="Post \"https://gitlab.enjoyms.com/oauth/token\": dial tcp 192.168.123.188:443: connect: connection refused"
2020-10-28_12:54:58.36917 t=2020-10-28T12:54:58+0000 lvl=eror msg="Request Completed" logger=context userId=0 orgId=0 uname= method=GET path=/login/gitlab status=500 remote_addr=192.168.123.2 time_ms=1 size=1754 referer=https://gitlab.enjoyms.com/-/grafana/login
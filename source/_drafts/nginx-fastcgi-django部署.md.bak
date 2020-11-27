---
title: nginx+fastcgi+django部署
date: 2020-11-26 10:34:06
tags: [Python, Nginx, Fastcgi]
category: Nginx
---

Django 项目中写一个脚本来启动 fastcgi ，可以添加上一些判断及处理，这样重启或者开启都可以执行。

<!--more -->

```shell
#!/bin/sh

export VENV="/xxx/venv/bin/activate"

PROJECT_PATH='xxx'

PIDFILE="$PROJECT_PATH/xx.pid"
SOCKET="$PROJECT_PATH/xx.sock"
LOG="$PROJECT_PATH/logs/fcgi.log"
ERROR="$PROJECT_PATH/logs/fcgi.error"
cd $PROJECT_PATH
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

ps -ef | grep python | grep $PROJDIR | awk '{print $2}' | xargs kill

source $VENV
echo "python ./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE errlog=$ERROR"
python ./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE errlog=$ERROR

chmod 777 $SOCKET

date -R >> $LOG
```

需要将上面的脚本中 PROJECT_PATH 的值改为Django项目的地址。

执行后，会产生两个文件，其中 SOCKET 文件的路径需要在 Nginx 配置中使用。

以上简略说了 Django 方面的配置，可能会存在一些 Python 包的依赖安装，略过。

Nginx 方面的配置 server 如下：

```nginx
    server {
   		listen 9101;

			server_name  填写你自己的ip或者域名;
  
        default_type 'text/html';
        charset utf-8;

        location / {
            include uwsgi_params;
       	    fastcgi_pass  unix://填写上面的socket文件目录;
      	    fastcgi_param SCRIPT_FILENAME "";
            fastcgi_param PATH_INFO $fastcgi_script_name;
fastcgi_read_timeout 1000;
	    fastcgi_param  SERVER_ADDR        $server_addr;
            fastcgi_param  SERVER_PORT        $server_port;
            fastcgi_param  SERVER_NAME        $server_name;
    fastcgi_param  QUERY_STRING     $query_string;
  fastcgi_param  REQUEST_METHOD   $request_method;
  fastcgi_param  CONTENT_TYPE     $content_type;
  fastcgi_param  CONTENT_LENGTH   $content_length;
        }

        location /static {
             alias /项目静态文件目录/;
        }
    }
```

以上是 nginx 的配置。 nginx 有两种配置方式，在于  fastcgi_pass 值的不同，可以是一个 sock 文件的地址如 `unix:///tmp/pyth-cgi.sock`  ，也可以是一个 `127.0.0.1:8008;` 。不同的地方在于前者不需要Python 程序监听一个端口，是直接通过 Unix 套接字来进行通信的，后者是使用 TCP 套接字进行通信的。但是要注意的是，使用 TCP 套接字一般不会涉及权限问题，而使用 Unix 套接字记得把文件的权限改成 777 才可以，`chmod 777 python-cgi.sock`。




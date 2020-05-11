---
title: uWSGI部署记录
tags: [Python, Web]
category: Python
date: 2018-10-30
---

就不那么多废话了，也不用一点一点来讲为什么了。只是说一说流程。


<!--more -->

## 第一步

安装 uWSGI，建议使用 pip 进行安装。

我是在 ubuntu 上面部署的，其他服务器类似，请先查一下各自版本在安装之前，需要安装什么依赖，比如，出了错，不要一股脑就把他粘上谷歌，然后看的一头雾水，出了问题好好读读报错信息，看看自己是否见过，能否解决，要不然的话，找不到根本问题，那就是问题一个接一个的来。

如果开始没有 gcc 请先安装，好好看看出错信息，缺什么安什么，  uWSGI 并不是一条命令就能搞定的。

```shell
Command "/usr/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-install-wpULhz/uwsgi/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-record-axH1lT/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-install-wpULhz/uwsgi/
```

这个是当时我报的错，由于缺少 gcc 导致的。

[从零开始在 Ubuntu  下部署 Django + uwsgi + nginx](https://www.jianshu.com/p/f1ed50f22d07)

这个已经说得比较清楚了，如果是在 Python2 的环境下，只需要把 3 去掉即可。



## 第二步

uWSGI 安装完之后，试验一下能否运行，一步一步实验，否则最后东西都搭建完成了，跑不起来，还不是需要重头再来检测一下。

```python
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]
```

把下面这个代码新建一个 test.py 复制粘贴保存

然后

```shell
uwsgi --http :8000 --wsgi-file test.py
```

打开浏览器输入服务器的 ip, 端口 8000 如果能看到 hello, world 就表安装 uwsgi 成功了。



## 第三步

然后开始配置 Nginx 。

Nginx 安装不是什么难事。

Nginx 安装完之后，它的配置文件目录，一般都是 /etc/nginx/ 目录下有一个 uwsgi_params 文件，然后把这个文件原封不动的拷贝到你的项目的根目录。

然后新建一个 自定义的 Nginx 配置文件：

```shell
upstream django {
        server 127.0.0.1:8001;
}
server {
        listen      8000; # 端口号
        server_name abc; # 没有就不填，不影响
        charset     utf-8;
  
        # Django media
        location /media  {
            alias /home/yww/djangotest/Hello/media; # 媒体文件所在文件夹
        }

        location /static {
            alias /home/yww/djangotest/Hello/static; # 静态文件所在文件夹
        }
         # max upload size
        client_max_body_size 75M;   # adjust to taste

        # Finally, send all non-media requests to the Django server.
        location / {
            uwsgi_pass  django;
            include     /home/yww/djangotest/Hello/uwsgi_params; #uwsgi_params 路径
        }
}

```

上面的是示例：

下面是我的真实配置：

```shell
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name abc.com; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /apps/beautyblock/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /apps/beautyblock/static; # your Django project's static files - amend as required
    }
    location /resource {
        alias /apps/beautyblock/resource; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /apps/beautyblock/uwsgi_params; # the uwsgi_params file you installed
    }
}
```

其中，本来项目只有两个目录，media 和 static ，但是临时需要加一个目录，提供一些下载的服务，于是乎，我就又加了一条 resource ， 如有需要，请在 Nginx 里面配置好路径对应，然后在 Django 里面配好路由就可以了，还是比较简单的。

这个文件放到 /etc/nginx/site-enabled/xxxx.conf  自己取个名字。（Nginx 主配置已经包含了这个目录，他回自动加载的）

至此，Nginx 可以算是结束了。

！！！！！！注意：

这个时候，你去访问以下，应该会发现，访问的结果是 

**502**  Bad Gateway  

那是因为你上游的服务还没启动，就是项目还没启动。这个时候就该 uWSGI 出场了。

 

## 开始配置 uWSGI

如果遇到一些错误，不要太过于慌张，就觉得是代码写错了。  真的有可能是你在哪个目录下使用 uWSGI 命令的锅呢。  所以，最后，是在项目的根目录来进行 uwsgi 命令，然后再指明 wsgi.py 的路径进行启动，如果你的 wsgi.py 里不是那么单纯，还涉及导自己的包，那就容易出现 xxxx moudle not found 错误。

所以，记住： 在项目根目录来使用 

`uwsgi --http :8000 --wsgi-file wsgi.py`

来进行服务器的启动操作

还有一种 `--socket` 类型：如果跟 nginx 搭配，比较推荐 socket

而使用 `--http` 其实是可以直接当做一个 Web 服务器的。而且 uWSGI 其实就可以看做是 WSGI 的 服务器部分的实现。

开始的时候，可以通过一条命令来开启，然后看看是否可以正常访问，而不是出现 502 的问题。

如果一切没问题，好了，那么我们就可以通过写一个配置文件来方便管理了。

```shell
[uwsgi]
socket=127.0.0.1:8001
chdir=/apps/beautyblock
wsgi-file=ksCMS/wsgi.py
processes=4
threads=2
master=True
pidfile=uwsgi.pid
daemonize=uswgi.log
```

这是我的文件，大家看着改就行，保证 socket 和  nginx 里面的配置一致。

然后，改完之后，重启 Nginx 和 uwsgi  ，否则有可能造成没有效果，又导致不必要的麻烦。

最后说一个，快速停掉 uwsgi ，然后在 开启。 可以 通过 kill -9  pid 来进行全部杀死。

可以通过  uwsgi --ini wsgi.py 来开启 **注意是 两个 “-”**


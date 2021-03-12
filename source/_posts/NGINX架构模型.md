---
title: NGINX架构模型
date: 2018-10-10
tags: [NGINX, Linux]
category: 服务器
---

Nginx 采用 `Master-Worker` 的多进程模型。

Nginx 启动后，Master 进程会去加载配置文件，建立好需要 `Listen` 的 `Socket(Listenfd)` 之后，然后 `Fork` 出多个 `Worker` 进程，`Master` 进程负责管理`Worker` 进程以及接收来自外接的信号，向各个 `Worker` 进程发送信号，监控 `Worker` 进程的运行状态，如有 `Worker` 异常退出，`Master` 进程会重新启动新的 `Worker` 进程。请求的处理是放在 `Worker` 进程中进行。

采用 `Master-Worker` 多进程的模式有诸多好处。

1. 如果程序有 `bug` 导致 `Worker` 异常退出，`Master` 会启动新的 `Worker` 补充上，这样就不会对其他没有异常的服务造成影响，就不至于造成整个服务都无法访问。
2. `Worker` 个数是确定的，一般 `CPU` 有多少核，就设置成多少，这样就不会造成无意义的进程切换及进程竞争开销。

`Nginx`  是采用多路复用I/O模型（严谨点的话不能说是异步非阻塞I/O模型），所以它的并发量会比 `Apache` 高非常多，并且性能更好，更轻量。

`Apache` 中每个请求会独占一个工作线程，当并发数达到几千时，就同时有几千的线程在处理请求了。这对操作系统来说，是个不小的挑战，线程带来的内存占用非常大，线程的上下文切换带来的 `CPU` 开销很大，性能自然就上不去了，而且这些开销完全是没有意义的。阻塞的系统调用会导致 `CPU` 空闲，`CPU` 的利用率就会下降。

> 同步阻塞：线程会阻塞在那里等待返回，并让出 CPU
>
> 非阻塞：线程发现数据还没有可用的，就先直接先去做其他事情，定时自己来检查数据状态
>
> 异步非阻塞：线程发现数据没有可用的，然后把这个监控数据的任务交给操作系统，由操作系统来通知线程数据是否已经准备好。
>
> 有时候经常把异步非阻塞和非阻塞调用搞混，到底算不算异步，取决于进程向内核发起读取数据操作的时候，在内核把数据从内核态复制到用户态的这一时间内，进程是否处于阻塞状态。



`Nginx` 使用的是 `epoll` 模型，可以并发处理大量请求，但是同一时间能处理的请求当然也只有一个，只是在请求间不断地切换而已，切换是因为事件未准备好，而主动让出的。这里的切换是没有任何代价的，这跟 `Apache` 由于阻塞让出 `CPU` 是完全不同的。与多线程相比，`Nginx` 的处理机制有很大的优势，不需要创建线程，每个请求占用的内存也很少，没有上下文切换，不会造成竞争 `CPU`，事件处理也非常的轻量级。并发数再多也不会导致无谓的资源浪费。更多的连接只会造成更多的内存占用，在 1 G 的机器上，可容纳的连接数可达 10 万左右。

> Linux I/O 模型
>
> select、poll、epoll 请看我很早写的另一篇文章：
>
> [Linux I/O 模型之select、poll、epoll](https://anitazhaochen.github.io/2018/09/27/Linux-I-O%E6%A8%A1%E5%9E%8B%E4%B9%8Bselect-poll-epoll/)
>
> 着重讲了什么阻塞、非阻塞、异步、同步 及 select、poll、epoll 解析



## Nginx 如何热部署

当Nginx reload 发生的时候，比如执行 `nginx -s reload `

`Master` 进程收到信号后，会重新加载配置文件，然后向当前的 Worker 发出信号，并且告诉他们把当前手中的任务处理完你们就可以光荣退休了，不要再去竞争新的连接，然后 `Master` 会 `Fork` 出新的 `Worker`，此时新的 `Worker` 就是具备新的配置文件属性，因此就完成了热重启。



## Nginx 负载均衡

Nginx 负载均衡通过配置 `upstream` 模块来实现，内置了三种负载均衡策略。

* s轮询（默认）/ 加权轮询

  轮询：Nginx 根据请求次数，将每次请求均匀分配到每台服务器，如果每台服务器的性能都一样，那么在一定程度上是可以使用这种模式的。

  ```nginx
  http {
  
      # ... 省略其它配置
  
      upstream web1 {
          server 192.168.0.100:8080;
          server 192.168.0.101:8080;
          server example.com:8080;
      }
  
      server {
          listen 80;
  
          location / {
              proxy_pass http://web1;
          }
      }
  
      # ... 省略其它配置
  }
  ```

  加权轮询：如果在 `upstream 中的 server` 参数最后面加上 weight=n ，就变成了加权轮询：

  ```nginx
      upstream web1 {
          server 192.168.1.2:8080 weight=1; # 分担 1/6 的请求
          server 192.168.1.3:8080 weight=2; # 分担 2/6 的请求
          server test.com weight=3;  # 分担 3/6 的请求
      }
  ```

   除了 `weight` 还支持其他的一些参数比如下面这条语句：

  ```nginx
  upstream web1{
    server 192.168.1.2:8080 weight=2 max_fails=3 fail_timeout=15;
    server 192.168.1.10:8080 backup;
  }
  
  ```

  第一条`server` 语句的意思是 `192.168.1.2:8080` 这台服务器的权重是2，如果出现了 3 次请求失败，就等待 15 秒后再请求。

  第二条 `server` 语句的意思是 `192.168.1.10:8080` 这台服务器作为备份机，所有服务器挂了之后才会生效。

  > `backup`: 备份机，所有服务器挂了之后才会生效
  >
  > `max_fails`: 默认为1，某台 Server 允许请求失败的次数，超过最大次数后，在 fail_timeout 时间内，新的请求将不会分配给这台机器。如果设置为0，Nginx 会将这台 Server 置为永久无效状态，然后将请求发送到其他 handler 来处理这次的错误请求。
  >
  > `fail_timeout`: 默认10秒。某台 `Server` 达到 max_fails 次失败请求后，在 `fail_timeout`期间内， `Nginx` 会认为这台 `Server` 暂时不可用，不会将请求分配给它。
  >
  > `max_conns`: 限制分配给某台 Server 当前正在处理的最大连接数量，超过这个数量，将不会分配新的连接给它。默认为0，表示不限制。1.5.9 以后才有这个参数
  >
  > `resolve`:  将 server 指令配置的域名，指定域名解析服务器。需要在 http 模块下配置 resolver 指令，指定域名解析服务。

  ```nginx
  http {
    resolver 192.168.1.20; # dns 服务器地址
    
    upstream web1 {
      server abc.com resolve;
    }
  }
  ```

* 最少连接

  将请求分配给连接数最少的服务器。 `Nginx` 会统计哪些服务器的连接数最少

* IP Hash

  绑定处理请求的服务器。第一次请求时，根据客户端的 `IP` 算出一个 `HASH` 值，将请求分配到集群中的某一台服务器上。后面该客户端的所有请求，都将通过 HASH 算法，找到之前处理这台客户端请求的服务器，然后将请求交给它来处理。

* URL_Hash

  在1.7.2版本之后，加入了 url_hash 策略，按照请求 url 的 hash 结果来分配请求，使每个 url 定向到同一个后端服务器，服务器做缓存时比较有效。

  ```nginx
  upstream web1 {
    server 192.168.1.3:8080;
    server 192.168.1.4:8080;
    hash $request_uri;
    
  }
  ```

  

[Nginx 官方配置参数](http://nginx.org/en/docs/http/ngx_http_upstream_module.html#server)

除了以上三种是官方自带的负载均衡策略，还有第三方的，比较常用的有一下几个

### fair

根据服务器的响应时间来分配请求，响应时间短的优先分配，即负载压力小的优先会分配。

使用第三方模块时，我们需要在编译 `Nginx` 源码时，将其添加到 `Nginx` 模块中，具体方法可以查看第三方模块 README。

[nginx-upstream-fair Github地址](https://github.com/gnosek/nginx-upstream-fair)



## Nginx 正向代理和反向代理的区别

### 正向代理

请求到 Nginx 后， Nginx 帮你去请求你的目标地址，目标地址把请求响应发送给 Nginx，Nginx 再重新组装包返回给客户端。这样可以隐藏客户端的IP地址。

### 反向代理

请求到 Nginx 后， Nginx 将请求分发给后端服务器进行处理，后端服务器再将响应返回给Nginx，再由 Nginx 将响应做一些修改后，返回给客户端。在这个过程中， 后端真实服务器地址对客户端是不可见的。
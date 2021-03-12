---
title: Linux I/O 模型之 select、poll、epoll
date: 2018-09-27
tags: [Linux, I/O模型, select, poll, epoll]
category: Linux
---

很多概念就是在不断讨论中，不断查询中，不断修正。

## 先说几个概念

* 用户空间和内核空间

  * 现在操作系统都是采用虚拟存储器，那么对32位操作系统而言，它的寻址空间（虚拟存储空间）为 4GB（2的32次方）。操作系统的核心是内核，独立于普通的应用程序，可以访问受保护的内存空间，也有访问底层硬件设备的所有权限。为了保证用户进程不能直接操作内核（kernel），保证内核的安全，操心系统将虚拟空间划分为两部分，一部分为内核空间，一部分为用户空间。针对 Linux 操作系统而言，将最高的 1GB 字节（从虚拟地址 0xC0000000 到 0xFFFFFFFF ），供内核使用，称为内核空间，而将较低的 3GB 字节（从虚拟地址 0x00000000 到0xBFFFFFFF ），供各个进程使用，称为用户空间。

    每个进程的 4GB 进程空间中，最高 1GB 都是一样的，即内核空间。只有剩余的 3GB 才归进程自己使用。

    换句话说就是、最高 1GB 的内核空间是被所有进程共享的！

    如图：

    ![image-20180930133015993](/images/image-20180930133015993.png)

  详情请参考： [Linux 内核空间与用户空间](https://www.cnblogs.com/sparkdev/p/8410350.html)

<!-- more -->

* 进程阻塞 

  正在执行的进程，由于期待的某些事件未发生，如请求系统资源失败、等待某种操作的完成、新数据尚未到达或无新工作做等，则由系统自动执行阻塞原语(Block)，使自己由运行状态变为阻塞状态。可见，进程的阻塞是进程自身的一种主动行为，也因此只有处于运行态的进程（获得CPU），才可能将其转为阻塞状态。`当进程进入阻塞状态，是不占用CPU资源的`。

* 文件描述符fd (File descriptor)

  [文件描述符](https://anitazhaochen.github.io/2018/09/20/%E6%96%87%E4%BB%B6%E6%8F%8F%E8%BF%B0%E7%AC%A6%E6%98%AF%E4%BB%80%E4%B9%88/)

* 阻塞 `I/O (Blocking I/O)`

  在 Linux 中，默认情况下所有的 Socket 都是 Blocking ，如图：

  ![image-20180930130714002](/images/image-20180930130714002.png)

  当用户进程调用了 `recvfrom` 这个系统调用，`Kernel` 就开始了 `I/O` 的第一个阶段：准备数据（对于网络 `I/O` 来说，很多时候数据在一开始并没有到达。比如，还没有收到一个完整的 UDP 包。这个时候 `Kernel` 就要等待足够的数据到来）。这个过程需要等待，也就是说数据被拷贝到操作系统内核的缓冲区中是需要一个过程的。而在用户进程这边，整个进程会被阻塞（当然，是进程自己选择的阻塞）。当 `Kernel` 一直等到数据准备好了，它就会将数据从 `Kernel` 中拷贝到用户内存，然后 `Kernel` 返回结果，用户进程才解除 `Blocking` 状态，并重新运行起来。

* 非阻塞 `I/O` （Non-Blocking I/O）

  在 `Linux` 下，可以通过设置 Socket 的参数使其变为 `Non-Blocking I/O`。当对一个 `Non-Blocking Socket` 执行读操作时：

  如图：

  ![image-20180930130839360](/images/image-20180930130839360.png)

  当用户进程发出 `Read` 操作时，如果 `Kernel` 中的数据还没有准备好，那么它并不会 阻塞用户进程，而是立刻返回一个 `Error`。从用户进程角度讲 ，它发起一个 `Read` 操作后，并不需要等待，而是马上就得到了一个结果。用户进程判断结果是一个 `Error` 时，它就知道数据还没有准备好，于是它可以随时再次发送 `Read` 操作。一旦`Kernel` 中的数据准备好了，并且又再次收到了用户进程的 `Read` 操作，那么它马上就将数据拷贝到了用户内存，然后返回。

  > 所以，Non-Blocking IO 的特点是用户进程需要**不断的主动询问** Kernel 数据准备好了没有。

* `I/O` 多路复用 （I/O multiplexing）

  `I/O multiplexing` 就是我们说的 `select、poll、epoll` ，有些地方也称这种`I/O` 方式为`Event driven I/O (事件驱动I/O)`。`select、poll、epoll` 的优势就在于单个`进程/线程` 就可以同时处理多个网络连接的 `I/O`。它的基本原理就是`select、poll、epoll` 对应的 `function` 会不断地轮询所负责的所有 Socket，当某个 Socket 有数据到达了，就通知用户进程。

  ![image-20180930130903960](/images/image-20180930130903960.png)

  `当用户进程调用了 select，那么整个进程会被 block`，而同时，kernel 会“监视”所有 select 负责的 socket，当任何一个 socket 中的数据准备好了，select 就会返回。这个时候用户进程再调用 read 操作，将数据从 `Kernel` 拷贝到用户进程。

  > 所以，I/O 多路复用的特点是通过一种机制一个进程能同时等待多个文件描述符，而这些文件描述符（套接字描述符）其中的任意一个进入读就绪状态，select() 函数就可以返回。

* 异步 I/O (Asynchronous I/O 简称 AIO)

  linux下的 Asynchronous I/O 其实用得很少。先看一下它的流程：

  ![image-20180930130941633](/images/image-20180930130941633.png)

用户进程发起 **read** 操作之后，立刻就可以开始去做其它的事。而另一方面，从 `Kernel` 的角度，当它收到一个 Asynchronous read 之后，首先它会立刻返回，所以不会对用户进程产生任何 Block。然后，Kernel 会等待数据准备完成，然后将数据拷贝到用户内存，当这一切都完成之后，Kernel 会给用户进程发送一个 signal，告诉它 `Read` 操作完成了。

## 总结

`Synchronous IO(同步I/O)` 和 `Asynchronous IO(异步I/O)` 的区别，先看下两者的定义。`POSIX` 的定义如下：

> A synchronous I/O operation causes the requesting process to be blocked until that I/O operation completes;
>
> An asynchronous I/O operation does not cause the requesting process to be blocked;

两者的区别就在于 `Synchronous I/O` 做 `I/O Operation` 的时候会将 `Process` 阻塞。

按照这个定义，之前所述的 `Blocking I/O、Non-blocking I/O、I/O Multiplexing ` 都属于 `Synchronous I/O`。

我一开是也认为，`Non-Blocking I/O` 并没有 `Block` 进程呀。这里有个误区，定义中所指的 `I/O Operation` 是指真实的`I/O`操作，就是例子中的 `Recvfrom` 这个 `System call(系统调用)`。`Non-Blocking I/O` 在执行 `Recvfrom` 这个`System call`的时候，如果 `Kernel` 的数据没有准备好，这时候不会 `Block` 进程。但是，当 `Kernel` 中数据准备好的时候，`Recvfrom` 会将数据从 `Kernel` 拷贝到用户内存中，在这段时间内进程是处于 `Blocking` 状态。

而 `Asynchronous I/O` 则不一样，当进程发起`I/O Operation` 之后，就直接被返回，然后进程就再也不理睬了，直到 `Kernel` 主动发送一个信号，告诉进程说 `I\O` 完成。在这整个过程中，进程完全没有被 Block。

**各个 I/O 模型的比较如图所示：**

通过上面的图片，可以发现 `Non-Blocking IO(非阻塞I/O)`和 `Asynchronous IO(异步 I/O)` 的区别还是很明显的。在 `Non-blocking I/O(非阻塞 I/O)`中，虽然进程大部分时间都不会被 `Block`，但是它仍然要求进程去主动的 `Check`，并且当数据准备完成以后，也需要进程主动的再次调用 `Recvfrom` 来将数据从内核空间拷贝到用户空间。而 `Asynchronous I/O(异步 I/O)` 则完全不同。它就像是用户进程将整个`I/O操作` 交给了其他人（Kernel）去完成，然后那个人做完后发信号通知就行。在此期间，用户进程不需要去检查`I\O操作` 的状态，也不需要主动的去拷贝数据。

## 异步 I/O

为什么要采用 `异步 I/O` ，想象这样一个场景，浏览器向服务器请求一个资源，如果采用同步的方式，那么

```
同步方式：
// 消耗时间M
get image1
// 消耗时间N
get image2
// 获取完 image1 和 image2 所花时间为 M+N

异步方式：
// 消耗时间M
get image1
// 消耗时间N
get image2
// 获取完 image1 和 image2  所花时间为 max(M, N) 即M和N中间的较大值

备注：暂不考虑 http 协议及网络的问题。

```

如果网站资源很多，现在已经很常见，同步方式所花费的时间将是 A+B+C+....+....Z  而异步所花的时间取决于其中加载最慢的那一个资源。

* 不同 `I/O` 类型及其对 CPU 花费时间的开销

|  I/O 类型   | 花费的 CPU 时钟周期 |
| :---------: | :-----------------: |
| CUP一级缓存 |          3          |
| CPU二级缓存 |         14          |
|    内存     |         250         |
|    硬盘     |      41000000       |
|    网络     |      240000000      |

从此图可以看出 `磁盘I/O 及 网络I/O` 是非常耗时的。

如果要完成一组互不相关的任务，比如读取每一张图片：**单线程串行依次执行** 或者**多线程并行** 去完成。

要选择以上哪种方式，取决于开销大小。 多线程的代价在于**创建线程**和**执行期线程上下文切换**的开销较大。在某些复杂的场景下，多线程会存在资源竞争，状态同步(锁)的问题。

## 阻塞 I/O 操作系统

操作系统内核对于 `I/O` 只有两种方式：阻塞与非阻塞。在调用 `阻塞 I/O` 时， 应用程序需要等待 `I/O` 完成后才返回结果。在此期间，此线程必须等到操作系统内核层面完成所有操作之后，调用才结束，才可以继续向后执行程序。

`阻塞 I/O` 造成的 CPU 等待 I/O ，浪费等待时间， CPU 的处理能力不能得到充分利用。为了提高性能， 内核提供了`非阻塞 I/O`。

`非阻塞 I/O` 调用之后会立即返回，这个立即返回到底什么意思呢，就是接下来 I/O 的事情就交给操作系统去做了，我们可以继续向后执行程序，当 `I/O` 准备好后，操作系统就会通知我们，我们就可以不需要等待直接去获取结果，这样性能提升是明显的。

接下来我们来看看操作系统是如何实现。



## 操作系统非阻塞 I/O 的实现

Linux 操作系统对计算机进行了抽象，所有设备都抽象为文件。内核在进行文件 `I/O` 操作时，通过 `文件描述符(fd)` 进行管理，而 `文件描述符`(fd)  类似于应用程序与系统内核之间的凭证。应用程序如果要进行 `I/O 调用` ，需要先打开 `文件描述符`，然后再根据 `文件描述符` 去实现文件的数据读写。此处 `非阻塞 I/O` 与`阻塞 I/O`  的区别在于 `阻塞 I/O` 完成整个获取数据的过程，而 `非阻塞 I/O` 则直接返回空数据，进程真正获取数据的时候，还需要通过 `文件描述符` 再次读取。

为了获取有效完整的数据，`进程` 需要重复调用 `I/O 操作` 来确认是否完成。这种重复调用判断操作是否完成的技术叫轮询。`阻塞 I/O` 造成 `CPU 等待浪费`，`非阻塞 I/O`带来` CPU 循环判断`，是对 CPU 的资源浪费。



### select 

通过文件描述符上的事件状态来进行判断。

select 轮询具有一个较弱的限制，那就是由于它采用一个 1024 长度的数组来存储状态，所以它最多可以同时检查 1024 个文件描述符。

下面，我们将深入对为何是 1024 进行讨论。

​	FD_SETSIZE 限制了文件描述符个数，但是根据 fd_set 存储文件描述符的原理， FD_SeTSIZE 限制的应该是文件描述符的最大值，因而限制了最大值也就是最大个数。因为文件描述符总是从当前可用的最小数开始分配。

下面通过图来解决问题：

 [ Linux 源码的网站](https://elixir.bootlin.com/linux/v4.18.10/ident)

![image-20180929172251721](/images/image-20180929172251721.png)

打开后，从右边的搜索，搜索 字段  __FD_SETSIZE

![image-20180929172345317](/images/image-20180929172345317.png)可以看到在这些文件里出现过，点进去，我们可以看到：

![image-20180929172418410](/images/image-20180929172418410.png)

通过宏定义，定了了它的值为 1024 ， 所以 Select 最大只能同时观测 1024 个文件描述符。

如果要对它做一些修改，则需要重新编译内核来实现。

select 使用的是定长数组，而 poll 是通过用户自定义数组长度的形式 （polldf[] ）

select 只支持 fd<1024， 如果单个进程的文件句柄数超过1024， select 就不能用了。 poll 在接口上无限制，考虑到每次都要拷贝到内核。

我当时很不理解到底是什么因素导致了不同，而最终只有看源码才知道他们所说的不同是体现在哪里。

首先 select 和 poll 的区别： 因为内核直接把 1024 限制写进去了，所以说我们说 select 只支持 1024 个文件描述符，如果需要更改，是需要重新编译内核的。 而 poll 为什么无限制呢？ 因为 内核没有限制，就好比，对于 `select` 操作系统直接让内核给我们申请 1024 个空间 ， 而 `poll` 是可以交给开发者通过参数来指定，需要多少个空间。

```c
// select 定义函数，第一个 n 的含义是当前监听的描述符最大值加1的值传进去，并不是传进去一个监听的描述符上限值，如果传的值大于1024，那么会有一些错误发生。
int select (int n, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);

```

`select` 函数监视的文件描述符分3类，分别是 `writefds、readfds、exceptfds`。调用后 `select` 函数会阻塞，直到有 `文件描述符` 就绪（有数据 可读、可写、或者有异常），或者超时（timeout 指定等待时间，如果需要立即返回，设为 `null` 即可），函数返回。当 `select` 函数返回后，可以通过遍历 `fdset`，来找到就绪的描述符。

`select` 目前几乎在所有的平台上都支持，其良好跨平台支持也是它的一个优点。`select` 的一个缺点在于单个进程能够监视的文件描述符的数量存在最大限制，在 `Linux` 上一般为`1024`，可以通过修改宏定义甚至重新编译内核的方式提升这一限制，但是这样可能会造成效率的降低。

如果还不是很明白，我们可以写一个基于 select 实现的服务器：

```c
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<netinet/in.h>
#include<sys/time.h>
#include<unistd.h>
#include<assert.h>
#define _SIZE_ 128
int makesock(const char* ip,const char* port)
{
    assert(ip);
    assert(port);
    int listensock = socket(AF_INET,SOCK_STREAM,0);
    if(listensock < 0)
    {
        perror("socket");
        return 2;
    }
    
    int opt = 1;
    int retset = setsockopt(listensock,SOL_SOCKET,SO_REUSEADDR,&opt,sizeof(opt));
    if(retset < 0)
    {
        perror("setsockopt");
        return 3;
    }
    
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(atoi(port));
    addr.sin_addr.s_addr = inet_addr(ip);
    
    if(bind(listensock,(struct sockaddr*)&addr,sizeof(addr)) < 0)
    {
        perror("bind");
        return 4;
    }
    
    if(listen(listensock,5) < 0)
    {
        perror("listen");
        return 5;
    }
    
    
    return listensock;
}


int main(int argc,char* argv[])
{
    
    
	//printf("%d",sizeof(fd_set));
    
    if(argc < 3)
    {
        printf("Please input:%s [ip] [port]\n",argv[0]);
        return 1;
    }
    int listensock = makesock(argv[1],argv[2]);
    int gfds[_SIZE_];
    int i = 0;
    for(i = 0;i < _SIZE_;i++)
    {
        gfds[i] = -1;
    }
    gfds[0] = listensock;
    
    int max_fd = gfds[0];
    while(1)
    {
		printf("主循环\n");
        fd_set rfds;
        FD_ZERO(&rfds);
        int j = 0;
        for(;j < _SIZE_;j++)
        {
            if(gfds[j] != -1)
            {
                FD_SET(gfds[j],&rfds);
            }
            if(max_fd < gfds[j])
            {
                max_fd = gfds[j];
            }
        }
        
        struct timeval timeout = {5,0};
        
		printf("switch外面\n");
        switch(select(max_fd+1,&rfds,NULL,NULL,NULL))
        {
            case -1://error
                perror("select");
                break;
            case 0://timeout
                printf("...timeout\n");
                break;
            default:{
				printf("default\n");
                int k = 0;
                for(;k < _SIZE_;k++){
                    if(gfds[k] != -1 && FD_ISSET(gfds[k],&rfds)){
                        if(gfds[k] == listensock){
                            struct sockaddr_in peer;
                            int len = 0;
                            memset(&peer,'\0',sizeof(peer));
                            int sock = accept(listensock,(struct sockaddr*)&peer,&len);
                            if(sock < 0){
                                perror("accept");
                                continue;
                            }
                            printf("%s:%d(%d)",inet_ntoa(peer.sin_addr),ntohs(peer.sin_port),sock);
                            int m = 0;
                            for(;m < _SIZE_;m++)
                            {
                                if(gfds[m] == -1)
                                {
									printf("执行了这里 ，并且 m=%d",m);
									printf("接受成功，并且设置到 Select");
                                    gfds[m] = sock;
                                    break;
                                }
                            }
                            
                            if(m == _SIZE_)
                            {
                                printf("gfds have no space!\n");
                                continue;
                            }
                        }
                    	else
                    	{
                            char buf[1024];
                            ssize_t s = read(gfds[k],buf,sizeof(buf));
                            if(s < 0)
                            {
                                perror("read");
                                continue;
                            }
                            else if(s == 0)
                            {
                                printf("client is quit!\n");
                                close(gfds[k]);
                                gfds[k] = -1;
                                continue;
                            }
                            else
                            {
                                buf[s] = '\0';
                                printf("读取完毕  client say# %s\n",buf);
                            }
                    }
                    }
                    
                }
                break;
            }
                
        }
        
    }
    //close(listensock);
    
    return 0;
    
}




```

大家可以在 `Linux`上面 直接 gcc  xxx.c 编译 ，然后 ./a.out ip port  运行 通过 printf  函数来观察函数执行过程。

并且 另开一个窗口 使用 curl 127.0.0.1:port  进行请求。

### poll



```c
int poll (struct pollfd *fds, unsigned int nfds, int timeout);
```

select 使用三个位图来表示读取和错误，而 poll 使用一个 pollfd 的指针来实现。

```c
struct pollfd {
    int fd; /* file descriptor */
    short events; /* requested events to watch */
    short revents; /* returned events witnessed */
};
```



pollf 结构体包含了要监视的 event 不再使用类似 select 参数-值传递的方式。同时，`pollfd`并没有最大数量限制（但是数量过大后性能也是会下降）。 和 `select` 函数一样，` poll` 返回后，需要轮询 pollfd 来获取就绪的描述符。



> 从上面看，select和poll都需要在返回后，`通过遍历文件描述符来获取已经就绪的socket`。事实上，同时连接的大量客户端在一时刻可能只有很少的处于就绪状态，因此随着监视的描述符数量的增长，其效率也会线性下降。



### epoll



`epoll` 是在`Linux 2.6 `内核版本中提出的，是 `select` 和`poll` 的增强版本。相对于 `select、poll` 来说，`epoll` 更加灵活，和 `poll` 同样没有描述符限制, 但是会比 poll 更高效。`epoll` 使用一个 `文件描述符` 管理 `多个文件描述符`，将用户关心的 `文件描述符` 的事件存放到内核的一个事件表中，这样在用户空间和内核空间的Copy 只需一次。



### epoll操作过程

epoll操作过程需要三个接口，分别如下：

```
int epoll_create(int size)；//创建一个epoll的句柄，size用来告诉内核这个监听的数目一共有多大
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)；
int epoll_wait(int epfd, struct epoll_event * events, int maxevents, int timeout);
```

**1. int epoll_create(int size);**
创建一个epoll的句柄，size用来告诉内核这个监听的数目一共有多大，这个参数不同于select()中的第一个参数，给出最大监听的fd+1的值，`参数size并不是限制了epoll所能监听的描述符最大个数，只是对内核初始分配内部数据结构的一个建议`。
当创建好epoll句柄后，它就会占用一个fd值，在linux下如果查看/proc/进程id/fd/，是能够看到这个fd的，所以在使用完epoll后，必须调用close()关闭，否则可能导致fd被耗尽。

2. int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)；
函数是对指定描述符fd执行op操作。
- epfd：是epoll_create()的返回值。
- op：表示op操作，用三个宏来表示：添加EPOLL_CTL_ADD，删除EPOLL_CTL_DEL，修改EPOLL_CTL_MOD。分别添加、删除和修改对fd的监听事件。
- fd：是需要监听的fd（文件描述符）
- epoll_event：是告诉内核需要监听什么事，struct epoll_event结构如下：

```
struct epoll_event {
  __uint32_t events;  /* Epoll events */
  epoll_data_t data;  /* User data variable */
};

//events可以是以下几个宏的集合：
EPOLLIN ：表示对应的文件描述符可以读（包括对端SOCKET正常关闭）；
EPOLLOUT：表示对应的文件描述符可以写；
EPOLLPRI：表示对应的文件描述符有紧急的数据可读（这里应该表示有带外数据到来）；
EPOLLERR：表示对应的文件描述符发生错误；
EPOLLHUP：表示对应的文件描述符被挂断；
EPOLLET： 将EPOLL设为边缘触发(Edge Triggered)模式，这是相对于水平触发(Level Triggered)来说的。
EPOLLONESHOT：只监听一次事件，当监听完这次事件之后，如果还需要继续监听这个socket的话，需要再次把这个socket加入到EPOLL队列里
```

**3. int epoll_wait(int epfd, struct epoll_event \* events, int maxevents, int timeout);**
等待epfd上的io事件，最多返回maxevents个事件。
参数events用来从内核得到事件的集合，maxevents告之内核这个events有多大，这个maxevents的值不能大于创建epoll_create()时的size，参数timeout是超时时间（毫秒，0会立即返回，-1将不确定，也有说法说是永久阻塞）。该函数返回需要处理的事件数目，如返回0表示已超时。

### 工作模式

　epoll对文件描述符的操作有两种模式：**LT（level trigger）**和**ET（edge trigger）**。LT模式是默认模式，LT模式与ET模式的区别如下：
　　**LT模式**：当epoll_wait检测到描述符事件发生并将此事件通知应用程序，`应用程序可以不立即处理该事件`。下次调用epoll_wait时，会再次响应应用程序并通知此事件。
　　**ET模式**：当epoll_wait检测到描述符事件发生并将此事件通知应用程序，`应用程序必须立即处理该事件`。如果不处理，下次调用epoll_wait时，不会再次响应应用程序并通知此事件。

#### 1. LT模式

LT(level triggered)是缺省的工作方式，并且同时支持block和no-block socket.在这种做法中，内核告诉你一个文件描述符是否就绪了，然后你可以对这个就绪的fd进行IO操作。如果你不作任何操作，内核还是会继续通知你的。

#### 2. ET模式

ET(edge-triggered)是高速工作方式，只支持no-block socket。在这种模式下，当描述符从未就绪变为就绪时，内核通过epoll告诉你。然后它会假设你知道文件描述符已经就绪，并且不会再为那个文件描述符发送更多的就绪通知，直到你做了某些操作导致那个文件描述符不再为就绪状态了(比如，你在发送，接收或者接收请求，或者发送接收的数据少于一定量时导致了一个EWOULDBLOCK 错误）。但是请注意，如果一直不对这个fd作IO操作(从而导致它再次变成未就绪)，内核不会发送更多的通知(only once)

ET模式在很大程度上减少了epoll事件被重复触发的次数，因此效率要比LT模式高。epoll工作在ET模式的时候，必须使用非阻塞套接口，以避免由于一个文件句柄的阻塞读/阻塞写操作把处理多个文件描述符的任务饿死。

#### 3. 总结

假如有这样一个例子：
1. 我们已经把一个用来从管道中读取数据的文件句柄(RFD)添加到epoll描述符
2. 这个时候从管道的另一端被写入了2KB的数据
3. 调用epoll_wait(2)，并且它会返回RFD，说明它已经准备好读取操作
4. 然后我们读取了1KB的数据
5. 调用epoll_wait(2)......

**LT模式：**
如果是LT模式，那么在第5步调用epoll_wait(2)之后，仍然能受到通知。

**ET模式：**
如果我们在第1步将RFD添加到epoll描述符的时候使用了EPOLLET标志，那么在第5步调用epoll_wait(2)之后将有可能会挂起，因为剩余的数据还存在于文件的输入缓冲区内，而且数据发出端还在等待一个针对已经发出数据的反馈信息。只有在监视的文件句柄上发生了某个事件的时候 ET 工作模式才会汇报事件。因此在第5步的时候，调用者可能会放弃等待仍在存在于文件输入缓冲区内的剩余数据。

当使用epoll的ET模型来工作时，当产生了一个EPOLLIN事件后，
读数据的时候需要考虑的是当recv()返回的大小如果等于请求的大小，那么很有可能是缓冲区还有数据未读完，也意味着该次事件还没有处理完，所以还需要再次读取：

```c
while(rs){
  buflen = recv(activeevents[i].data.fd, buf, sizeof(buf), 0);
  if(buflen < 0){
    // 由于是非阻塞的模式,所以当errno为EAGAIN时,表示当前缓冲区已无数据可读
    // 在这里就当作是该次事件已处理处.
    if(errno == EAGAIN){
        break;
    }
    else{
        return;
    }
  }
  else if(buflen == 0){
     // 这里表示对端的socket已正常关闭.
  }

 if(buflen == sizeof(buf){
      rs = 1;   // 需要再次读取
 }
 else{
      rs = 0;
 }
}
```

> **Linux中的EAGAIN含义**

Linux环境下开发经常会碰到很多错误(设置errno)，其中EAGAIN是其中比较常见的一个错误(比如用在非阻塞操作中)。
从字面上来看，是提示再试一次。这个错误经常出现在当应用程序进行一些非阻塞(non-blocking)操作(对文件或socket)的时候。

例如，以 O_NONBLOCK的标志打开文件/socket/FIFO，如果你连续做read操作而没有数据可读。此时程序不会阻塞起来等待数据准备就绪返回，read函数会返回一个错误EAGAIN，提示你的应用程序现在没有数据可读请稍后再试。
又例如，当一个系统调用(比如fork)因为没有足够的资源(比如虚拟内存)而执行失败，返回EAGAIN提示其再调用一次(也许下次就能成功)。

### 三 代码演示

下面是一段不完整的代码且格式不对，意在表述上面的过程，去掉了一些模板代码。

```c
#define IPADDRESS   "127.0.0.1"
#define PORT        8787
#define MAXSIZE     1024
#define LISTENQ     5
#define FDSIZE      1000
#define EPOLLEVENTS 100

listenfd = socket_bind(IPADDRESS,PORT);

struct epoll_event events[EPOLLEVENTS];

//创建一个描述符
epollfd = epoll_create(FDSIZE);

//添加监听描述符事件
add_event(epollfd,listenfd,EPOLLIN);

//循环等待
for ( ; ; ){
    //该函数返回已经准备好的描述符事件数目
    ret = epoll_wait(epollfd,events,EPOLLEVENTS,-1);
    //处理接收到的连接
    handle_events(epollfd,events,ret,listenfd,buf);
}

//事件处理函数
static void handle_events(int epollfd,struct epoll_event *events,int num,int listenfd,char *buf)
{
     int i;
     int fd;
     //进行遍历;这里只要遍历已经准备好的io事件。num并不是当初epoll_create时的FDSIZE。
     for (i = 0;i < num;i++)
     {
         fd = events[i].data.fd;
        //根据描述符的类型和事件类型进行处理
         if ((fd == listenfd) &&(events[i].events & EPOLLIN))
            handle_accpet(epollfd,listenfd);
         else if (events[i].events & EPOLLIN)
            do_read(epollfd,fd,buf);
         else if (events[i].events & EPOLLOUT)
            do_write(epollfd,fd,buf);
     }
}

//添加事件
static void add_event(int epollfd,int fd,int state){
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epollfd,EPOLL_CTL_ADD,fd,&ev);
}

//处理接收到的连接
static void handle_accpet(int epollfd,int listenfd){
     int clifd;     
     struct sockaddr_in cliaddr;     
     socklen_t  cliaddrlen;     
     clifd = accept(listenfd,(struct sockaddr*)&cliaddr,&cliaddrlen);     
     if (clifd == -1)         
     perror("accpet error:");     
     else {         
         printf("accept a new client: %s:%d\n",inet_ntoa(cliaddr.sin_addr),cliaddr.sin_port);                       //添加一个客户描述符和事件         
         add_event(epollfd,clifd,EPOLLIN);     
     } 
}

//读处理
static void do_read(int epollfd,int fd,char *buf){
    int nread;
    nread = read(fd,buf,MAXSIZE);
    if (nread == -1)     {         
        perror("read error:");         
        close(fd); //记住close fd        
        delete_event(epollfd,fd,EPOLLIN); //删除监听 
    }
    else if (nread == 0)     {         
        fprintf(stderr,"client close.\n");
        close(fd); //记住close fd       
        delete_event(epollfd,fd,EPOLLIN); //删除监听 
    }     
    else {         
        printf("read message is : %s",buf);        
        //修改描述符对应的事件，由读改为写         
        modify_event(epollfd,fd,EPOLLOUT);     
    } 
}

//写处理
static void do_write(int epollfd,int fd,char *buf) {     
    int nwrite;     
    nwrite = write(fd,buf,strlen(buf));     
    if (nwrite == -1){         
        perror("write error:");        
        close(fd);   //记住close fd       
        delete_event(epollfd,fd,EPOLLOUT);  //删除监听    
    }else{
        modify_event(epollfd,fd,EPOLLIN); 
    }    
    memset(buf,0,MAXSIZE); 
}

//删除事件
static void delete_event(int epollfd,int fd,int state) {
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epollfd,EPOLL_CTL_DEL,fd,&ev);
}

//修改事件
static void modify_event(int epollfd,int fd,int state){     
    struct epoll_event ev;
    ev.events = state;
    ev.data.fd = fd;
    epoll_ctl(epollfd,EPOLL_CTL_MOD,fd,&ev);
}

//注：另外一端我就省了
```

### 四 epoll总结

在 select/poll中，进程只有在调用一定的方法后，内核才对所有监视的文件描述符进行扫描，而**epoll事先通过epoll_ctl()来注册一 个文件描述符，一旦基于某个文件描述符就绪时，内核会采用类似callback的回调机制，迅速激活这个文件描述符，当进程调用epoll_wait() 时便得到通知**。(`此处去掉了遍历文件描述符，而是通过监听回调的的机制`。这正是epoll的魅力所在。)

**epoll的优点主要是一下几个方面：**

1. 监视的描述符数量不受限制，它所支持的FD上限是最大可以打开文件的数目，这个数字一般远大于2048,举个例子,在1GB内存的机器上大约是10万左 右，具体数目可以cat /proc/sys/fs/file-max察看,一般来说这个数目和系统内存关系很大。select的最大缺点就是进程打开的fd是有数量限制的。这对 于连接数量比较大的服务器来说根本不能满足。虽然也可以选择多进程的解决方案( Apache就是这样实现的)，不过虽然linux上面创建进程的代价比较小，但仍旧是不可忽视的，加上进程间数据同步远比不上线程间同步的高效，所以也不是一种完美的方案。
2. IO的效率不会随着监视fd的数量的增长而下降。epoll不同于select和poll轮询的方式，而是通过每个fd定义的回调函数来实现的。只有就绪的fd才会执行回调函数。

> 如果没有大量的idle -connection或者dead-connection，epoll的效率并不会比select/poll高很多，但是当遇到大量的idle- connection，就会发现epoll的效率大大高于select/poll。



[参考](https://segmentfault.com/a/1190000003063859)

[select 和 poll 的区别](https://zhuanlan.zhihu.com/p/26441158)

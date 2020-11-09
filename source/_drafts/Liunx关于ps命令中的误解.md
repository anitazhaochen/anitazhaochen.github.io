---
title: Liunx关于ps命令中的误解
date: 2020-11-06 11:57:29
tags: [Linux, ps]
category: Liunx
---

在使用 ps 命令中，个人偏好使用 ps aux 来进行查询，在一次工作中，想获取一下某个进程的全部启动命令及参数，发现只有命令不带参数，于是想去寻找他的父进程，明明记得 ps 是可以查找父进程的，但是执行了好几次，又拿到ps aux 显示的信息一列一列看，都没有发现父进程。然后又试了下 pstree 也发现什么都没显示，忽然觉得这个进程是不是没有父进程，一度陷入尴尬的局面。

然后跟同事说出了疑惑后，发现他可以找到父进程，我照着他给发的命令执行了一遍，第三列不就是父进程id嘛，奈何我的终端字太小，而且这进程id又极其相似，搞得我差点以为这俩id 是相同的。

我执行的命令是 `ps aux`

同事执行的命令是 `ps -ef`

找到父进程后，立即去查看这两种命令的区别。

Linux 下显示系统进程，有两种风格比较常用，一种是 `ps -ef` 另外一种是 `ps aux`。这两种风格是 Unix 系统中的两种不同风格，一种 System V （ps -ef）风格 一种 BSD （ps aux）风格。这个其实不重要，重要的是需要查看什么信息就用哪种风格，因为这两种风格显示的信息是不同的。

* ps -ef 显示如下信息：

```
➜  ~ ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 Oct28 ?        00:00:18 /sbin/init
root         2     0  0 Oct28 ?        00:00:00 [kthreadd]
root         3     2  0 Oct28 ?        00:00:00 [rcu_gp]
root         4     2  0 Oct28 ?        00:00:00 [rcu_par_gp]
root         8     2  0 Oct28 ?        00:00:00 [mm_percpu_wq
root         9     2  0 Oct28 ?        00:06:37 [ksoftirqd/0]
root        10     2  0 Oct28 ?        00:05:08 [rcu_sched]
root        11     2  0 Oct28 ?        00:00:00 [migration/0]
root        12     2  0 Oct28 ?        00:00:00 [cpuhp/0]
root        13     2  0 Oct28 ?        00:00:00 [cpuhp/1]
root        14     2  0 Oct28 ?        00:00:00 [migration/1]
root        15     2  0 Oct28 ?        00:07:47 [ksoftirqd/1]
root        18     2  0 Oct28 ?        00:00:00 [cpuhp/2]
```

从第一列开始分别是： 

UID： 用户id（实则用户名）、

PID： 进程id

PPID：父进程id

C：进程占用 CPU 的百分比

STIME：进程启动到现在的时间、

TTY：该进程是在哪个终端运行，若与终端无关，则显"?"，若`pts/0` 等，则表示由网络连接主机进程

TIME：进程实际使用 CPU 的时间

CMD ：命令的名称和参数（可能子进程显示不全，需要到父进程查看）

* ps aux 显示如下信息：

```shell
➜  ~ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.2  34952  8424 ?        Ss   Oct28   0:18 /sbin/init
root         2  0.0  0.0      0     0 ?        S    Oct28   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        I<   Oct28   0:00 [rcu_gp]
root         4  0.0  0.0      0     0 ?        I<   Oct28   0:00 [rcu_par_gp]
root         8  0.0  0.0      0     0 ?        I<   Oct28   0:00 [mm_percpu_wq]
root         9  0.0  0.0      0     0 ?        S    Oct28   6:37 [ksoftirqd/0]
root        10  0.0  0.0      0     0 ?        I    Oct28   5:08 [rcu_sched]
root        11  0.0  0.0      0     0 ?        S    Oct28   0:00 [migration/0]
root        12  0.0  0.0      0     0 ?        S    Oct28   0:00 [cpuhp/0]
root        13  0.0  0.0      0     0 ?        S    Oct28   0:00 [cpuhp/1]
root        14  0.0  0.0      0     0 ?        S    Oct28   0:00 [migration/1]
root        15  0.0  0.0      0     0 ?        S    Oct28   7:47 [ksoftirqd/1]
```

从第一列开始分别是：

USER：用户名

PID： 进程ID

%CPU：进程占用CPU的百分比

%MEM：进程占用内存的百分比

VSZ：进程使用的虚拟内存量（单位KB）

RSS：进程占用的固定内存量（单位KB，驻留中页的数量）

TTY： 同上ps -ef

STAT：进程的状态

​		D： 不可中断的休眠状态（通过为 IO 的进程）

​		R：正在运行或正在等待运行状态

​		S：休眠状态

​		T：停止或被追踪

​		Z： 僵尸进程

​		<：优先级较高的进程

​		N：优先级较低的进程

​		L：有些数据页被锁进内存

​		s：进程的主进程，在它之下有子进程

​		l：多线程，克隆线程

​		+：后台的进程组

START：该进程被触发启动的时间

TIME：该进程实际使用CPU的时间



* 查询进程启动命令 / 一层层查询父进程

有的时候，我们通过 top 看到某个进程 %cpu 很高，我们想看下到底是什么程序导致的，我们直接在 top 的界面按下”c“，发现他显示了部分命令，并不是我们想要的。这个时候，可以通过 `ps -ef | grep pid` 来进行查找，查找到的结果后，在此查看最后列是否有完整的命令，如果没有的话，就看下你查的这个 pid 的父进程是哪个，继续往下查，最终查到这些进程的最终父进程，就会有详细信息了。一般来说父（主）进程做的事情很少，基本比较吃cpu的都交给子进程去做了，所以往往我们看到的是子进程，需要一层一层去找到源头。 



* 查看系统全部进程的关系

可以使用 `pstree` 进行查看，不过显示的信息会比较多，可以搭配 less 或者more 进行使用。




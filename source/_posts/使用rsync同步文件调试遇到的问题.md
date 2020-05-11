---
title: 使用rsync同步文件调试遇到的问题
date: 2019-11-07 17:56:51
tags: [rsync, Linux]
category: Linux
---

## rsync 

rsync 可以用来做代码同步。以前还没接触这个工具的时候，都是用 scp 上传到服务器，然后在测试，有些麻烦，有时候索性就到服务器改了，所以最后造成代码不一致，引起诸多麻烦等等。

rsync 一般用法：

```shell
rsync -auv --progress /Users/home/project/project_finder zhaochen03@106.2.67.13:/home/username/.
```

这里需要注意： 如果ssh端口不是 22 端口,比如ssh端口是 2222，需要加上端口号：

```shell
<!--more -->
rsync -auv --progress /Users/home/project/project_finder zhaochen03@106.2.67.13:/home/username/.   -e " ssh -p 2222"
```

其底层是基于 SSH 的。如果在 ~/.ssh/config 中配置了信息，则可以直接：

```shell
rsync -auv --progress /Users/zhaochen/Netease/dsp ali:/home/zhaochen03/. 
```



# 坑

1. rsync 默认增量同步，比如 Python 中某个目录以前生成了 pyc 文件，但是后来把文件移动到另一个目录，而忘记更改 import 的路径，这样在服务器上是可以继续运行的，因为那个路径下是存在 pyc 文件的，而上线另一台服务器的时候就会报错。

2. rsync 同步的时候，是基于文件修改时间同步的，如果服务器上的文件修改时间新， 本地旧， 则从本地 rsync 就不会同步过去。


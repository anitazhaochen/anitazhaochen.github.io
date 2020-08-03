---
title: git-clone可选参数depth
date: 2020-08-03 14:21:50
tags: [Git]
category: Git
---

在国内，如果不搭梯子，使用 git clone 会比较慢。一旦遇到很大的仓库需要
clone 的时候，只能静静等待。

其实 git clone 有一些可选参数，可以让我们只 clone 我们需要的内容, 即减少了网络传输, 也省了时间。

* 不加任何参数

在不加任何参数的情况下，默认就是全部克隆。

并且这样也会把所有远程分支也克隆下来，其实很多分支我们是用不到的。

选择切换到其中的一个远程分支命令, 假设通过 `git branch -a` 有 `remotes/origin/dev` 分支：

<!--more -->
```shell
git checkout -b dev remotes/origin/dev
```

* single-branch 实现单一分支克隆, 其中 dev 分支在远程存在,对应的是 remotes/origin/dev

```shell
git clone -b dev --single-branch git@github.com/xxx/xx.git

```

* --depth 参数

一般而言，如果我们不是要去看这个仓库以前的提交，我们是没有必要把所有提交记录都
clone 下来的，使用 depth 参数可以选择最近的 n 次提交进行下载, n 越小，这个仓库占用
的磁盘空间就越小，因为每次修改提交后，`.git` 文件体积就会增大。

```shell
git clone -b dev --single-branch --depth 1 git@github.com/xxx/xx.git
```

上面这条命令就选择了我们想要的分支，及最近的一次提交。这样，大小就很精准的拿到我们想要的内容了。





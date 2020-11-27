---
title: Git保持干净的历史记录及清晰的提交记录
date: 2020-11-25 10:43:17
tags: [Git]
category: Git
---

## 让 git log 的每一条记录都有价值

合作共同开发项目的大致流程是：

1. 分配任务给每个开发者，每个开发者负责某块业务
2. 开始开发，开发者拉取 master 分支的代码，并且创建自己的分支
3. 某个开发者开发完成后，将自己的代码推送至自己本地分支对应的远程分支
4. 在 GitLab 页面上进行 merge request 操作，请求合并到 测试分支如 dev 分支
5. dev 分支测试完毕后，将 dev 分支合并至 master 分支。



稍微看一下项目的 git log 日志，会发现每个人写的 commit message 基本都不一样，还可能过一阵后自己的 commit message 自己都看不懂了。
<!--more -->

介绍一种 commit 规范，[Angular 规范](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#heading=h.greljkmo14y0)

```
<type>(<scope>): <subject>
// 空一行
<body>    
// 空一行
<footer>
```

* 第一行 Header 含义如下：

| type(必填) 用于说明 commit 的类别                         | scope：用于说明 commit影响的范围 | subject:commit目的的简短描述 |
| --------------------------------------------------------- | -------------------------------- | ---------------------------- |
| feat：新功能                                              | 数据层                           |                              |
| fix： 修补bug                                             | 控制层                           |                              |
| docs： 文档                                               | 视图层                           |                              |
| style：格式（不影响代码运行的变动）                       | 等等                             |                              |
| refactor：重构（既不是新增功能，也不是修改bug的代码变动） |                                  |                              |
| test：增加测试                                            |                                  |                              |
| chore：构建过程或辅助工具的变动                           |                                  |                              |

* Body 部分是对本次 commit 的详细描述，可以分为多行

应该注意代码变动的冬季，以及与以前行为的对比

* Footer 
  * 如果当前代码与上一个版本不兼容，则 Footer 部分以`BREAKING CHANGE`开头，后面是对变动的描述、以及变动理由和迁移方法。
  * 如果当前 commit 针对某个issue，那么可以在 Footer 部分关闭这个 issue 或者关闭多个 issue。



[参考-Commit message 和 Change log 编写指南](http://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html)



## 学会使用 Git rebase 

关于 git rebase 和 git merge 的区别就在于 前者可以保持良好清晰的历史记录。注意点就是： 仅在自己独立使用的分支上使用 git rebase， 否则可能造成丢失提交的风险。

[参考-彻底搞懂 Git-Rebase](http://jartto.wang/2018/12/11/git-rebase/)


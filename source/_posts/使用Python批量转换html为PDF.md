---
title: 使用Python批量转换html为PDF
date: 2020-08-28 16:54:51
tags: [Chrome, html, pdf]
category: Chrome
---

把 html 文件批量转换成 PDF 文件，然后再用 calibre 处理成 Kindle 的格式，就可以在
kindle 上面欣赏优秀的文章和博客了。

一开始，我拿到一堆 html 文件的时候，我记得 Chrome 浏览器可以点击文件，打印，然后
选择保存成 PDF 格式， 于是手动转换了几个 html 文件是在觉得麻烦物料，重复的操作。

正在前几天无意中看到了一个新的名词 Headless Chrome , 其实就是一个无界面的 Chrome 
浏览器，易于通过编程来进行控制。于是我自然就联想到了是否有 文件--打印--存储为PDF
这个 API， 看了一会，发现确实有。

于是马上开工，直接使用 Python 的 os 模块来循环执行生成，最终还算满意，都转换成了 PDF。

既然能编程了，那要求可能就不能止于此了， 尝试把广告，无用的水印，无关的内容都去掉，
<!--more -->

然后操作流程就是：

1. 读取 html 文件

2. 通过正则表达式，xpath 表达式等来提取替换内容

3. 将替换之后的文件写入新的 html 文件中

4. 使用 headless 来生成 PDF 文件

最终得到的 PDF 文件就基本没有广告了，并且看着也简约, 并且最终转换到 kindle 对应的
格式也不会因为以前的广告导致错位。

代码就先不贴了，有一个问题就是用编程无法像手动一样去除页眉操作，看着很难受，于是乎
搜了一下，发现有了解决方案， 其实就是在 html 文件中写入一端 css 代码，需要注意的是
需要将css 写在 css 应该写到的位置，否则无效。
[去除页眉参考](https://stackoverflow.com/questions/46077392/additional-options-in-chrome-headless-print-to-pdf)
[How can I remove page number when I use --print-to-pdf?](https://github.com/Zenika/alpine-chrome/issues/7)
[Headless Chrome 入门](https://zhuanlan.zhihu.com/p/29207391)

---
title: linux编辑器
date: 2018-03-05 16:39:31
tags: [linux, 文本处理器]
category: linux
---



# GNU awk

文本处理三工具：grep，sed，awk
    grep，egrep，fgrep：文本过滤工具：pattern
    sed：行编辑器
<!-- more -->
        模式空间、保持空间
    awk：报告生成器，格式化文本输出
    
    AWK：AHo，Weinberger，Kernighan --> New AWK，NAWK
    
    GUN awk，gawk

gawk - pattern scanning and processing language

    基本用法： gawk [options] 'program' FILE ...
        program: PATTERN{ACTION STATEMENTS}
            语句之间用分号分割
            
            print，printf
            
        选项：
            -F： 指明输入时用到的字段分隔符
            -v var=value： 自定义变量

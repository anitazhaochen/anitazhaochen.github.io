---
title: 运行 Python 使用 sudo 注意
date: 2017-10-04 16:47:56
tags: [Linux, Python, sudo]
category: Python
---
# 如果此时正是虚拟环境，那么sudo之后，执行的位置一定不是虚拟环境的python，或者 pip 因为 sudo 之后就是root的环境变量了，所以会出错，如果一定要使用sudo ，那么请写绝对路径来 使用 python 或者 pip.


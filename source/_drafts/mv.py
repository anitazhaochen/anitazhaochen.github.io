#!/usr/bin/python3
#coding:utf8
import sys
import os

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("缺少文章题目参数")
        exit(-1)
    else:
        print(sys.argv[1])
        with open(sys.argv[1],'r') as f:
            li = f.readlines()
            li.insert(20,"<!--more -->\n")
            with open (sys.argv[1],"w") as f:
                f.writelines(li)
        os.popen(r"sed  's/\(^.*!\[.*\)\.\.\(.*\)/\1\2/g' %s > ../_posts/%s"%(sys.argv[1], sys.argv[1]))
        os.popen("mv %s %s.bak"%(sys.argv[1],sys.argv[1]))
        print("已发布完成")

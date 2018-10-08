#!/usr/bin/python3
#coding:utf8
import sys
import os

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print "缺少文章题目参数"
        exit(-1)
    else:
        print sys.argv[1]
        os.popen(r"sed  's/\(^ *!\[image.*\)\.\.\(.*\)/\1\2/g' %s > ../_posts/%s"%(sys.argv[1], sys.argv[1]))
        os.popen("mv %s %s.bak"%(sys.argv[1],sys.argv[1]))
        print "已发布完成"

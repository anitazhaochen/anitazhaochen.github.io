#!/bin/bash

if [ $# == 0 ]
then
  echo "请输入提交信息再次执行"
  exit 2
fi

echo "开始生成静态文件"


echo "准备开始发布"

echo "正在提交 GitLab 备份"
`git pull origin && hexo g`
`git add . && git commit -m "$1" && git push origin dev`
echo "提交到dev分支完成"



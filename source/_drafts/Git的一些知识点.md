---
title: Git的一些知识点
tags:
---



# git如何解决代码冲突

git stash 
git pull 
git stash pop 
这个操作就是把自己修改的代码隐藏，然后把远程仓库的代码拉下来，然后把自己隐藏的修改的代码释放出来，让 git 自动合并。

如果要代码库的文件完全覆盖本地版本。 
git reset –hard

git pull

# git merge和git rebase的区别

git merge把本地代码和已经取得的远程仓库代码合并。

git rebase是复位基底的意思，git merge 会生成一个新的节点，之前的提交会分开显示，而rebase操作不会生成新的操作，将两个分支融合成一个线性的提交。

# reset 与 rebase, pull 与 fetch 的区别

git reset 不修改commit相关的东西，只会去修改.git目录下的东西。

git rebase 会试图修改你已经commit的东西，比如覆盖commit的历史等，但是不能使用rebase来修改已经push过的内容，容易出现兼容性问题。rebase还可以来解决内容的冲突，解决两个人修改了同一份内容，然后失败的问题。

git pull=fetch+merge,

使用git fetch是取回远端更新，不会对本地执行merge操作，不会去动你的本地的内容。

而是用git pull会更新你本地代码到服务器上对应分支的最新版本

[git rebase 写的很好 ](http://jartto.wang/2018/12/11/git-rebase/)

## git rm 和 git rm --cached 和 rm 的区别



* git rm 会连附带本地文件一起删除。

  即：我们需要删除缓存区或分支上的文件，同时工作区也不需要这个文件了

* git rm --cached 只会将文件移除缓存区，让 git 不在跟踪

  即： 如果我们只是不希望这个文件被版本控制，而且本地还能使用，我们就只需要删除暂存区上的文件。

* rm

  直接使用 rm 命令也可以删除文件只不过：

  git rm  =  rm file  && git add file 然后提交

* 有一些文件由于误操作的原因，被 git 跟踪了，但是我们其实不想让git 跟踪，这时应该先 git rm --cached file 停止跟踪文件，然后再在 .gitignore 里面添加文件。



## git cherry-pick 

可以理解为 “挑拣”提交，它会获取某一个分支的单笔提交，并作为一个新的提交引入到你当前分支删。当我们需要在本地合入其他分支的提交时，如果我们不想对整个分支进行合并，而是只想将某一次提交和入到本地当前分支上，那么久要使用 git cherry-pick 了。

首先选择哪一个提交作为补丁，记录下 commit id 。 然后 切换至要打补丁的分支，然后执行

`git cherry-pick  xxxxxxxxxx`

如果没有出现冲突，该命令将自动提交。如果不想让它自动提交，则加参数 -n 即可。

* 发生冲突

  手动修改冲突文件，然后执行   `git add .`  然后执行  `git cherry-pick --continue`
---
title: git常用操作
categories: [tools-devops]
tags: js
date: 2021-03-29 19:03:04
---
> 梳理 git 中易混的操作

## git reset (--hard)

git reset + commitId 返回指定 id 的提交，但是依然会保存我们已经提交的代码，知识 log 信息会删除
git reset --hard 会重置所有已提交的代码到指定的版本

## git rebase -i id

以对应的 id 提交为基础，做处理

### 配合 git fetch 做一个合并冲突的操作

git fetch + 远程分支名，先把远程分支的代码更新到本地
git rebase + 分支名 ，这样处理后就是本地的修改都是基于远程的版本做的修改，分支是干净的，对比直接 git merge 需要提交一次合并冲突的 commit

## git revert

代码回滚到指定分支，并生成一次新的 commit

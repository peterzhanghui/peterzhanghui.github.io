---
title: git配置多个用户
categories: 前端开发
tags: js
date: 2022-08-01 22:19:43
---
## 前言
一般我们使用git，拉取代码，首先会生成SSH公钥，然后把公钥添加到对应的代码平台，最后本地配置一下用户名和邮箱，就可以愉快的拉取修改代码了。

```

git config --global user.name "XXXX"
git config --global user.email "XXX@XXX.com" 
```
## 问题
但是工作中，我们会经常需要有多个平台账号，例如，github，gitlab，gitee等，这时候就需要给git配置多用户。不同平台前两步都一样，最后需要不同平台配置不同的用户名。

## 解决方案
### 配置方式
~/.gitconfig
```
[user]
        name = XXXX
        email = XXX@XXX.com
[includeIf "gitdir:~/Documents/workSpace/github/"]
        path = .gitconfig-github
[includeIf "gitdir:~/Documents/workSpace/gitee/"]
        path = .gitconfig-gitee
```

### 新增github配置文件
~/.gitconfig-github 配置如下：
```
[user]
    name = githubName
    email = XXXXX@XX.com
```
## 总结
这样当项目在 ~/Documents/workSpace/github/ 文件夹中，就会读取对应的配置文件，其他平台同理。
完美解决，收工！！
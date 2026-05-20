---
title: github 网站使用问题及解决方法总结
categories: [tools-devops]
date: 2020-11-17
tags: 环境配置
---
## 静态资源加载失败问题

> 访问 github 的时候，头像图片加载失败，有时候页面布局也会有问题，打开控制台发现，github 二级域名下的静态资源加载失败。

因为浏览器对 http 请求的并发数量是有限制的，如果请求数量超出限制，就会阻塞。其中 Chrome 浏览器最多允许对同一个域名 Host 建立 6 个 TCP 连接，不同的浏览器有所区别
github 这样把静态资源放到多个二级域名下，可以提高加载速度，

### 可能出错的原因

- dns 污染，本地 dns 配置错误
- github 相关域名 ip 修改

### 解决方案

> 问题找到啦，接下来就是解决方案，通过修改 hosts 文件中 github 相关静态资源域名的 dns 配置。步骤如下

## 一、 打开终端,编辑 host 文件

### macOs 系统

```
sudo vim /etc/hosts
```

### windows 系统

找到文件 C:\Windows\System32\drivers\etc\hosts

## 二、配置 dns

> 如果以前 host 中已经配置过，可以先注释掉，然后跳过第二步，刷新 dns。如果不生效再自行通过 dns 查询工具查询最快的 ip 地址 当前使用的配置。

dns 查询工具

- [站长工具 dns 查询](http://tool.chinaz.com/dns/) 推荐的 ip 不太稳定
- [ipaddress.com](https://www.ipaddress.com/) 推荐的更稳定

```
# GitHub Start
# 192.30.253.112 github.com
192.30.253.119 gist.github.com
199.232.96.133 assets-cdn.github.com
199.232.96.133 raw.githubusercontent.com
199.232.96.133 gist.githubusercontent.com
199.232.96.133 cloud.githubusercontent.com
199.232.96.133 camo.githubusercontent.com
199.232.96.133 avatars0.githubusercontent.com
199.232.96.133 avatars1.githubusercontent.com
199.232.96.133 avatars2.githubusercontent.com
199.232.96.133 avatars3.githubusercontent.com
199.232.96.133 avatars4.githubusercontent.com
199.232.96.133 avatars5.githubusercontent.com
199.232.96.133 avatars6.githubusercontent.com
199.232.96.133 avatars7.githubusercontent.com
199.232.96.133 avatars8.githubusercontent.com
# GitHub End
```

## 三、刷新 mac 系统 dns 缓存

### macOs 系统

```
sudo killall -HUP mDNSResponder
```

### windows 系统

```
ipconfig /flushdns
```

刷新缓存后，打开页面刷新即可。此问题完美解决

## github 网站无法加载问题

访问网站提示网站无法访问，可能就是 github.com 的 dns 被污染啦，解决和上面也是一样的流程。

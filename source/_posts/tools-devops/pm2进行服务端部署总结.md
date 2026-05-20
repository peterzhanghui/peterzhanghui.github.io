---
title: pm2进行服务端部署总结
date: 2020-11-30
categories: [tools-devops]
tags: pm2
---
> 因为是做平台相关项目，所以对 seo 有要求, 所以考虑 使用 nuxt.js 实现服务端渲染，一个有利于 seo, 还可以提高页面加载速度。
> 本地开发一切顺利，线上部署遇到了以下问题：

1. 构建好的代码放到服务器端，直接 npm run start 终端关掉，进程也会被停掉
2. 使用 npm run start & 在后台运行， 终端关掉服务正常，但是不能维持稳定的服务，进程还是会挂

## 解决方案：[pm2，查看官网详细教程](https://pm2.keymetrics.io/)

> pm2 守护进程管理器，管理和保持应用程序在线，而且可以使用集群模式，根据可用的 CPU 数量进行缩放，这将大大提高应用程序的性能和可靠性

## 安装并使用 pm2

```
npm install -g pm2
```

使用 pm2 启动 node 服务

```
pm2 start npm -i 0 --name mobile --update-env --log-date-format 'DD-MM HH:mm:sds.SSS' -- run start —watch
```

使用 curl ip + 端口 检查启动是否成功

```
curl 127.0.0.1:3000
```

正常启动后，浏览器 ip + 端口也可以正常访问，最后阿里云做一下域名解析，服务端 nginx 设置一下反向代理就可以使用域名访问了。

### pm2 常用操作

重启服务

```
pm2 researt all/name
```

删除服务

```
pm2 delete all/name
```

pm2 查看实时的日志输出

```
pm2 logs
```

pm2 错误日志保存地址

```
cd /root/.pm2/logs
```

终端监视内存和 CPU

```
pm2 monit
```

查看列表

```
pm2 list
```

## 常用操作

查看端口号是否被占用

```
查看3000 端口
Mac: lsof -i:3000
centos: netstat -lnp|grep 3000
```

停掉进程

```
kill -9 + id  // 停掉指定id的进程
pkill -9 + name  // 停掉指定name程序的所有进程
```

## 总结

- 直接使用 node server.js 开启服务，修改文件无法热更新，需要关闭进程重新启动
- 开发环境可以使用 nodemon 文件修改，进程自动重启
- 服务端使用 pm2 直接后台运行服务，不占用终端，文件修改后需要 reload

目前对于 pm2 的使用可以满足项目需要，但是实现的还是不够优雅，需要再优化一下，后续有更好的实现也会持续更新。如果有不对的，或者各位大佬有好的实现方案，也希望可以不吝赐教（手动抱拳）

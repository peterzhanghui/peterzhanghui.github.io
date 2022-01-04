---
title: nginx
categories: 前端开发
tags: js
date: 2022-01-04 11:11:41
---

Mac

1. 安装Homebrew（若已安装，可以跳过）
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. 使用brew安装nginx
```
brew install nginx
```

3. 启动nginx
```
brew services start nginx
```

4. 将nginx设置为开机自启
```
launchctl start ~/Library/LaunchAgents/homebrew.mxcl.nginx.plist
```
5. 设置nginx通用配置
```
vim /usr/local/etc/nginx/servers/fe_91jkys_qa.conf
```
6. 粘贴如下配置
```
server {
  listen 80;
  server_name *.qa.91jkys.com;

  if ($http_host ~* "^(.*?)\.qa\.91jkys\.com$") {
    set $domain $1;
  }

  location / {
    proxy_pass http://127.0.0.1:$1;
    proxy_redirect     off;
    proxy_set_header   Host             $http_host;
    proxy_set_header   X-Real-IP        $remote_addr;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
  }
}
```
7. 重载/重启nginx
```
nginx -t # 检查配置是否正确
nginx -s reload # 重载nginx（2、3行任选一个命令执行）
brew services restart nginx # brew重启nginx（2、3行任选一个命令执行）
```
8. 根据本地端口配置hosts，如
```
# 本地启了个 3000、3001、3002 项目，不需要更改nginx配置，直接添加三个host，如

sudo vim /etc/hosts

# 添加三行

127.0.0.1 3000.qa.91jkys.com
127.0.0.1 3001.qa.91jkys.com
127.0.0.1 3002.qa.91jkys.com
```
9. 直接访问试试，后面有新端口直接配host就行，有任何问题可以联系：张文

Centos7+/Ubuntu18+
1. 安装nginx
```
yum install -y nginx # centos
apt install -y nginx # ubuntu
```
2. 启动
```
systemctl start nginx # 启动nginx
systemctl enable nginx # 开机自启
```
3. 剩余配置参考上方【Mac】5~9 配置部分，注意二则配置文件保存路径的区分，一般配置文件路径参考：
```
 vim /etc/nginx/conf.d/fe_91jkys_qa.conf
```
Windows（win10+）
直接在Windows应用商店下载一个Ubuntu，作为win的子系统，参考上面方式即可。
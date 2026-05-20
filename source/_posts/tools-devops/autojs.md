---
title: 连接 VS Code 电脑端进行编辑调试
date: 2020-11-12
categories: [tools-devops]
tags: autojs
---
> auto.js 一个支持无障碍服务的 Android 平台上的 JavaScript IDE，同时有 VS Code 插件可提供基础的在桌面开发的功能，既可以在手机端直接编写代码，也可以使用 vs code
> 因为习惯使用电脑端开发，所以主要讲解基于 VS Code 插件的桌面开发

## 开发环境搭建

1. 手机端下载 auto.js 电脑端安装 vs code
2. vs code 中安装 Auto.js-VSCodeExt 插件

### 然后参照插件的说明

> Step 1
>
> 按 Ctrl+Shift+P 或点击"查看"->"命令面板"可调出命令面板，输入 Auto.js 可以看到几个命令，移动光标到命令 Auto.js: Start Server，按回车键执行该命令。此时 VS Code 会在右上角显示"Auto.js server running"，即开启服务成功。
>
> Step 2
>
> 将手机连接到电脑启用的 Wifi 或者同一局域网中。通过命令行 ipconfig(或者其他操作系统的相同功能命令)查看电脑的 IP 地址。在 Auto.js 的侧拉菜单中启用调试服务，并输入 IP 地址，等待连接成功。
>
> Step 3
>
> 之后就可以在电脑上编辑 JavaScript 文件并通过命令 Run 或者按键 F5 在手机上运行了。

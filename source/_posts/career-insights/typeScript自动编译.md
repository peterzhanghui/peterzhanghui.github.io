---
title: typeScript文件保存时自动编译
categories: [career-insights]
tags: typeScript
date: 2021-02-14 15:04:20
---
> typeScript 文件保存时自动编译，官网教程中的 提到的 vsCode 插件 atom-typescript，在 vsCode 中搜索没找到。

## 1、全局安装 typeScript

```
npm install -g typescript
```

## 2、手动编译

创建完成 ts 文件后运行 tsc test.ts，会在当前目录下生成同名的 js 文件。

```
tsc test.ts
```

## 3、自动编译

### a、生成配置 ts 文件

在项目根目录生成 tsconfig.json 文件，可以修改相关 ts 配置，设置编译后的 js 文件目录

```
tsc --init
```

### b、在 vsCode 中配置

终端 -> Run Task -> typescript -> tsc: watch - tsconfig.json

### c、直接在命令行监听修改，自动更新

```
tsc -w
```

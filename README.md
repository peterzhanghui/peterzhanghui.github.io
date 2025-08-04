# peterzhanghui.github.io

## 📖 项目简介

个人技术博客网站，基于 Hexo 静态网站生成器构建，部署在 GitHub Pages 上。

**🔗 网站地址：** [https://peterzhanghui.github.io/](https://peterzhanghui.github.io/)

记录开发学习过程中的一些思考，对知识的一个总结梳理的过程，让自己可以理解的更加透彻，当然如果对你有所帮助，也希望可以一起讨论交流。

## 🛠️ 技术栈

- **静态网站生成器：** [Hexo](https://hexo.io/)
- **主题：** Fluid
- **部署平台：** GitHub Pages
- **包管理器：** npm/yarn

## 📋 环境要求

- Node.js >= 14.0.0
- npm >= 6.0.0 或 yarn >= 1.0.0
- Git

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/peterzhanghui/peterzhanghui.github.io.git
cd peterzhanghui.github.io
```

### 2. 安装依赖

```bash
npm install
# 或者使用 yarn
yarn install
```

### 3. 本地开发

```bash
# 启动本地服务器
hexo server
# 或者简写
hexo s

# 默认访问地址：http://localhost:4000
```

### 4. 新建文章

```bash
# 创建新文章
hexo new "文章标题"

# 创建新页面
hexo new page "页面名称"
```

## 📦 构建与部署

### 本地构建

```bash
# 清理缓存文件
hexo clean

# 生成静态文件
hexo generate
# 或者简写
hexo g
```

### 部署到 GitHub Pages

#### 方式一：手动部署

```bash
# 1. 构建静态文件
hexo clean && hexo generate

# 2. 进入 public 目录
cd public

# 3. 初始化 git 仓库（首次部署）
git init
git add .
git commit -m "Deploy blog"
git branch -M main
git remote add origin https://github.com/peterzhanghui/peterzhanghui.github.io.git
git push -u origin main

# 4. 后续部署
git add .
git commit -m "Update blog"
git push
```

#### 方式二：使用 hexo-deployer-git（推荐）

1. 安装部署插件：
```bash
npm install hexo-deployer-git --save
```

2. 配置 `_config.yml`：
```yaml
deploy:
  type: git
  repo: https://github.com/peterzhanghui/peterzhanghui.github.io.git
  branch: main
```

3. 一键部署：
```bash
hexo clean && hexo deploy
# 或者简写
hexo clean && hexo d
```

## 📁 项目结构

```
peterzhanghui.github.io/
├── _config.yml              # Hexo 主配置文件
├── _config.fluid.yml        # Fluid 主题配置文件
├── package.json             # 项目依赖配置
├── scaffolds/               # 文章模板
│   ├── draft.md            # 草稿模板
│   ├── page.md             # 页面模板
│   └── post.md             # 文章模板
├── source/                  # 源文件目录
│   ├── _posts/             # 博客文章
│   ├── about/              # 关于页面
│   ├── img/                # 图片资源
│   └── CNAME               # 自定义域名
├── themes/                  # 主题目录
└── public/                  # 生成的静态文件（部署文件）
```

## ✍️ 写作指南

### 文章 Front Matter

```yaml
---
title: 文章标题
date: 2024-01-01 12:00:00
categories: 分类
tags: 
  - 标签1
  - 标签2
description: 文章描述
---
```

### 图片资源管理

1. 将图片放在 `source/img/` 目录下
2. 在文章中使用相对路径引用：
```markdown
![图片描述](../img/图片文件名.png)
```

### 常用命令

```bash
# 新建文章
hexo new post "文章标题"

# 新建草稿
hexo new draft "草稿标题"

# 发布草稿
hexo publish "草稿标题"

# 启动本地服务器（调试模式）
hexo server --debug

# 生成静态文件并启动服务器
hexo generate --watch
hexo server
```

## 🔧 主题配置

主题配置文件：`_config.fluid.yml`

主要配置项：
- 网站基本信息
- 导航菜单
- 首页设置
- 文章页面设置
- 评论系统
- 数据统计
- 社交链接

详细配置请参考 [Fluid 主题文档](https://hexo.fluid-dev.com/docs/)

## 📈 SEO 优化

- 配置网站 sitemap
- 设置合适的 meta 标签
- 优化图片 alt 属性
- 配置百度/Google 统计
- 提交搜索引擎收录

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 更新日志

查看 [提交历史](https://github.com/peterzhanghui/peterzhanghui.github.io/commits/main) 了解项目更新详情。

## 📧 联系方式

如果你有任何问题或建议，欢迎通过以下方式联系：

- GitHub Issues: [提交问题](https://github.com/peterzhanghui/peterzhanghui.github.io/issues)
- 个人网站: [https://peterzhanghui.github.io/](https://peterzhanghui.github.io/)

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

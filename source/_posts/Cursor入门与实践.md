---
title: Cursor入门与实践
categories: 前端开发
tags: js
date: 2025-04-25 13:42:07
---

## 简介

Cursor是一款基于VS Code的增强型代码编辑器，专为AI辅助编程而设计。它在保留VS Code熟悉的编辑体验基础上，深度集成了先进的AI功能，使开发人员能够更高效地编写和理解代码。

文档中展示的截图和相关配置项都是以Cursor 官网目前最新版本（0.48.9）为准

## 1. 基础配置&迁移

### 1.1 个性化设置

*   **界面汉化**: 在 VS Code 扩展市场搜索 "Chinese (Simplified) Language Pack for Visual Studio Code" 并安装。
    
*   **活动栏垂直布局**: 在设置 (Cmd/Ctrl + ,) 中搜索 `workbench.activityBar.orientation`，将其值修改为 `vertical`。
    

修改前：

![image.png](../img/Cursor入门与实践/img/image_1.png)

修改后：

![image.png](../img/Cursor入门与实践/img/image_2.png)

### 1.2 VSCode 

从VSCode迁移，相关配置

![image.png](../img/Cursor入门与实践/img/image_3.png)

### 1.3 WebStorm 

[![image](../img/Cursor入门与实践/img/image_4.png)](https://pic-bed-1256249917.cos.ap-chengdu.myqcloud.com/uPic/image-20250401%E4%B8%8B%E5%8D%8843220485.png)

WebStorm 专注于前端开发，Cursor 通过以下扩展可提供类似功能：

*   [JavaScript and TypeScript Nightly](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-next)：最新语言特性
    
*   [ES7+ React/Redux Snippets](https://marketplace.visualstudio.com/items?itemName=dsznajder.es7-react-js-snippets)：React 开发代码片段
    
*   [Vue Language Features](https://marketplace.visualstudio.com/items?itemName=Vue.volar)：Vue.js 支持
    
*   [Angular Language Service](https://marketplace.visualstudio.com/items?itemName=Angular.ng-template)：Angular 开发
    
*   [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) 和 [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)：代码检查和格式化
    

许多 WebStorm 功能已内置于 Cursor/VS Code，包括：

*   npm 脚本视图（在资源管理器中可见）
    
*   调试 JavaScript/TypeScript
    
*   Git 集成
    
*   TypeScript 智能补全和类型检查

## 2. 主要功能介绍

### 2.1 智能补全与编辑

*   **Tab 补全**: 智能预测并补全代码，支持多种语言和框架。
    
    *   与 GitHub Copilot 对比：Cursor 提供更深度的项目上下文理解。
        
*   **内联编辑 (Cmd/Ctrl+K)**: 选中代码后按 `Cmd/Ctrl+K` 快速唤起 AI 进行修改或生成，无需离开当前编辑位置。
    
    *   **代码场景**: 快速修改、重构、解释选中代码。
        
    *   **终端场景**: 在终端中按 `Cmd/Ctrl+K`，可以用自然语言描述生成需要的命令行代码。
        

### 2.2 AI 对话功能-Ask&Agent

*   **需求开发：**通过自然语言与AI对话沟通，实现需求开发 
    
*   **代码库问答**: 能够基于整个代码库回答问题，理解项目结构和依赖。
    

## 3. 收费与免费版本对比

![image.png](../img/Cursor入门与实践/img/image_5.png)

### 3.1 高级请求的次数

**更多高级模型调用次数**: 免费版对 GPT-4o, Claude 3 等高级模型的调用次数有限制，付费版提供更多或无限制的调用。GPT-4o 和 Claude 3.5/3.7 Sonnet 都属于高级模型。每次使用 o1-mini 将消耗 1/3 次高级请求。

### 3.2 什么是快速请求和慢速请求？

高级模型的快速请求会被后端优先处理。在 Pro 版中，达到快速请求上限后仍可使用高级模型，但在高负载时请求可能会排队。

## 4. AI 模型差异与选择建议

### 4.1 可用模型

Cursor 支持多种 AI 模型，不同的模型在性能、成本和可用功能上有所差异。以下是部分可用模型及其信息的概述 (信息可能随时间变化，请以 Cursor 官方为准):

|  名称  |  提供方  |  Premium  |  Agent  |  Price⁶  |  Notes  |
| --- | --- | --- | --- | --- | --- |
|  `claude-3.7-sonnet`  |  Anthropic  |  ✓  |  ✓  |  $0.04  |   |
|  `claude-3.7-sonnet (MAX)`  |  Anthropic  |  **MAX**  |  ✓  |  $0.05  |  ¹  |
|  `claude-3.5-haiku`  |  Anthropic  |  ✓  |   |  $0.01  |  ²  |
|  `claude-3-opus`  |  Anthropic  |  ✓  |   |  $0.10  |  ³  |
|  `deepseek-v3`  |  Fireworks  |   |   |  免费  |   |
|  `gemini-2.5-pro-exp`  |  Google  |  ✓  |  ✓  |  $0.04  |   |
|  `gemini-2.5-pro-exp (MAX)`  |  Google  |  **MAX**  |  ✓  |  $0.05  |  ¹  |
|  `gpt-4o`  |  OpenAI  |  ✓  |  ✓  |  $0.04  |   |

**表格说明:**

*   **Premium**: 是否属于高级模型（通常需要付费计划或有使用限制）。`MAX` 可能表示需要最高级别的付费计划。
    
*   **Agent**: 是否支持 Agent 模式（允许 AI 调用工具如文件系统、终端等）。
    
*   **Price⁶**: 每次请求的参考价格（美元）。注意角标 `⁶` 的解释。
    
*   **Notes**: 表格中数字角标的解释如下：（重点关注1、3、6）
    
    *   **¹ (Tool calls charged like requests)**: 对于标记 `¹` 的模型, 在 Agent 模式下使用工具调用会像普通聊天请求一样消耗请求次数或计费。
        
    *   **² (1/3 request)**: 对于标记 `²` 的模型，每次调用仅消耗 1/3 次标准请求额度。
        
    *   **³ (10 requests/day included with paid plan)**: 对于标记 `³` 的模型，付费计划用户每天可免费调用这些特定模型 10 次。
        
    *   **⁴ (500 requests/day with free plan)**: 对于标记 `⁴` 的模型，免费计划用户每天可免费调用此模型 500 次。
        
    *   **⁵ (High reasoning effort)**: 标记 `⁵` 的模型需要较高的推理成本，可能响应较慢。
        
    *   **⁶ (Prices are higher for long context window requests)**: "Price"列显示的是基础价格。处理长上下文的请求，实际价格会更高。
        

### 4.2 模型选择建议

*   场景适用性分析
    
    *   代码生成：GPT-4 和 Claude 表现最佳
        
    *   代码解释：Claude 更适合复杂逻辑分析
        
    *   文档生成：GPT-4 和 Claude 均可
        
    *   问题解答：Claude 更擅长
        

## 5. 使用模式选择

![image.png](../img/Cursor入门与实践/img/image_6.png)

### 5.1 Ask 模式

之前版本的 Chat 模式。

*   **适用场景**:
    
    *   **需求沟通与确认**: 在开始编码前，与 AI 沟通确认需求细节，确保理解一致。
        
    *   **问题咨询**: 询问技术问题、寻求解决方案、获取代码示例。
        
    *   **文档生成**: 快速生成函数注释、README 文档、API 文档等。
        

### 5.2 Agent 模式

默认模式，带来更强大和统一的 AI 体验，能够支持自动 web 联网操作。

*   **适用场景**:
    
    *   **智能代码生成与修改**: 适合编写新功能、重构复杂逻辑，或需要 AI 跨多个文件进行修改的场景。
        
    *   **处理复杂任务**: AI 可以根据指令自动规划并执行一系列操作（如查找文件、编辑代码、运行命令）。
        
*   **注意**: Agent 模式下，AI 的每次回复可能包含多个工具调用（如读文件、写文件、搜索等）。每次请求最多包含 25 个工具调用，超出部分会作为新的请求计费。
    

### 5.3 Manual 模式

手动模式，适合需要精确控制代码修改，或 AI 自动修改不符合预期时进行手动调整。

## 6. 对话上下文管理

*   **上下文窗口限制**: 不同 AI 模型的上下文窗口大小不同，会影响 AI 能"记住"的对话历史长度。长对话可能导致早期信息丢失。
    
*   **上下文保留策略**: AI 会尝试保留最重要的信息，但长对话或复杂任务下效果可能下降。
    

### 6.1 当前限制

目前不同模型的限制![image.png](../img/Cursor入门与实践/img/image_7.png)

### 6.2 解决方案

*   **提示用户**: 当上下文过长时，Cursor 会提示用户可能需要开启新窗口或减少上下文范围。
    
*   **手动开启新窗口**: 对于不同的独立任务，手动开启新的聊天窗口是保持上下文清洁的最佳实践。
    
*   **任务拆解**: 将复杂的大任务拆解成更小的、可以分步处理的子任务，引导 AI 逐步完成。
    
*   **手动管理**: 使用 `@` 精确引入需要的上下文，或在聊天中明确指示 AI "忽略之前的讨论，专注于当前问题"。
    

## 7. rule 规则设置

在 0.45 版本之后，Cursor 有两种 Rules 的方式，一种是 Project Rules（官方推荐），一种是 User Rules。

目前社区已经有很多成熟的 cursorrules 可供参考，可以先拷贝到项目中，再根据自己特定规范进行修改。

*   [https://github.com/PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)
    
*   [https://cursor.directory/](https://cursor.directory/)
    
*   [https://cursorlist.com/](https://cursorlist.com/)
    

### 7.1 个人规则配置 (全局生效)

配置应用于所有项目的个人编码偏好。可以配置以下规则：

*   代码风格
    
*   命名规范
    
*   文件组织
    

![image.png](../img/Cursor入门与实践/img/image_8.png)

### 7.2 项目规则设置 (当前项目生效)

针对特定项目设置的规则，会覆盖个人规则 。可以配置以下规则：

*   代码行数限制（>300行建议提取单独组件）
    
*   环境文件管理（禁止覆盖.env）
    
*   环境区分（dev/test/production）
    
*   生产环境规范（禁用mock）  
    ![image.png](../img/Cursor入门与实践/img/image_9.png)
    

## 8. Notepad 功能详解

**项目文档集成**:  Markdown 文件，用于记录项目特定的需求文档、接口文档、设计思路等

Notepad 为实验功能，需要在设置中开启

![image.png](../img/Cursor入门与实践/img/image_10.png)

使用示例：

![image.png](../img/Cursor入门与实践/img/image_11.png)


## 9. 错误处理

### 9.1 项目运行报错

*   **截图辅助诊断**: 将运行报错的截图粘贴到聊天窗口，AI 可以识别错误信息并提供修复建议。
    

### 9.2 控制台报错处理

*   **AI 自动修复 (Lint Errors)**: Cursor 可以自动识别并一键修复常见的 Linter 错误。
    
*   **自动获取错误信息**: 当程序运行出错时，可以直接复制控制台的错误堆栈信息给 AI，让其分析原因。
    

## 10. MCP (Machine Control Protocol)

### 10.1 概述

MCP（[Model Context Protocol](https://zhida.zhihu.com/search?content_id=256500246&content_type=Article&match_order=1&q=Model+Context+Protocol&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NDU0NjE2MjIsInEiOiJNb2RlbCBDb250ZXh0IFByb3RvY29sIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6MjU2NTAwMjQ2LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.5dEyEZyelqPoc2YPlhSWbi-f70ZvwRaNw5HqjFO0s1o&zhida_source=entity)）是一种开放协议，它标准化了应用程序如何向大语言模型（[LLMs](https://zhida.zhihu.com/search?content_id=256500246&content_type=Article&match_order=1&q=LLMs&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NDU0NjE2MjIsInEiOiJMTE1zIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6MjU2NTAwMjQ2LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.ruB41XzLMC-btn_XMzHpjEA7iXl5bOA1wCRm9FbNJsw&zhida_source=entity)）提供上下文。你可以把它理解为 AI 应用的“USB-C 接口”，让 AI 模型能够安全、有效地和外部数据源、工具进行交互，以完成更复杂的任务。

看一下官方的MCP架构图:

![34fbb14fc889d99deb0c921ee818877c.jpeg](../img/Cursor入门与实践/img/image_12.jpeg)

MCP 的核心遵循客户端-服务器架构，其中主机应用程序可以连接到多个服务器：

*   **本地数据源**：MCP 服务器可以安全访问的您计算机上的文件、数据库和服务
    
*   **远程服务**：MCP 服务器可以通过互联网（例如通过 API）连接到的外部系统
    

### 10.2 推荐的 MCP 资源市场

### 目前有多个优质的 MCP 资源市场，可以寻找并安装各种功能的 MCP 服务：

*   Smithery：[https://smithery.ai/](https://smithery.ai/)
    
*   Mcp.so：[https://mcp.so/](https://mcp.so/)
    
*   PulseMCP：[https://www.pulsemcp.com/servers](https://www.pulsemcp.com/servers)
    
*   Glama：[https://glama.ai/mcp/servers](https://glama.ai/mcp/servers)
    
*   Cursor Directory：[https://cursor.directory/mcp](https://cursor.directory/mcp)
    
*   MCP 官方 Github：[https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
    

### 10.3 mcp推荐

**filesystem：**可以对项目外的文件进行操作

![image.png](../img/Cursor入门与实践/img/image_13.png)

**sequentialthinking：**支持复杂问题的分步拆解、动态调整、分支推演和多方协作

![image.png](../img/Cursor入门与实践/img/image_14.png)

## 11. 实践提效小技巧

### 11.1 常见使用场景

**图像生成代码**: 在聊天窗口上传 UI 设计稿截图，让 AI 生成对应的 HTML/CSS 或组件代码。

**基于 Git 修改生成测试用例**: 使用 `@git` 引入最近的提交，让 AI 分析变更内容，生成测试用例清单用来自测。

![image.png](../img/Cursor入门与实践/img/image_15.png)

**使用联网功能**：使用`@web` ，快速获取最新的信息。

**使用 checkpoint 一键回滚：**

![image.png](../img/Cursor入门与实践/img/image_16.png)

**快捷键**: 熟练使用 `Cmd/Ctrl+K` (内联编辑/终端生成), `Cmd/Ctrl+L` (聊天) 等核心快捷键。

终端使用自然语言生成命令

![image.png](../img/Cursor入门与实践/img/image_17.png)

代码中使用，针对选中代码快速提问

![image.png](../img/Cursor入门与实践/img/image_18.png)

**上下文管理快捷键**: 在聊天输入框中：

`/`: 快速设置上下文选项。

`@`: 快速引入如文档 (`@doc`) 或已打开的文件等。

`#`: 快速搜索并引入项目中的文件 (`@file`)。

`@/`: 快速搜索并引入项目中的文件夹。

**Tips: 上面的快捷键在空白聊天框可以直接使用，但是如果已经输入文案，需要前面加个空格，如果是复制粘贴过来的信息需要前后都有空格才可以**

**拖拽式 添加上下文：**在目录中直接拖拽目标文件，拖进对话框即可

**预先沟通**: 对于复杂任务，先让 AI 复述一遍你的需求，确认理解无误后再让它开始执行，避免方向错误。

![image.png](../img/Cursor入门与实践/img/image_19.png)

**关注边界**: 在 AI 生成代码后，注意检查是否考虑了边界情况、错误处理以及对现有代码的影响范围。

建议在Rules中添加全局规则

![image.png](../img/Cursor入门与实践/img/image_20.png)

**Git Commit Message**: 让 AI 基于暂存区的代码变更自动生成规范的 Git Commit Message。

![image.png](../img/Cursor入门与实践/img/image_21.png)

最好可以结合 Cursor Rules 一起使用：

![image.png](../img/Cursor入门与实践/img/image_22.png)

**自动化执行配置**

启用自动运行模式，不需要每次调用再手动确认，比如需要执行命令或者MCP调用

设置路径：Features > Enable auto-run mode

![image.png](../img/Cursor入门与实践/img/image_23.png)

**任务完成通知**: 在设置中开启任务完成声音提示，方便异步等待 AI 处理结果。

![image.png](../img/Cursor入门与实践/img/image_24.png)

### 11.2 提示词编写模版

模糊的提示词也是AI乱写的一大痛点之一，可以通过优化提示词尽量避免

一个好的 Cursor 提示词通常包含三个部分：`目标说明` + `上下文信息` + `具体要求`。

#### 11.2.1 代码生成模板

```plaintext
用[编程语言]创建[功能描述]，要求：
1. [功能要点1]
2. [功能要点2]
3. [功能要点3]
风格参考：[项目中已有的文件路径]
```

 开发立即注册页面

```plaintext
用Vue创建一个立即注册页面，要求：
1. 使用 Vue 语法
2. 在登录页面点击立即注册之后可以跳转到该页面
3. 页面 UI 风格和登录页面保持一致
4. 预留 API 调用逻辑，便于后续实现
风格参考：项目中已有的 components/login.vue
```

#### 11.2.2 功能扩展模板

```plaintext
基于现有代码：
[粘贴现有代码]
添加[新功能描述]功能，需要与现有代码风格保持一致
```

在现有代码中添加功能

```plaintext
基于现有代码：
参考@引用的文件
添加如下功能：
1. 该页面当前只支持邮箱地址登录，加上手机号码登录
2. 两种登录方式，可以快速切换
3. 手机号登录不需要密码，通过获取验证码登录
4. 手机号码需要进行校验，暂时支持+86中国区，11 位数字
需要与现有代码风格保持一致
```

#### 11.2.3 代码重构模板

```plaintext
重构以下代码，提高其[性能/可读性/可维护性]：
[粘贴需要重构的代码]
重点改进：
1. [改进点1]
2. [改进点2]
但保持原有的功能不变
```

代码重构

```plaintext
重构以下代码，提高页面的 UI 设计：
参考@引用的代码片段或者文件
重点改进：
1. 设计一个美观的背景图，采用渐变色
2. 登录界面加入一个平台名称，如：理财控台，同时在这个名称前面生成一个图标
但保持原有的功能不变
```

### 常见错误与避免方法

|  错误类型  |  示例  |  改进方法  |
| --- | --- | --- |
|  过于宽泛  |  写个好看的UI  |  使用 Element UI创建数据表格，支持排序和分页  |
|  隐含假设  |  修复登录问题  |  修复登录表单提交后出现的401错误，详细错误日志：...  |
|  术语混淆  |  做个响应式的程序  |  创建在移动端和桌面端都能良好显示的 Vue 组件  |

## 12. 项目示例

### 控台需求

背景：

需要新增一个特殊理财产品管理页面

![原型图片.png](../img/Cursor入门与实践/img/image_25.png)

#### 具体实现

提示词

![image.png](../img/Cursor入门与实践/img/image_26.png)

结果页面

![image.png](../img/Cursor入门与实践/img/image_27.png)

### 流程图优化

背景：理财商城跳转美市双录对接断点改造

需要再原有的流程中增加修改节点信息

![image.png](../img/Cursor入门与实践/img/image_28.png)

提示词：

![image.png](../img/Cursor入门与实践/img/image_29.png)

结果：

![双录优化流程图.png](../img/Cursor入门与实践/img/image_30.png)


## 总结

使用下来，Cursor确实提效很多，但是同时也存在很多不足，还待完善。

总之，在Cursor的加持下，提升开发体验的同时又能提升生产力，可以让大家有更充沛的精力聚焦在更有创造性的工作和个人成长上。

最后也祝愿大家，可以享受AI编程的乐趣。
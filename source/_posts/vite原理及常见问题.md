---
title: vite原理及常见问题
categories: 前端开发
tags:
  - js
  - vite
  - webpack
  - 面试题
date: 2025-12-28 11:00:00
---

## Vite简介

Vite（法语意为"快速的"）是一种新型前端构建工具，由Vue.js作者尤雨溪开发。它能够显著提升前端开发体验，主要体现在：

- **极速的服务启动**：使用原生ESM，无需打包即可启动
- **轻量快速的热重载**：无论应用规模多大，HMR始终快速
- **真正的按需编译**：不再等待整个应用编译完成
- **开箱即用**：对TypeScript、JSX、CSS等提供一流支持

## Vite vs Webpack 核心差异

### 开发模式对比

#### Webpack开发模式

```
启动开发服务器
      ↓
  分析所有模块
      ↓
   打包所有代码
      ↓
  编译生成bundle
      ↓
   启动开发服务器
      ↓
  页面可以访问了
（耗时：通常几十秒甚至几分钟）
```

#### Vite开发模式

```
  启动开发服务器
      ↓
   页面可以访问了！
（耗时：通常几百毫秒）
      ↓
  按需编译导入的模块
```

### 核心区别总结

| 特性 | Webpack | Vite |
|------|---------|------|
| **启动速度** | 慢（需要打包全部代码） | 快（无需打包） |
| **热更新速度** | 随项目变大而变慢 | 始终快速 |
| **开发模式** | Bundle based | ESM based |
| **生产构建** | 自己打包 | 使用Rollup |
| **配置复杂度** | 较复杂 | 简单 |
| **插件生态** | 非常丰富 | 快速增长 |
| **浏览器兼容** | 很好 | 现代浏览器 |
| **成熟度** | 非常成熟 | 相对较新 |

## Vite核心原理

### 1. 基于ESM的Dev Server

Vite利用浏览器原生支持的ES Module，在开发环境下不需要打包，直接让浏览器加载模块。

```javascript
// 传统方式（webpack）：需要将所有代码打包成bundle
// 开发服务器启动前：
import Vue from 'vue'
import App from './App.vue'
// webpack会打包成 bundle.js

// Vite方式：直接使用ESM
// 浏览器直接请求：
import { createApp } from '/node_modules/.vite/deps/vue.js'
import App from '/src/App.vue'
```

**工作流程：**

```javascript
// 1. 浏览器请求模块
GET /src/main.js

// 2. Vite拦截请求，返回转换后的代码
import { createApp } from '/node_modules/.vite/deps/vue.js'
import App from '/src/App.vue?import'

// 3. 浏览器继续请求依赖
GET /node_modules/.vite/deps/vue.js
GET /src/App.vue?import

// 4. Vite即时编译并返回
```

### 2. 依赖预构建（Pre-bundling）

Vite会在首次启动时对依赖进行预构建，主要有两个目的：

#### 目的一：兼容CommonJS和UMD

```javascript
// 很多npm包仍使用CommonJS
const express = require('express')

// Vite使用esbuild将其转换为ESM
import express from 'express'
```

#### 目的二：性能优化

```javascript
// lodash-es有600+个模块
import { debounce } from 'lodash-es'

// 预构建后打包成一个模块，减少HTTP请求
// 从600+个请求 → 1个请求
```

**预构建配置：**

```javascript
// vite.config.js
export default {
  optimizeDeps: {
    // 指定需要预构建的依赖
    include: ['vue', 'axios'],
    // 排除某些依赖
    exclude: ['your-local-package'],
    // 自定义esbuild选项
    esbuildOptions: {
      plugins: []
    }
  }
}
```

### 3. 模块热更新（HMR）

Vite的HMR基于ESM，通过WebSocket实现精确的模块更新。

```javascript
// HMR工作原理
// 1. 文件系统监听
chokidar.watch('src/**/*.{js,vue}').on('change', (file) => {
  // 2. 分析模块依赖图
  const affectedModules = getAffectedModules(file)
  
  // 3. 通过WebSocket通知客户端
  wss.send({
    type: 'update',
    updates: affectedModules.map(m => ({
      type: m.type,
      path: m.path,
      timestamp: Date.now()
    }))
  })
})

// 4. 客户端接收更新
socket.addEventListener('message', async ({ data }) => {
  const payload = JSON.parse(data)
  if (payload.type === 'update') {
    payload.updates.forEach(update => {
      // 5. 重新import更新的模块
      import(`${update.path}?t=${update.timestamp}`)
    })
  }
})
```

**HMR API使用：**

```javascript
// 在模块中使用HMR API
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    // 模块自更新
    console.log('模块已更新:', newModule)
  })
  
  // 接受依赖更新
  import.meta.hot.accept('./dep.js', (newDep) => {
    // 依赖更新时的处理逻辑
  })
  
  // 模块即将被替换时的清理逻辑
  import.meta.hot.dispose((data) => {
    // 清理副作用
  })
  
  // 自定义事件
  import.meta.hot.on('custom-event', (data) => {
    console.log('收到自定义事件:', data)
  })
}
```

### 4. 按需编译

Vite只编译浏览器实际请求的模块，而不是提前编译所有模块。

```javascript
// 路由懒加载场景
const routes = [
  {
    path: '/home',
    component: () => import('./views/Home.vue') // 只在访问时编译
  },
  {
    path: '/about',
    component: () => import('./views/About.vue')
  }
]

// webpack：构建时会生成 home.chunk.js 和 about.chunk.js
// vite开发模式：访问/home时才编译Home.vue，访问/about时才编译About.vue
```

### 5. 文件处理

#### CSS处理

```javascript
// Vite自动处理CSS
import './style.css' // 自动注入<style>标签

// CSS Modules
import styles from './style.module.css'
console.log(styles.className)

// CSS预处理器（安装对应依赖即可）
import './style.scss'
import './style.less'

// PostCSS（自动读取postcss.config.js）
```

#### 静态资源处理

```javascript
// 导入资源会返回解析后的URL
import imgUrl from './img.png'
console.log(imgUrl) // /src/img.png

// 显式URL导入
import imgUrl from './img.png?url'

// 导入为字符串
import imgContent from './shader.glsl?raw'

// 导入为Worker
import Worker from './worker.js?worker'
```

#### JSON处理

```javascript
// 导入整个JSON
import json from './data.json'

// 命名导入（支持tree-shaking）
import { field } from './data.json'
```

### 6. 生产构建

Vite使用Rollup进行生产构建，充分利用Rollup优秀的tree-shaking和代码分割能力。

```javascript
// vite.config.js
export default {
  build: {
    // 指定输出目录
    outDir: 'dist',
    
    // 指定静态资源目录
    assetsDir: 'assets',
    
    // 小于此阈值的导入资源会被内联为base64
    assetsInlineLimit: 4096,
    
    // 是否生成source map
    sourcemap: false,
    
    // Rollup配置
    rollupOptions: {
      input: {
        main: './index.html',
        admin: './admin.html'
      },
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router'],
          'ui': ['element-plus']
        }
      }
    },
    
    // 启用/禁用CSS代码拆分
    cssCodeSplit: true,
    
    // chunk大小警告限制
    chunkSizeWarningLimit: 500,
    
    // 自定义底层的Rollup打包配置
    minify: 'terser', // 'terser' | 'esbuild'
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
}
```

## Vite配置详解

### 基础配置

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  // 项目根目录
  root: process.cwd(),
  
  // 开发服务器配置
  server: {
    host: '0.0.0.0',
    port: 3000,
    open: true, // 自动打开浏览器
    cors: true, // 允许跨域
    
    // 代理配置
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },
    
    // 预热常用文件
    warmup: {
      clientFiles: ['./src/components/*.vue']
    }
  },
  
  // 路径别名
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components')
    },
    // 导入时想要省略的扩展名列表
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
  },
  
  // 插件
  plugins: [
    vue()
  ],
  
  // CSS配置
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    },
    modules: {
      localsConvention: 'camelCase'
    }
  },
  
  // 环境变量
  envPrefix: 'VITE_', // 自定义env变量前缀
  
  // 构建配置
  build: {
    target: 'es2015',
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser'
  }
})
```

### 多环境配置

```javascript
// vite.config.js
import { defineConfig } from 'vite'

export default defineConfig(({ command, mode }) => {
  // command: 'serve' | 'build'
  // mode: 'development' | 'production' | 自定义
  
  if (command === 'serve') {
    // 开发环境配置
    return {
      server: {
        port: 3000
      }
    }
  } else {
    // 生产环境配置
    return {
      build: {
        minify: 'terser',
        rollupOptions: {
          // 生产环境特定配置
        }
      }
    }
  }
})
```

## Vite插件开发

### 插件结构

```javascript
// my-vite-plugin.js
export default function myVitePlugin(options = {}) {
  return {
    // 插件名称
    name: 'my-vite-plugin',
    
    // 应用模式：'serve' | 'build' | undefined
    apply: 'build',
    
    // 插件执行顺序：'pre' | 'normal' | 'post'
    enforce: 'pre',
    
    // Vite特有钩子：服务器启动时调用
    configResolved(config) {
      console.log('配置已解析:', config)
    },
    
    // Vite特有钩子：配置开发服务器
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // 自定义中间件
        if (req.url === '/custom') {
          res.end('Custom response')
        } else {
          next()
        }
      })
    },
    
    // Vite特有钩子：转换index.html
    transformIndexHtml(html) {
      return html.replace(
        /<title>(.*?)<\/title>/,
        '<title>My App</title>'
      )
    },
    
    // Vite特有钩子：处理HMR更新
    handleHotUpdate({ file, server }) {
      if (file.endsWith('.custom')) {
        console.log('自定义文件更新:', file)
        // 通知客户端刷新
        server.ws.send({
          type: 'full-reload',
          path: '*'
        })
      }
    },
    
    // Rollup钩子：解析模块ID
    resolveId(source) {
      if (source === 'virtual-module') {
        return source // 返回null以传递给其他解析器
      }
    },
    
    // Rollup钩子：加载模块
    load(id) {
      if (id === 'virtual-module') {
        return 'export default "This is virtual!"'
      }
    },
    
    // Rollup钩子：转换模块
    transform(code, id) {
      if (id.endsWith('.custom')) {
        // 转换代码
        return {
          code: transformCode(code),
          map: null // source map
        }
      }
    }
  }
}

// 使用插件
// vite.config.js
import myVitePlugin from './my-vite-plugin'

export default {
  plugins: [
    myVitePlugin({
      // 选项
    })
  ]
}
```

### 常用插件示例

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import legacy from '@vitejs/plugin-legacy'
import { visualizer } from 'rollup-plugin-visualizer'
import compression from 'vite-plugin-compression'

export default defineConfig({
  plugins: [
    // Vue 3支持
    vue(),
    
    // Vue JSX支持
    vueJsx(),
    
    // 传统浏览器支持
    legacy({
      targets: ['defaults', 'not IE 11']
    }),
    
    // 打包分析
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true
    }),
    
    // Gzip压缩
    compression({
      algorithm: 'gzip',
      ext: '.gz'
    })
  ]
})
```

## 面试高频问题

### 1. Vite为什么这么快？

**核心原因：**

1. **开发模式使用ESM**
   - 无需打包，直接利用浏览器的ESM加载能力
   - 按需编译，只编译当前页面实际导入的模块
   - 服务器启动时间与项目规模无关

2. **使用Esbuild预构建依赖**
   - Esbuild用Go编写，比JS快10-100倍
   - 预构建只在依赖变化时重新执行
   - 使用强缓存提升二次启动速度

3. **高效的HMR**
   - 基于ESM的HMR，只需让浏览器重新请求该模块即可
   - 利用浏览器缓存，未修改的模块使用304
   - 精确的模块失效，只更新变化的模块

4. **合理的HTTP缓存策略**
   ```javascript
   // 源码模块（频繁变动）
   Cache-Control: no-cache
   
   // 预构建依赖（很少变动）
   Cache-Control: max-age=31536000, immutable
   ```

**性能对比：**

```javascript
// 大型项目（1000+模块）
Webpack开发服务器启动: 30-60秒
Vite开发服务器启动: 1-2秒

Webpack HMR更新: 2-5秒
Vite HMR更新: 100-300毫秒
```

### 2. Vite的依赖预构建是如何工作的？

```javascript
// 预构建流程
export async function prebundle() {
  // 1. 扫描入口文件，收集依赖
  const deps = await scanImports(['index.html'])
  
  // 2. 使用esbuild打包依赖
  await esbuild.build({
    entryPoints: deps,
    bundle: true,
    format: 'esm',
    outdir: 'node_modules/.vite/deps',
    plugins: [
      // 处理CommonJS
      // 处理外部依赖
    ]
  })
  
  // 3. 生成元数据文件
  writeFileSync(
    'node_modules/.vite/deps/_metadata.json',
    JSON.stringify({
      hash: getDepHash(),
      optimized: deps
    })
  )
}

// 预构建触发时机
// 1. 首次启动
// 2. package.json/lock文件变化
// 3. vite.config.js的optimizeDeps配置变化
// 4. 强制重新构建（--force参数）
```

**预构建配置优化：**

```javascript
export default {
  optimizeDeps: {
    // 方式1：手动指定需要预构建的依赖
    include: [
      'axios',
      'lodash-es',
      'vue',
      // 深层依赖
      '@ant-design/icons-vue/lib/icons/LoadingOutlined'
    ],
    
    // 方式2：排除不需要预构建的
    exclude: [
      'your-local-package'
    ],
    
    // 方式3：为特定依赖指定esbuild选项
    esbuildOptions: {
      plugins: [
        // 自定义插件
      ]
    }
  }
}
```

### 3. Vite如何处理CSS？

```javascript
// 1. 普通CSS - 自动注入<style>标签
import './style.css'

// 实际处理流程：
// a. Vite读取CSS文件
// b. 通过PostCSS处理（如果配置了）
// c. 返回JS代码，在运行时注入<style>标签
export default `
  const style = document.createElement('style')
  style.textContent = '${cssContent}'
  document.head.appendChild(style)
`

// 2. CSS Modules - 返回类名映射对象
import styles from './style.module.css'

// 实际处理：
// a. 通过postcss-modules处理
// b. 生成哈希类名
// c. 返回映射对象
export default {
  'btn': '_btn_x7k9s_1',
  'btn-primary': '_btn-primary_x7k9s_5'
}

// 3. CSS预处理器 - 自动编译
import './style.scss'

// 实际处理：
// a. 使用sass编译成CSS
// b. 后续处理同普通CSS

// 4. 生产构建 - 提取为单独的CSS文件
// 使用Rollup插件提取CSS到单独文件
// 并在HTML中自动注入<link>标签
```

**CSS配置：**

```javascript
export default {
  css: {
    // PostCSS配置
    postcss: {
      plugins: [
        require('autoprefixer'),
        require('tailwindcss')
      ]
    },
    
    // 预处理器配置
    preprocessorOptions: {
      scss: {
        // 全局导入
        additionalData: `
          @import "@/styles/variables.scss";
          @import "@/styles/mixins.scss";
        `,
        // Dart Sass选项
        api: 'modern'
      },
      less: {
        modifyVars: {
          'primary-color': '#1DA57A'
        },
        javascriptEnabled: true
      }
    },
    
    // CSS Modules配置
    modules: {
      // 类名生成规则
      generateScopedName: '[name]__[local]___[hash:base64:5]',
      
      // 驼峰化类名
      localsConvention: 'camelCaseOnly'
    },
    
    // 开发时是否提取CSS
    devSourcemap: true
  }
}
```

### 4. Vite的HMR实现原理

```javascript
// 服务端实现
class ViteDevServer {
  constructor() {
    this.ws = new WebSocketServer()
    this.moduleGraph = new ModuleGraph()
    this.watcher = chokidar.watch('src')
    
    this.watcher.on('change', async (file) => {
      // 1. 使模块失效
      const module = this.moduleGraph.getModuleById(file)
      this.moduleGraph.invalidateModule(module)
      
      // 2. 分析影响范围
      const affectedModules = this.getAffectedModules(module)
      
      // 3. 通知客户端更新
      this.ws.send({
        type: 'update',
        updates: affectedModules.map(m => ({
          type: m.type, // 'js-update' | 'css-update' | 'full-reload'
          path: m.url,
          acceptedPath: m.acceptedPath,
          timestamp: Date.now()
        }))
      })
    })
  }
  
  getAffectedModules(module) {
    // 向上查找接受HMR的模块边界
    const boundaries = new Set()
    const visited = new Set()
    
    const traverse = (mod) => {
      if (visited.has(mod)) return
      visited.add(mod)
      
      // 如果模块接受自身更新
      if (mod.isSelfAccepting) {
        boundaries.add(mod)
        return
      }
      
      // 如果没有导入者，需要全量刷新
      if (mod.importers.size === 0) {
        boundaries.add({ type: 'full-reload' })
        return
      }
      
      // 继续向上查找
      mod.importers.forEach(importer => traverse(importer))
    }
    
    traverse(module)
    return Array.from(boundaries)
  }
}

// 客户端实现
class HMRClient {
  constructor() {
    this.socket = new WebSocket('ws://localhost:3000')
    
    this.socket.addEventListener('message', async ({ data }) => {
      const payload = JSON.parse(data)
      
      switch (payload.type) {
        case 'update':
          payload.updates.forEach(update => {
            if (update.type === 'js-update') {
              this.handleJSReload(update)
            } else if (update.type === 'css-update') {
              this.handleCSSReload(update)
            }
          })
          break
          
        case 'full-reload':
          location.reload()
          break
      }
    })
  }
  
  async handleJSReload({ path, timestamp }) {
    // 1. 获取模块的热更新回调
    const module = this.hotModulesMap.get(path)
    
    // 2. 执行dispose回调（清理）
    module?.dispose?.()
    
    // 3. 动态导入新模块
    const newModule = await import(`${path}?t=${timestamp}`)
    
    // 4. 执行accept回调
    module?.accept?.(newModule)
    
    // 5. 更新模块缓存
    this.hotModulesMap.set(path, newModule)
  }
  
  handleCSSReload({ path, timestamp }) {
    // CSS更新更简单：直接替换<link>标签
    const link = document.querySelector(`link[href*="${path}"]`)
    const newLink = link.cloneNode()
    newLink.href = `${path}?t=${timestamp}`
    newLink.onload = () => link.remove()
    link.after(newLink)
  }
}

// 模块中使用HMR API
if (import.meta.hot) {
  // 接受自身更新
  import.meta.hot.accept((newModule) => {
    // 用新模块替换旧模块
    app.update(newModule.default)
  })
  
  // 接受依赖更新
  import.meta.hot.accept('./dep.js', (newDep) => {
    // 依赖更新时的处理
  })
  
  // 清理副作用
  import.meta.hot.dispose((data) => {
    // 保存状态
    data.state = app.getState()
    // 清理事件监听等
    app.cleanup()
  })
  
  // 使用之前保存的状态
  if (import.meta.hot.data.state) {
    app.setState(import.meta.hot.data.state)
  }
}
```

### 5. Vite如何处理环境变量？

```javascript
// .env 文件
VITE_APP_TITLE=My App
VITE_API_URL=https://api.example.com
DB_PASSWORD=secret123  // 不会暴露到客户端

// .env.development
VITE_API_URL=http://localhost:3000

// .env.production
VITE_API_URL=https://api.production.com

// 在代码中使用
console.log(import.meta.env.VITE_APP_TITLE)
console.log(import.meta.env.VITE_API_URL)
console.log(import.meta.env.MODE) // 'development' | 'production'
console.log(import.meta.env.DEV)  // boolean
console.log(import.meta.env.PROD) // boolean

// TypeScript类型支持
// env.d.ts
interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_API_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

**实现原理：**

```javascript
// Vite在构建时会替换环境变量
// 源码：
console.log(import.meta.env.VITE_API_URL)

// 转换后：
console.log("https://api.example.com")

// define配置（类似webpack.DefinePlugin）
export default {
  define: {
    __APP_VERSION__: JSON.stringify('1.0.0'),
    'import.meta.env.CUSTOM': JSON.stringify('custom value')
  }
}
```

### 6. Vite的生产构建优化

```javascript
export default {
  build: {
    // 1. 目标浏览器
    target: 'es2015', // 或 ['es2015', 'chrome58', 'edge16']
    
    // 2. 压缩选项
    minify: 'terser', // 或 'esbuild'
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log'] // 移除特定函数调用
      }
    },
    
    // 3. CSS代码拆分
    cssCodeSplit: true, // 每个异步chunk都生成独立的CSS文件
    
    // 4. 静态资源内联阈值
    assetsInlineLimit: 4096, // 小于4kb的资源内联为base64
    
    // 5. chunk大小警告
    chunkSizeWarningLimit: 500, // kb
    
    // 6. Rollup配置
    rollupOptions: {
      output: {
        // 手动分包
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'ui-vendor': ['element-plus', '@element-plus/icons-vue'],
          'utils': ['axios', 'dayjs']
        },
        
        // 或使用函数形式
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // 第三方库按包名分割
            return id.toString().split('node_modules/')[1].split('/')[0]
          }
        },
        
        // 文件命名
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    },
    
    // 7. 启用/禁用brotli压缩
    brotliSize: false,
    
    // 8. watch模式
    watch: null,
    
    // 9. 清空输出目录
    emptyOutDir: true
  }
}
```

**代码分割策略：**

```javascript
// 1. 动态导入
const Home = () => import('./views/Home.vue')

// 2. 使用魔术注释
const About = () => import(
  /* webpackChunkName: "about" */
  /* webpackPrefetch: true */
  './views/About.vue'
)

// 3. 配置预加载
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // 核心依赖
          'framework': ['vue', 'vue-router', 'pinia'],
          
          // UI组件库
          'ui-lib': ['element-plus'],
          
          // 工具库
          'vendor': ['axios', 'dayjs', 'lodash-es'],
          
          // 图表库（按需加载）
          'charts': ['echarts']
        }
      }
    }
  }
}
```

### 7. Vite vs Webpack 详细对比

#### 开发体验对比

| 方面 | Webpack | Vite |
|------|---------|------|
| **启动速度** | 慢，需要完整打包 | 快，秒级启动 |
| **HMR速度** | 随项目增大变慢 | 始终快速 |
| **配置复杂度** | 较复杂 | 简单直观 |
| **调试体验** | 需配置source map | 原生ESM，直观 |
| **TypeScript支持** | 需loader | 内置支持 |

#### 生产构建对比

```javascript
// Webpack配置（简化版）
module.exports = {
  mode: 'production',
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js'
  },
  module: {
    rules: [
      { test: /\.js$/, use: 'babel-loader' },
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
      { test: /\.vue$/, use: 'vue-loader' }
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin(),
    new MiniCssExtractPlugin()
  ],
  optimization: {
    splitChunks: { chunks: 'all' }
  }
}

// Vite配置（简化版）
export default {
  plugins: [vue()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue']
        }
      }
    }
  }
}
// CSS、TypeScript等开箱即用，无需额外配置
```

#### 适用场景对比

**选择Webpack的场景：**
- 需要极致的兼容性（IE11等老旧浏览器）
- 已有大量Webpack配置和插件的老项目
- 需要使用Webpack独有的特性（如Module Federation）
- 团队对Webpack非常熟悉

**选择Vite的场景：**
- 新项目开发
- 注重开发体验和构建速度
- 主要面向现代浏览器（ES2015+）
- 使用Vue 3、React、Svelte等现代框架
- 需要快速迭代的中小型项目

### 8. Vite的浏览器兼容性处理

```javascript
// 1. 使用@vitejs/plugin-legacy
import legacy from '@vitejs/plugin-legacy'

export default {
  plugins: [
    legacy({
      // 目标浏览器
      targets: ['defaults', 'not IE 11'],
      
      // 是否为支持原生ESM的浏览器提供polyfill
      modernPolyfills: true,
      
      // 渲染legacy chunks
      renderLegacyChunks: true,
      
      // 额外的polyfills
      additionalLegacyPolyfills: ['regenerator-runtime/runtime']
    })
  ],
  
  build: {
    // 需要设置target
    target: ['es2015', 'edge79', 'firefox67', 'chrome63', 'safari11.1']
  }
}

// 2. 构建结果
// index.html会包含两套bundle：
<script type="module" src="/assets/index.js"></script>
<script nomodule src="/assets/index-legacy.js"></script>

// 支持ESM的浏览器加载现代bundle
// 不支持的浏览器加载legacy bundle（包含polyfill）
```

### 9. Vite常见问题及解决方案

#### 问题1：开发环境正常，生产环境报错

```javascript
// 原因：开发环境使用ESM，生产环境使用Rollup打包
// 可能的原因：
// 1. 循环依赖
// 2. 副作用代码被tree-shaking
// 3. 路径别名未正确配置

// 解决方案1：检查循环依赖
// 使用vite-plugin-circular-dependency
import circularDependency from 'vite-plugin-circular-dependency'

export default {
  plugins: [
    circularDependency({
      // 排除某些目录
      exclude: /node_modules/,
      // 发现循环依赖时的行为
      onDetected({ paths, cycle }) {
        console.warn('检测到循环依赖:', cycle)
      }
    })
  ]
}

// 解决方案2：标记副作用文件
// package.json
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "./src/utils/register.js"
  ]
}

// 解决方案3：确保路径别名一致
export default {
  resolve: {
    alias: {
      '@': '/src'
    }
  }
}
```

#### 问题2：import.meta.glob不生效

```javascript
// ❌ 错误用法：动态路径
const modules = import.meta.glob(`./modules/${variable}/*.js`)

// ✅ 正确用法：静态路径
const modules = import.meta.glob('./modules/**/*.js')

// 使用示例
const modules = import.meta.glob('./modules/*.js')
// {
//   './modules/a.js': () => import('./modules/a.js'),
//   './modules/b.js': () => import('./modules/b.js')
// }

// 立即导入
const modules = import.meta.glob('./modules/*.js', { eager: true })
// {
//   './modules/a.js': { default: ... },
//   './modules/b.js': { default: ... }
// }

// 导入特定导出
const modules = import.meta.glob('./modules/*.js', { 
  import: 'setup',
  eager: true 
})
```

#### 问题3：第三方库报错

```javascript
// 问题：某些CommonJS包无法正常工作
// 解决方案1：添加到optimizeDeps.include
export default {
  optimizeDeps: {
    include: ['problematic-package']
  }
}

// 解决方案2：使用esbuild配置
export default {
  optimizeDeps: {
    esbuildOptions: {
      plugins: [
        // 自定义esbuild插件
      ]
    }
  }
}

// 解决方案3：排除预构建，使用原始文件
export default {
  optimizeDeps: {
    exclude: ['problematic-package']
  },
  ssr: {
    noExternal: ['problematic-package']
  }
}
```

#### 问题4：样式加载顺序问题

```javascript
// 问题：开发环境和生产环境样式顺序不一致
// 解决方案：明确导入顺序

// main.js - 确保基础样式最先导入
import './styles/reset.css'      // 1. 重置样式
import './styles/variables.css'  // 2. 变量
import './styles/global.css'     // 3. 全局样式
import App from './App.vue'      // 4. 组件样式

// 或使用CSS的@import（不推荐，性能较差）
// global.css
@import './reset.css';
@import './variables.css';
```

### 10. Vite性能优化最佳实践

```javascript
export default {
  // 1. 优化依赖预构建
  optimizeDeps: {
    // 提前预构建大型依赖
    include: [
      'vue',
      'vue-router',
      'pinia',
      'axios',
      'element-plus'
    ],
    // 排除无需预构建的包
    exclude: ['local-package']
  },
  
  // 2. 合理配置服务器
  server: {
    // 文件系统缓存
    fs: {
      // 限制访问范围
      strict: true,
      allow: ['.']
    },
    // 预热常用文件
    warmup: {
      clientFiles: [
        './src/components/Common/**/*.vue',
        './src/layouts/**/*.vue'
      ]
    }
  },
  
  // 3. 构建优化
  build: {
    // 提取CSS
    cssCodeSplit: true,
    
    // 合理的chunk拆分
    rollupOptions: {
      output: {
        manualChunks(id) {
          // 按npm包分割
          if (id.includes('node_modules')) {
            const name = id.split('node_modules/')[1].split('/')[0]
            
            // 大型库单独拆分
            if (['echarts', 'lodash-es'].includes(name)) {
              return name
            }
            
            // 其他第三方库合并
            return 'vendor'
          }
        }
      }
    },
    
    // 使用esbuild压缩（更快）
    minify: 'esbuild',
    
    // 禁用brotli计算（加快构建）
    brotliSize: false
  }
}
```

**代码层面优化：**

```javascript
// 1. 路由懒加载
const routes = [
  {
    path: '/heavy-component',
    component: () => import('./views/HeavyComponent.vue')
  }
]

// 2. 使用import.meta.glob实现自动导入
const views = import.meta.glob('./views/**/*.vue')

// 3. 避免在开发环境导入大型库
if (import.meta.env.PROD) {
  // 生产环境才导入
  import('./analytics')
}

// 4. 合理使用动态导入
// ❌ 不好：同步导入大型库
import * as echarts from 'echarts'

// ✅ 好：按需异步导入
const loadChart = async () => {
  const echarts = await import('echarts')
  return echarts.init(dom)
}
```

## Vite迁移指南（从Webpack迁移）

### 1. 更新package.json

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-vue": "^5.0.0"
  }
}
```

### 2. 创建vite.config.js

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  
  resolve: {
    // webpack的alias → vite的alias
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '~': path.resolve(__dirname, 'src')
    }
  },
  
  server: {
    // webpack-dev-server的proxy → vite的proxy
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  },
  
  // webpack的DefinePlugin → vite的define
  define: {
    'process.env': {}
  }
})
```

### 3. 修改index.html

```html
<!-- Webpack -->
<div id="app"></div>
<!-- script会由html-webpack-plugin自动注入 -->

<!-- Vite -->
<div id="app"></div>
<script type="module" src="/src/main.js"></script>
<!-- 需要手动添加入口脚本 -->
```

### 4. 更新环境变量

```javascript
// Webpack
console.log(process.env.VUE_APP_API_URL)

// Vite
console.log(import.meta.env.VITE_API_URL)

// .env文件也需要修改前缀
// VUE_APP_API_URL → VITE_API_URL
```

### 5. 处理require

```javascript
// ❌ Webpack的require（Vite不支持）
const module = require('./module.js')
const imgSrc = require('@/assets/logo.png')

// ✅ 改用ES Module的import
import module from './module.js'
import imgSrc from '@/assets/logo.png'

// 动态require改为动态import
// ❌
const module = require(`./modules/${name}.js`)

// ✅
const module = await import(`./modules/${name}.js`)
```

### 6. 处理静态资源

```javascript
// Webpack
import imgUrl from './img.png'
// 需要file-loader或url-loader

// Vite
import imgUrl from './img.png'
// 自动处理，返回处理后的URL

// public目录
// Webpack: public/img.png → /img.png
// Vite: public/img.png → /img.png
// （这点是一样的）
```

## 总结

### Vite的核心优势
1. **极快的开发启动**：利用ESM实现秒级启动
2. **快速的HMR**：精确的模块更新，始终保持快速
3. **简单的配置**：合理的默认配置，开箱即用
4. **现代化工具链**：Esbuild + Rollup，性能强大
5. **优秀的插件生态**：快速增长的插件生态系统

### 适合的场景
- ✅ 新项目开发
- ✅ 现代浏览器应用
- ✅ Vue 3 / React / Svelte项目
- ✅ 注重开发体验的团队
- ✅ 中小型到大型应用

### 不适合的场景
- ❌ 需要支持IE11的项目（虽然有legacy插件，但体验不如Webpack）
- ❌ 依赖大量Webpack特定功能的老项目
- ❌ 需要极致定制化构建的场景

### 核心面试要点记忆
1. **为什么快**：开发用ESM + Esbuild预构建 + 按需编译
2. **HMR原理**：WebSocket + ESM重新请求 + 精确失效
3. **预构建**：Esbuild打包依赖 + 减少HTTP请求
4. **与Webpack对比**：开发模式根本不同（ESM vs Bundle）
5. **生产构建**：Rollup打包，tree-shaking和代码分割优秀


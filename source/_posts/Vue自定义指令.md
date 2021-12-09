---
title: Vue自定义指令
categories: 前端开发
tags: - js
- vue.js
date: 2021-12-09 15:41:02
---

> vue.js中除了常用的v-model 和 v-if 这种常用的指令外，有一些需求还是需要自定义指令的，首先还是先放上官网[介绍](https://v3.cn.vuejs.org/api/application-api.html#directive)

## 权限控制的自定义指令
自定义指令
```
  // 页面权限点
  permission: {
    inserted(el, binding, vnode) {
      const { arg } = binding;
      const {
        context: {
          $route: { name },
          $store: { state }
        }
      } = vnode;
      const handler = () => {
        const { authPoints } = state.app;
        if (!authPoints) return setTimeout(handler, 50);
        !(authPoints[name] || []).includes(arg) && el.parentNode.removeChild(el);
      };
      handler();
    }
  },

```
页面使用
```
<el-button type='text' v-permission:edit >编辑</el-button>
```
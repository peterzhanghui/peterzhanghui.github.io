---
title: keep-alive保持页面位置
categories: 前端开发
tags: js
date: 2025-04-02 11:40:27
---

> 在vue单页面应用中，可以通过在router 配置中添加 keepAlive 来keepAlive页面，但是这样会导致页面在切换时，页面位置会回到顶部，这样用户体验不好，所以需要保持页面位置。

## 解决方案

1. 在router配置中添加keepAlive
2. 在需要保持页面位置的组件中添加scrollTop属性
3. 在组件的activated钩子函数中获取scrollTop，并恢复滚动位置
4. 在组件的beforeRouteLeave钩子函数中设置scrollTop
## 代码示例
```js
// router配置
{
  path: '/list',
  name: 'list',
  component: List,
  meta: {
    keepAlive: true
  }     
}

// List组件
export default {
  data() {
    return {
      scrollTop: 0
    }
  },
  activated() {
    // 恢复滚动位置
    this.$nextTick(() => {
        const pages = document.querySelector('.page');
        if (pages) {
            pages.scrollTop = this.scrollTop;
        }
    });
  },
    beforeRouteLeave(to, from, next) {
        // 保留滚动位置
        this.scrollTop = document.querySelector('.page')?.scrollTop;
        next();
    },
}
```
        


---
title: vue-router简单实现
categories: [vue]
tags:
  - js
  - vue
date: 2021-04-03 16:48:34
---
> 本文为学习总结，希望对你也有帮助

实现 vue-router 插件的需求分析

- 作为一个插件存在：实现 VueRouter 类和 install 方法
- 实现两个全局组件：router-view 用于显示匹配组件内容，router-link 用于跳转
- 监控 url 变化：监听 hashchange 或 popstate 事件
- 响应最新 url：创建一个响应式的属性 current，当它改变时获取对应组件并显示

## 插件 install

为什么要用混入方式写？主要原因是 use 代码在前，Router 实例创建在后，而 install 逻辑又需要用
到该实例

```
// 插件：实现install方法，注册$router
VueRouter.install = function(_Vue) { // 引用构造函数，VueRouter中要使用
    Vue = _Vue;
    Vue.mixin({
        beforeCreate() { // 只有根组件拥有router选项
            if (this.$options.router) { // vm.$router
                Vue.prototype.$router = this.$options.router;
            }
        }
    });
};

```

## 监控 url 变化

监测 hashchange，和 load 事件，获取 hash 值。重点是使用 Vue.util.defineReactive 定义响应式属性，这样 hash 改变的时候可以触发 router-view 中的 render 函数。

```
// current应该是响应式的
Vue.util.defineReactive(this, 'current', '/')
// 定义响应式的属性current
const initial = window.location.hash.slice(1) || '/'
Vue.util.defineReactive(this, 'current', initial) // 监听hashchange事件
window.addEventListener('hashchange', this.onHashChange.bind(this)) // 需要手动绑定this，否则this会指向window
window.addEventListener('load', this.onHashChange.bind(this))


onHashChange() { this.current = window.location.hash.slice(1) }

```

## router-view 组件

```
export default {
    render(h) { // 动态获取对应组件
        let component = null;
        this.$router.$options.routes.forEach(route => {
            if (route.path === this.$router.current) {
                component = route.component }
            });
        return h(component);
    }
}

```

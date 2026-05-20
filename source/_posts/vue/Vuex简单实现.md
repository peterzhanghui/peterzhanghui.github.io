---
title: Vuex
categories: [vue]
tags: js
date: 2021-04-07 17:21:42
---
> Vuex 是专为 Vue.js 应用程序开发的状态管理模式。它采用集中式存储管理应用的所有组件的状态。Vuex 和单纯的全局对象主要有两点不同，一 Vuex 的状态存储是响应式的。你不能直接改变 store 中的状态。改变 store 中的状态的唯一途径就是显式地提交 (commit) mutation。

## Vuex 流程

在 vue 组件里面，通过 dispatch 来触发 actions 提交修改数据的操作， 然后通过 actions 的 commit 触发 mutations 来修改数据，mutations 接收到 commit 的请求，就会自动通过 mutate 来修改 state，最后由 store 触发每一个调用它的组件的更新

### vuex 的 State 特性是？

State 就是数据源的存放地 State 里面的数据是响应式的，state 中的数据改变，对应这个数据的组 件也会发生改变 State 通过 mapstate 把全局的 state 和 getters 映射到当前组件的计算 属性中

### vuex 的 Getter 特性是？

Getter 可以对 state 进行计算操作，它就是 store 的计算属性 Getter 可以在多组件之间复用 如果一个状态只在一个组件内使用，可以不用 getters 51.vuex 的 Mutation 特性是？ 更改 vuex store 中修改状态的唯一办法就是提交 mutation，可以在回 调函数中修改 store 中的状态

### vuex 的 actions 特性是？

Action 类似于 mutation，不同的是 action 提交的是 mutation，不是 直接变更状态，可以包含任意异步操作

### vuex 的优势

优点：解决了非父子组件的通信，减少了 ajax 请求次数，有些可以直接 从 state 中获取 缺点：刷新浏览器，vuex 中的 state 会重新变为初始状态，解决办法是 vuex-along，得配合计算属性和 sessionstorage 来实现

## Vuex 的持久化处理

使用 Vuex 的插件 vuex-persist [github 连接](https://github.com/championswimmer/vuex-persist#tips-for-nuxt)文中有详细教程不在赘述，主要说一下在 nuxt.js 中的配置

按照官网的教程新建 plugins 配置后，需要在配置 Vuex 的 store 文件夹 的 index.js 添加 插件配置。最终就可以实现持久化缓存了。

```
import VuexPersistence from 'vuex-persist';
export const plugins = [new VuexPersistence().plugin];
```

## nuxt.js 使用 nuxtServerInit 获取组件数据

运行在服务端，都能帮助我们在页面渲染（组件加载 ）前操作 store。当我们想将服务端的一些数据传到客户端时，这个方法是灰常好用的。

使用方法示例，具体可以结合自己业务需要处理相关数据

```
export const actions = {
    nuxtServerInit({ commit }, { req }) {
        let cookie = req.headers.cookie;
        if (cookie) {
            cookie.split(';').map(item => {
                if (item.split('=')[0].trim() === 'token') {
                    let token = item.split('=')[1];
                    commit('setToken', token);
                }
            })
        }
    },
};

```

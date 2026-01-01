---
title: Vue 2和Vue 3 的区别
categories: 前端开发
tags:
  - vue
  - vuejs
  - 面试题
date: 2025-01-27 14:00:00
---

> 从 Vue 2 升级到 Vue 3 已经有一段时间了，现在很多新项目都直接用 Vue 3 了。这篇文章主要聊聊 Vue 2 和 Vue 3 到底有啥区别，以及为什么要做这些改动。

## 为什么要升级 Vue 3？

Vue 2 其实已经很成熟了，但确实有一些问题：

1. **性能瓶颈**：随着项目变大，响应式系统会有性能问题，特别是深层嵌套的对象
2. **TypeScript 支持不够好**：Vue 2 的 TypeScript 支持比较弱，写起来很别扭
3. **代码复用困难**：Options API 在复杂组件里，逻辑分散，复用困难
4. **打包体积**：Vue 2 的代码无法 tree-shaking，即使用不到的功能也会被打包进去
5. **维护成本**：Vue 2 的源码结构复杂，新功能开发困难

所以 Vue 3 的目标就是解决这些问题，同时保持向下兼容（虽然有些破坏性改动）。

## 核心架构变化

### 1. 响应式系统重构

这是 Vue 3 最核心的变化。Vue 2 用的是 `Object.defineProperty`，Vue 3 改成了 `Proxy`。

**Vue 2 的响应式原理：**

```javascript
// Vue 2 的实现方式
function defineReactive(obj, key, val) {
  Object.defineProperty(obj, key, {
    get() {
      console.log('get', key)
      return val
    },
    set(newVal) {
      console.log('set', key, newVal)
      val = newVal
      // 触发更新
    }
  })
}

// 问题1：无法监听数组索引和长度变化
const arr = [1, 2, 3]
defineReactive(arr, '0', arr[0]) // 只能监听已有索引
arr[0] = 4 // 能触发
arr.push(4) // 无法监听
arr.length = 0 // 无法监听

// 问题2：无法监听对象属性的新增和删除
const obj = { a: 1 }
defineReactive(obj, 'a', obj.a)
obj.b = 2 // 无法监听新增属性
delete obj.a // 无法监听删除属性

// 问题3：需要递归遍历所有属性
const deepObj = {
  a: { b: { c: 1 } }
}
// 需要递归处理每一层，性能差
```

**Vue 3 的响应式原理：**

```javascript
// Vue 3 使用 Proxy
function reactive(obj) {
  return new Proxy(obj, {
    get(target, key) {
      console.log('get', key)
      return target[key]
    },
    set(target, key, value) {
      console.log('set', key, value)
      target[key] = value
      // 触发更新
      return true
    },
    deleteProperty(target, key) {
      console.log('delete', key)
      delete target[key]
      return true
    }
  })
}

// 优势1：可以监听数组所有操作
const arr = reactive([1, 2, 3])
arr.push(4) // ✅ 能监听
arr[0] = 5 // ✅ 能监听
arr.length = 0 // ✅ 能监听

// 优势2：可以监听对象属性的新增和删除
const obj = reactive({ a: 1 })
obj.b = 2 // ✅ 能监听新增
delete obj.a // ✅ 能监听删除

// 优势3：按需响应，不需要递归
const deepObj = reactive({
  a: { b: { c: 1 } }
})
// 只有访问到深层属性时才会创建 Proxy，性能更好
```

**性能对比：**

```javascript
// Vue 2：初始化时需要递归处理所有属性
const obj = {
  a: 1,
  b: { c: 2, d: { e: 3 } },
  f: [1, 2, { g: 4 }]
}
// 所有属性都会被 defineProperty 处理，即使不会用到

// Vue 3：按需响应
const obj = reactive({
  a: 1,
  b: { c: 2, d: { e: 3 } },
  f: [1, 2, { g: 4 }]
})
// 只有访问到的属性才会被 Proxy 处理
// 访问 obj.a 时，只处理 a
// 访问 obj.b.c 时，才处理 b 和 c
```

### 2. Composition API

这是 Vue 3 最大的语法变化。Vue 2 用的是 Options API，Vue 3 引入了 Composition API（但 Options API 仍然支持）。

**Vue 2 的 Options API：**

```javascript
export default {
  data() {
    return {
      count: 0,
      name: '',
      todos: []
    }
  },
  computed: {
    doubleCount() {
      return this.count * 2
    }
  },
  watch: {
    count(newVal, oldVal) {
      console.log('count changed', newVal, oldVal)
    }
  },
  methods: {
    increment() {
      this.count++
    },
    addTodo() {
      this.todos.push({ id: Date.now(), text: this.name })
      this.name = ''
    }
  },
  mounted() {
    console.log('mounted')
  }
}
```

**问题：**
- 逻辑分散：相关的逻辑（比如 count 相关的 data、computed、methods）分散在不同选项里
- 代码复用困难：想要复用逻辑，只能用 mixin，但 mixin 有命名冲突、来源不清晰等问题
- TypeScript 支持差：this 的类型推断很困难

**Vue 3 的 Composition API：**

```javascript
import { ref, computed, watch, onMounted } from 'vue'

export default {
  setup() {
    // 所有相关逻辑都在一个函数里
    const count = ref(0)
    const name = ref('')
    const todos = ref([])
    
    const doubleCount = computed(() => count.value * 2)
    
    watch(count, (newVal, oldVal) => {
      console.log('count changed', newVal, oldVal)
    })
    
    const increment = () => {
      count.value++
    }
    
    const addTodo = () => {
      todos.value.push({ id: Date.now(), text: name.value })
      name.value = ''
    }
    
    onMounted(() => {
      console.log('mounted')
    })
    
    return {
      count,
      name,
      todos,
      doubleCount,
      increment,
      addTodo
    }
  }
}
```

**更好的代码组织：**

```javascript
// 可以把相关逻辑提取到 composable 函数里
function useCounter() {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  
  const increment = () => {
    count.value++
  }
  
  return {
    count,
    doubleCount,
    increment
  }
}

function useTodos() {
  const todos = ref([])
  const name = ref('')
  
  const addTodo = () => {
    todos.value.push({ id: Date.now(), text: name.value })
    name.value = ''
  }
  
  return {
    todos,
    name,
    addTodo
  }
}

// 在组件中使用
export default {
  setup() {
    const { count, doubleCount, increment } = useCounter()
    const { todos, name, addTodo } = useTodos()
    
    return {
      count,
      doubleCount,
      increment,
      todos,
      name,
      addTodo
    }
  }
}
```

**`<script setup>` 语法糖（更简洁）：**

```javascript
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubleCount = computed(() => count.value * 2)

const increment = () => {
  count.value++
}
</script>
```

### 3. 多根节点支持

Vue 2 要求组件只能有一个根节点，Vue 3 支持多个根节点。

```vue
<!-- Vue 2：必须有一个根节点 -->
<template>
  <div>
    <header>Header</header>
    <main>Main</main>
    <footer>Footer</footer>
  </div>
</template>

<!-- Vue 3：可以有多个根节点 -->
<template>
  <header>Header</header>
  <main>Main</main>
  <footer>Footer</footer>
</template>
```

### 4. Fragment 和 Teleport

**Fragment：** 上面说的多根节点就是 Fragment，不需要额外的 DOM 节点包裹。

**Teleport：** 可以把组件渲染到 DOM 的任意位置，比如弹窗、提示框。

```vue
<template>
  <div>
    <button @click="show = true">打开弹窗</button>
    <!-- 弹窗内容渲染到 body 下 -->
    <Teleport to="body">
      <div v-if="show" class="modal">
        <p>这是弹窗内容</p>
        <button @click="show = false">关闭</button>
      </div>
    </Teleport>
  </div>
</template>
```

### 5. 生命周期变化

Vue 3 的生命周期基本和 Vue 2 一样，但有一些调整：

```javascript
// Vue 2
export default {
  beforeCreate() {},
  created() {},
  beforeMount() {},
  mounted() {},
  beforeUpdate() {},
  updated() {},
  beforeDestroy() {}, // Vue 3 改名了
  destroyed() {}      // Vue 3 改名了
}

// Vue 3 Options API（兼容 Vue 2）
export default {
  beforeCreate() {},
  created() {},
  beforeMount() {},
  mounted() {},
  beforeUpdate() {},
  updated() {},
  beforeUnmount() {}, // 改名
  unmounted() {}       // 改名
}

// Vue 3 Composition API
import { onBeforeMount, onMounted, onBeforeUpdate, onUpdated, onBeforeUnmount, onUnmounted } from 'vue'

export default {
  setup() {
    onBeforeMount(() => {})
    onMounted(() => {})
    onBeforeUpdate(() => {})
    onUpdated(() => {})
    onBeforeUnmount(() => {})
    onUnmounted(() => {})
  }
}
```

## 性能提升

### 1. 更小的打包体积

Vue 3 支持 tree-shaking，没用到的功能不会被打包。

```javascript
// Vue 2：即使只用 createApp，也会打包整个 Vue
import Vue from 'vue'
Vue.createApp({})

// Vue 3：按需导入，只打包用到的
import { createApp } from 'vue'
createApp({})

// 打包体积对比
// Vue 2: ~35KB (gzipped)
// Vue 3: ~10KB (gzipped，只导入核心功能)
```

### 2. 更快的渲染速度

Vue 3 的渲染性能比 Vue 2 快很多，主要优化点：

**PatchFlag 优化：**

```javascript
// Vue 2：需要全量 diff
// 即使只有 class 变化，也要对比所有属性

// Vue 3：使用 PatchFlag 标记动态属性
// 编译时就知道哪些属性是动态的，diff 时只对比这些
const vnode = {
  type: 'div',
  props: { class: 'foo' },
  patchFlag: 1 // 标记 class 是动态的
}
// diff 时只对比 class，不对比其他静态属性
```

**静态提升：**

```vue
<!-- Vue 2：每次渲染都创建新的 VNode -->
<template>
  <div>
    <p>静态文本</p>
    <p>静态文本</p>
    <p>{{ dynamic }}</p>
  </div>
</template>

<!-- Vue 3：静态节点提升到渲染函数外 -->
const _hoisted_1 = createVNode('p', null, '静态文本')
const _hoisted_2 = createVNode('p', null, '静态文本')

function render() {
  return [
    _hoisted_1, // 复用，不重新创建
    _hoisted_2, // 复用，不重新创建
    createVNode('p', null, dynamic) // 只有这个是动态的
  ]
}
```

**事件缓存：**

```vue
<!-- Vue 2：每次渲染都创建新的函数 -->
<button @click="handleClick">点击</button>
// 每次渲染：createVNode('button', { onClick: handleClick })

<!-- Vue 3：缓存事件处理函数 -->
<button @click="handleClick">点击</button>
// 第一次渲染：创建并缓存
// 后续渲染：复用缓存的函数
```

### 3. 更快的响应式初始化

```javascript
// Vue 2：初始化时递归处理所有属性
const obj = {
  a: 1,
  b: { c: 2, d: { e: 3 } }
}
// 所有属性都会被 defineProperty 处理

// Vue 3：按需响应
const obj = reactive({
  a: 1,
  b: { c: 2, d: { e: 3 } }
})
// 只有访问到的属性才会被 Proxy 处理
// 初始化更快，内存占用更少
```

## 原理层面的区别

### 1. 响应式系统

**Vue 2：**
- 使用 `Object.defineProperty`
- 需要递归处理所有属性
- 无法监听数组索引和长度
- 无法监听对象属性的新增和删除
- 需要 `Vue.set` 和 `Vue.delete` 来触发更新

**Vue 3：**
- 使用 `Proxy`
- 按需响应，只有访问到的属性才会被代理
- 可以监听数组所有操作
- 可以监听对象属性的新增和删除
- 不需要 `Vue.set` 和 `Vue.delete`

### 2. 编译优化

**Vue 2：**
- 模板编译成渲染函数，没有太多优化
- diff 时需要全量对比

**Vue 3：**
- 编译时分析模板，标记动态内容
- 使用 PatchFlag 优化 diff
- 静态节点提升
- 事件处理函数缓存

### 3. 组件实例

**Vue 2：**
- 组件实例包含所有选项（data、computed、methods 等）
- 所有属性都挂载到 this 上

**Vue 3：**
- 组件实例更轻量
- setup 函数返回的内容才会挂载到实例上
- 更好的 TypeScript 支持

## 语法差异总结

### 1. 创建应用

```javascript
// Vue 2
import Vue from 'vue'
import App from './App.vue'

new Vue({
  render: h => h(App)
}).$mount('#app')

// Vue 3
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

### 2. 全局 API

```javascript
// Vue 2
import Vue from 'vue'
Vue.component('MyComponent', {})
Vue.directive('my-directive', {})
Vue.mixin({})
Vue.use(plugin)

// Vue 3
import { createApp } from 'vue'
const app = createApp({})
app.component('MyComponent', {})
app.directive('my-directive', {})
app.mixin({})
app.use(plugin)
```

### 3. 过滤器移除

```vue
<!-- Vue 2：支持过滤器 -->
<p>{{ message | capitalize }}</p>

<!-- Vue 3：过滤器被移除了，用计算属性或方法代替 -->
<p>{{ capitalize(message) }}</p>
```

### 4. v-model 变化

```vue
<!-- Vue 2：一个组件只能有一个 v-model -->
<MyComponent v-model="value" />

<!-- Vue 3：支持多个 v-model -->
<MyComponent v-model:title="title" v-model:content="content" />
```

### 5. 事件 API 变化

```javascript
// Vue 2
this.$on('event', handler)
this.$once('event', handler)
this.$off('event', handler)
this.$emit('event', data)

// Vue 3：移除了 $on、$once、$off
// 推荐使用 mitt 或 events 库
import mitt from 'mitt'
const emitter = mitt()
emitter.on('event', handler)
emitter.emit('event', data)
```

## 面试高频问题

### 1. Vue 2 和 Vue 3 响应式原理的区别？

**Vue 2：**
- 使用 `Object.defineProperty` 劫持对象属性的 getter 和 setter
- 需要递归处理所有属性，初始化性能差
- 无法监听数组索引和长度变化
- 无法监听对象属性的新增和删除
- 需要 `Vue.set` 和 `Vue.delete` 来触发更新

**Vue 3：**
- 使用 `Proxy` 代理整个对象
- 按需响应，只有访问到的属性才会被代理
- 可以监听数组所有操作
- 可以监听对象属性的新增和删除
- 不需要额外的 API，直接操作即可

### 2. 为什么 Vue 3 要用 Proxy 替代 Object.defineProperty？

1. **功能更强大**：可以监听数组索引、长度、对象属性的新增和删除
2. **性能更好**：按需响应，不需要递归处理所有属性
3. **代码更简洁**：不需要 `Vue.set` 和 `Vue.delete`
4. **更符合标准**：Proxy 是 ES6 标准，浏览器支持更好

### 3. Composition API 和 Options API 的区别？

**Options API：**
- 逻辑分散在不同选项里（data、computed、methods 等）
- 代码复用困难，只能用 mixin
- TypeScript 支持差

**Composition API：**
- 相关逻辑集中在一个函数里
- 更容易提取和复用逻辑（composable）
- TypeScript 支持好
- 更适合大型项目

### 4. Vue 3 的性能优化有哪些？

1. **响应式系统优化**：使用 Proxy，按需响应
2. **编译优化**：PatchFlag、静态提升、事件缓存
3. **Tree-shaking**：支持按需导入，减小打包体积
4. **更快的 diff 算法

### 5. Vue 3 的 Composition API 有什么优势？

1. **逻辑复用**：可以提取 composable 函数，比 mixin 更清晰
2. **代码组织**：相关逻辑集中在一起，更容易维护
3. **TypeScript 支持**：类型推断更好
4. **灵活性**：可以在 setup 中使用任何 JavaScript 特性

### 6. Vue 3 的 `<script setup>` 是什么？

`<script setup>` 是 Composition API 的语法糖，更简洁：

```vue
<script setup>
// 直接写代码，不需要 return
import { ref } from 'vue'
const count = ref(0)
</script>
```

等价于：

```vue
<script>
import { ref } from 'vue'
export default {
  setup() {
    const count = ref(0)
    return { count }
  }
}
</script>
```

### 7. Vue 3 的生命周期有什么变化？

- `beforeDestroy` → `beforeUnmount`
- `destroyed` → `unmounted`
- 其他生命周期保持不变
- Composition API 中需要用 `onXxx` 的形式（如 `onMounted`）

### 8. Vue 3 的 Teleport 是做什么的？

Teleport 可以把组件渲染到 DOM 的任意位置，常用于弹窗、提示框等需要渲染到 body 下的场景。

```vue
<Teleport to="body">
  <div class="modal">弹窗内容</div>
</Teleport>
```

### 9. Vue 3 的 Fragment 是什么？

Fragment 允许组件有多个根节点，不需要额外的 DOM 节点包裹。Vue 2 要求组件只能有一个根节点。

### 10. Vue 2 项目如何升级到 Vue 3？

1. **使用迁移构建工具**：`@vue/compat` 可以在 Vue 3 中运行 Vue 2 代码
2. **逐步迁移**：
   - 先升级到 Vue 3，使用兼容模式
   - 逐步将组件改为 Composition API
   - 移除废弃的 API（如过滤器）
3. **注意破坏性变化**：
   - 全局 API 变化
   - 事件 API 移除
   - 过滤器移除
   - v-model 变化

### 11. Vue 3 的响应式 API（ref、reactive）有什么区别？

**ref：**
- 用于基本类型和对象
- 需要通过 `.value` 访问值
- 返回一个响应式引用

```javascript
const count = ref(0)
console.log(count.value) // 0
count.value = 1
```

**reactive：**
- 只用于对象
- 直接访问属性，不需要 `.value`
- 返回一个响应式代理

```javascript
const state = reactive({ count: 0 })
console.log(state.count) // 0
state.count = 1
```

### 12. Vue 3 的 computed 和 watch 有什么区别？

**computed：**
- 计算属性，有缓存
- 只有依赖变化时才重新计算
- 返回一个只读的 ref

```javascript
const doubleCount = computed(() => count.value * 2)
```

**watch：**
- 监听器，没有缓存
- 依赖变化时立即执行
- 可以执行副作用操作

```javascript
watch(count, (newVal, oldVal) => {
  console.log('count changed', newVal, oldVal)
})
```

### 13. Vue 3 的 v-model 有什么变化？

Vue 3 支持多个 v-model，并且可以自定义 prop 和 event：

```vue
<!-- Vue 2：只能有一个 v-model -->
<MyComponent v-model="value" />

<!-- Vue 3：支持多个 v-model -->
<MyComponent v-model:title="title" v-model:content="content" />
```

### 14. Vue 3 的 Tree-shaking 是什么？

Tree-shaking 是指打包时移除未使用的代码。Vue 3 支持按需导入，没用到的功能不会被打包，减小打包体积。

```javascript
// 只导入用到的功能
import { createApp, ref } from 'vue'
// 没用到的功能（如 keep-alive）不会被打包
```

### 15. Vue 3 的编译优化有哪些？

1. **PatchFlag**：标记动态属性，diff 时只对比这些属性
2. **静态提升**：静态节点提升到渲染函数外，复用
3. **事件缓存**：事件处理函数缓存，避免重复创建
4. **Block Tree**：只 diff 动态部分，跳过静态部分

## 总结

Vue 3 相比 Vue 2 的主要改进：

1. **响应式系统**：从 `Object.defineProperty` 升级到 `Proxy`，功能更强，性能更好
2. **Composition API**：更好的逻辑复用和代码组织
3. **性能优化**：更小的打包体积，更快的渲染速度
4. **TypeScript 支持**：原生支持 TypeScript，类型推断更好
5. **新特性**：Fragment、Teleport、多个 v-model 等

虽然 Vue 3 有一些破坏性变化，但整体来说升级是值得的，特别是新项目建议直接用 Vue 3。对于老项目，可以使用 `@vue/compat` 逐步迁移。


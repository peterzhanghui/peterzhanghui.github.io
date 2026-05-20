---
title: js面试题
categories: [career-insights]
tags:
  - js
  - 面试
date: 2019-02-27 14:09:45
---
## 堆栈

堆：存储引用类型值的空间

栈：存储基本类型值和指定代码的环境

## 如何判断一个数据是 NaN

1. NaN 非数字 但是用 typeof 检测是 number 类型 所以可以 （typeof XXX == number && isNaN(XXX)）
2. 利用 NaN 是唯一一个不等于任何自身的特点 n !== n
3. Object.is(value1, value2)方法（判断两个值是否相等）
4. Number.isNaN(val)

## Object.is 和 == 和 === 的区别

相同点都是判断两个值是否相等的操作

区别如下：

- == 对比时如果两边变量的类型不同会进行强制类型转换， === 和 Object.is 不会
- === 运算符 (也包括 == 运算符) 将数字 -0 和 +0 视为相等 ，而将 Number.NaN 与 NaN 视为不相等，Object.is 可以区分

```
Object.is(null, null);       // true

// 特例
Object.is(0, -0);            // false
Object.is(0, +0);            // true
Object.is(-0, -0);           // true
Object.is(NaN, 0/0);         // true
```

## Js 中 null 与 undefined 区别

Null 表示一个值被定义了，但是这个值是空值
Undefined 变量声明但未赋值

- number 转换的值不同 number（null）为 0 number（undefined） 为 NaN
- 相同点是如果使用 if 判断都会转换为 false

## Promise 的理解

### 一、什么是 Promise？

我们都知道，Promise 是承诺的意思，承诺它过一段时间会给你一个结 果。Promise 是一种解决异步编程的方案，相比回调函数和事件更合理和更 强大。 从语法上讲，promise 是一个对象，从它可以获取异步操作的消息；

### 二、promise 有三种状态：

pending 初始状态也叫等待状态，fulfiled 成功状态，rejected 失败状态；状态一旦改变，就不会再变。创造 promise 实例后，它会立即执行。

### 三、Promise 的两个特点

1. Promise 对象的状态不受外界影响
2. Promise 的状态一旦改变，就不会再变，任何时候都可以得到这个结 果，状态不可以逆，

### 四、Promise 的三个缺点

1. 无法取消 Promise,一旦新建它就会立即执行，无法中途取消
2. 如果不设置回调函数，Promise 内部抛出的错误，不会反映到外部
3. 当处于 pending（等待）状态时，无法得知目前进展到哪一个阶段， 是刚刚开始还是即将完成

### 五、主要解决的问题

1. 链式调用，主要解决回调地狱问题
2. 支持并发请求

### Promise 原理 （待做）

## async 和 defer 两者区别：

- 当 script 中有 defer 属性时，脚本的加载过程和文档加载是异步发生的，等到文档解析完(DOMContentLoaded 事件发生)脚本才开始执行。

- 当 script 有 async 属性时，脚本的加载过程和文档加载也是异步发生的。但脚本下载完成后会停止 HTML 解析，执行脚本，脚本解析完继续 HTML 解析。

- 当 script 同时有 async 和 defer 属性时，执行效果和 async 一致。

## nuxt.js （待做）

## webpack （待做）

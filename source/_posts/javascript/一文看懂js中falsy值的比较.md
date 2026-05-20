---
title: 一文看懂js中falsy值的比较
categories: [javascript]
tags:
  - js
  - 面试题
date: 2021-03-21 14:49:08
---
> 面试中的笔试题经常有碰到 js 中假值的比较，其实主要考察的是 js 中在非全等情况下，比较的一个类型隐式转换问题

## 示例代码

js 中共有 8 个 falsy 值, 分别为 false, 0, 0n, -0, NaN, '', null, undefined 还有 js 中易混的空数组和控对象。

```
<!-- 首先罗列所有易混的值 几个数字0 的转换表现一致所以保留一个 -->
let falsyArr = ['', false, 0, null, undefined, NaN, [], {}];

for (let i =0 ; i < falsyArr.length; i ++) {
    let result = {};
    for (let j =0 ; j < falsyArr.length; j ++){
        <!-- 不需要和自身对比，过滤 -->
        if(i != j) result[falsyArr[j]] = (falsyArr[i] == falsyArr[j]);
    }
    console.log(`和${falsyArr[i]}的对比结果如下\n`)
    console.table(result)
}

```

## 拆箱转换

拆箱转换在 JavaScript 标准中，规定了 ToPrimitive 函数，它是对象类型到基本类型的转换（即，拆箱转换）。对象到 String 和 Number 的转换都遵循“先拆箱再转换”的规则。通过拆箱转换，把对象变成基本类型，再从基本类型转换为对应的 String 或者 Number。拆箱转换会尝试调用 valueOf 和 toString 来获得拆箱后的基本类型。如果 valueOf 和 toString 都不存在，或者没有返回基本类型，则会产生类型错误 TypeError。

```
var o = {valueOf : () => {console.log("valueOf"); return {}},toString : () => {console.log("toString"); return {}}}
o * 2

// valueOf
// toString
// TypeError

```

在 ES6 之后，还允许对象通过显式指定 @@toPrimitive Symbol 来覆盖原有的行为

```
var o = {valueOf : () => {console.log("valueOf"); return {}},toString : () => {console.log("toString"); return {}}}o[Symbol.toPrimitive] = () => {console.log("toPrimitive"); return "hello"}console.log(o + "")
// toPrimitive
// hello

```

## 总结

![图片来自掘金小册-前端面试之道](/img/对比流程图.webp)

根据输出结果可以得到以下结论：

1. [] 对比时会转化为空字符串 ''
2. {} 对比会转化为 '[object Object]' ([JavaScript 对象转换到基本类型值算法 ToPrimitive](https://juejin.cn/post/6844903555548053511))
3. NaN, {} 和任何值比较都为 false
4. null 和 undefined 除了 null == undefined 为 true 其他都是 false （js 规范中提到，在比较相等性之前不能将 null 和 undefined 转化为其他值，并且规定两者相等，都表示无效的值）
5. '' 和 [],表现一致，和数字和 false 比较都会转化为数字 0，结果为 true，其他为 false
6. NaN 不管是不是全等和自身相比都为 false

代码中如果是字符串和数字的判断可以使用 == 来判断，如果涉及到类型不明确的数据建议类型转换加 === 判断

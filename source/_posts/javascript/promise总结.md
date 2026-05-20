---
title: promise总结
categories: [javascript]
tags: js
date: 2021-03-29 18:13:10
---
> 整理一些 promise 常考的代码执行题

## 处理器函数 executor 中有 null

如果 promise 的处理器函数 executor 中有 null，那么对应的状态会向下传递

```
var p1 = new Promise(function(resolve, reject){
    reject(1000)
})
var p2 = p1.then( function() {
    console.log('p2');

}, null)
p2.then(()=>{
    console.log('p2 success');
},()=> {
    console.log('p2 error');  // p2 error
})

```

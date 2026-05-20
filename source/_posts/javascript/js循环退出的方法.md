---
title: js循环退出的方法
categories: [javascript]
tags: js
date: 2021-01-23 14:57:40
---
> 本文主要介绍 js 中 循环跳出/终止的方法，希望对你有所帮助

## 常用的方法

- continue
- break
- return

  接下来，分别看看他们不同的使用场景

## 一、for 循环中的使用

### continue 在 for 循环中是退出当前循环，接着执行下面的循环

```
for(var i =0;i<arr.length;i++){
    if (arr[i] == 4) continue;
    console.log(arr[i]) // 2,6,8
}

```

### break 在 for 循环中是退出整个循环

```
for(var i =0;i<arr.length;i++){
    if (arr[i] == 4) break;
    console.log(arr[i]) // 2
}

```

### return 在 for 循环中是退出整个循环，和 break 不同的是，必须要包含在方法体中，因为 for 本身没有函数作用域，是全局作用域

> for 循环 如果没有包含在方法中直接使用 return，会有报错 Uncaught SyntaxError: Illegal return statement

```
for(var i =0;i<arr.length;i++){
    if (arr[i] == 4) break;
    console.log(arr[i]) // 2
}

```

## 其他遍历器 终止循环的方法

forEach()不支持 break 和 continue，可以用 return false 或者 return

```
[2,4,6,8].forEach(item => {
    if (item == 4) return false;
    console.log(item) // 2,6,8
})

```

return 退出当前循环，执行下一个循环条件。如果想退出整个循环可以通过抛出异常的方式

```
[2,4,6,8].forEach(item => {
    if (item == 4) throw new Error("jump");
    console.log(item) // 2
})

```

## 最后

感谢各位的阅读，如有不对欢迎批评指正，共同交流。

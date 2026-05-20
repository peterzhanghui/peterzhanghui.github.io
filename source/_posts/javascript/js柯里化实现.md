---
title: js柯里化实现
categories: [javascript]
tags:
  - js
  - 面试题
date: 2021-03-28 09:58:56
---
> 柯里化是 Javascript 中函数式编程的一个重要概念。js 柯里化 引用百科中的说明--柯里化是把接受多个参数的函数变换成接受一个单一参数(最初函数的第一个参数)的函数，并且返回接受余下的参数且返回结果的新函数的技术

主要的作用如下

- 延迟计算
- 参数复用

接下来我们分别使用代码实现一下

## 延迟计算

### 参数个数已知

```

// 函数柯里化 要求，实现 add(1)(2)(3), add(1,2)(3) 返回累加结果
// 实现思路，一个是保存参数，reduce 实现累加
function carry(fn, args) {
    var len = fn.length;
    args = args || [];
    return function(){
        let arg = [].slice.apply(arguments);
        var argsList = args.slice(0);
        argsList.push.apply(argsList,arg);
        if(argsList.length < len){
            return carry.call(this,fn,argsList);
        }else{
            return fn.apply(this,argsList);
        }
    }
}
function  add(a,b,c) {
    let args = [].slice.apply(arguments);
    let result = args.reduce((account,item)=>{
        return account+= item;
    })
    console.log(result);
}
var addCarry = carry(add);

// addCarry(3)(4)(6);
addCarry(1,2)(3)

```

### 参数个数未知

```
var carry= function(fn) {
    var argsList = [];
    return function(){
        let args = [].slice.apply(arguments);
        if (args.length == 0) {
            fn(argsList)
        }else {
            argsList.push.apply(argsList,args)
        }
    }
}
function add (list) {
    let result = list.reduce((account,item)=>{
        return account+= item;
    })
    console.log(result);

}

var addCarry = carry(add);

addCarry(1);
addCarry(20);
addCarry(3);
addCarry();
```

## 参数复用

比如我们判断参数类型的方法

```

function carry(fn) {
    const inner = (args = []) => {
       return  args.length >= fn.length ?  fn(...args) : (...innerArgs) => inner([...args, ...innerArgs])
    }
    return inner();
}

function isType(type, val) {
    return Object.prototype.toString.call(val) == `[object ${type}]`;
}

let check = {};

['String', 'Number', 'Array', "Object", "Boolean", 'Null', 'Undefined'].forEach((type) => {
    check['is' + type] = carry(isType)(type);
})

<!-- 测试代码 -->
console.log(check.isNumber('ddd'));

```

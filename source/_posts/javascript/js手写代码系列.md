---
title: js手写代码系列
categories: [javascript]
tags:
  - js
  - 面试题
date: 2021-03-24 11:20:11
---
> js 中常用的一些方法的代码实现

## new 操作

引用 MDN 上的相关描述：new 关键字会进行如下的操作：

创建一个空的简单 JavaScript 对象（即{}）；
链接该对象（设置该对象的 constructor）到另一个对象 ；
将步骤 1 新创建的对象作为 this 的上下文 ；
如果该函数没有返回对象，则返回 this。

```
// construct: 构造函数
function newFunction() {
  // 通过Object.create创建一个空对象；
  var res = Object.create(null);
  // 获取第一个构造函数参数
  var construct = Array.prototype.shift.call(arguments);
  res.__proto__ = construct.prototype;
  // 使用apply执行构造函数，将构造函数的属性挂载在res上面
  var conRes = construct.apply(res, arguments);
  // 判断返回类型
  return conRes instanceof Object ? conRes : res;
}

```

### new.target

new 是从构造函数生成实例的命令。ES6 为 new 命令引入了一个 new.target 属性，（在构造函数中）返回 new 命令作用于的那个构造函数。如果构造函数不是通过 new 命令调用的，new.target 会返回 undefined，因此这个属性可以用来确定构造函数是怎么调用的

## bind

```
function.prototype.bind = function(context) {
      if (typeof this !== "function") {
        throw new TypeError("not a function");
      }
      let self = this;
      let args = [...arguments].slice(1);
      function Fn() {}
      Fn.prototype = this.prototype;
      let bound = function () {
        let res = [...args, ...arguments]; //bind传递的参数和函数调用时传递的参数拼接
        context = this instanceof Fn ? this : context || this;
        return self.apply(context, res);
      }; //原型链
      bound.prototype = new Fn();
      return bound;
    }

```

## Object.create

方法创建一个新对象，使用现有的对象来提供新创建的对象的**proto**

```
function(obj){
   let oo = {};
   oo.__proto__ = obj;
    return oo;
}
因为__proto__从web标准中删除，所以第二种更好

funciton(obj){
    function Fn(){}
    Fn.prototype = obj;
    return new Fn()
}

```

## instanceof

```
function _instanceof(left, right) {
  var prototype = right.prototype;
  var proto = left.__proto__;
  while (true) {
    if (proto === null) return false;
    if (proto === prototype) return true;
    proto = proto.__proto__;
  }
}

```

这个函数无法做到与原生的 Object.create 一致，一个是不支持第二个参数，另一个是不支持 null 作为原型

## 数组扁平化 flat

### 使用 flat

```
let result = arr.flat(Infinity);
```

### 使用递归的方法

```
有一个多维数组
var arr=[1,2,3,[4,5],[6,[7,[8]]]]
处理后转为一维数组

var arr = [1, 2, 3, [4, 5], [6, [7, [8]]]];

function myFlat() {
    let result = [];
    return function flat(arr) {
        if (arr instanceof Array) {
            if (arr.length === 0) return [];
            for (let item of arr) {
                if (item instanceof Array) {
                    // myFlat(item)
                    result.concat(flat(item))
                } else {
                    result.push(item)
                }
            }
        }
        return result;
    }
}

console.log(myFlat()(arr));

```

## async await

## promise.all()

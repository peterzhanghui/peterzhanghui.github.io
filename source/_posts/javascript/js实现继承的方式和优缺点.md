---
title: js实现继承的方式和优缺点
categories: [javascript]
tags:
  - js
  - 面试题
date: 2021-03-20 21:33:25
---
## 原型继承

实现的核心代码：

```
Child.prototype = new Parent();

var child1 = new Child();
```

缺点：

1. 引用类型的属性被所有实例共享
2. 创建实例时不能向 parent 传参

## 构造函数继承

在子类构造函数中调用父类的构造函数，相当于在新对象上，运行了父类的所有初始化代码

```
function Parent () {
    this.names = ['kevin', 'daisy'];
}

function Child () {
    Parent.call(this);
}

var child1 = new Child();

```

优点：

1. 避免了引用类型的属性被所有实例共享
2. 可以在 Child 中向 Parent 传参

缺点：

1. 方法都在构造函数中定义，每次创建实例都会创建一遍方法。
2. 只能继承父类私有方法和属性，原型链中的无法继承。

## 组合继承

结合原型继承和构造函数继承

```
function Parent (name) {
    this.name = name;
    this.colors = ['red', 'blue', 'green'];
}

Parent.prototype.getName = function () {
    console.log(this.name)
}

function Child (name, age) {

    Parent.call(this, name);

    this.age = age;

}

Child.prototype = new Parent();
Child.prototype.constructor = Child;

var child1 = new Child('kevin', '18');
```

缺点：会调用两次父构造函数，在 call()方法和 Child.prototype = new Parent()两次都调用了父级的构造函数，造成了不必要的性能浪费

## 寄生式继承

```
function createObj (o) {
    var clone = Object.create(o);
    clone.sayName = function () {
        console.log('hi');
    }
    return clone;
}

```

缺点：跟借用构造函数模式一样，每次创建对象都会创建一遍方法。

## 寄生组合式继承

```
function Parent (name) {
    this.name = name;
    this.colors = ['red', 'blue', 'green'];
}

Parent.prototype.getName = function () {
    console.log(this.name)
}

function Child (name, age) {
    Parent.call(this, name);
    this.age = age;
}

// 关键的三步
var F = function () {};

F.prototype = Parent.prototype;

Child.prototype = new F();


var child1 = new Child('kevin', '18');

```

最佳的继承实现 能够正常使用 instanceof 和 isPrototypeOf

## ES6 中的 extends

ES6 中的 extends 继承就是类似寄生组合式继承的实现方式。
类的写法实际上也是由原型运行时来承载的，逻辑上 JavaScript 认为每个类是有共同原型的一组对象，类中定义的方法和属性则会被写在原型对象之上。此外，最重要的是，类提供了继承能力。我们来看一下下面的代码

## 总结：

### instanceof

child instanceof Parent

运算符用于检测构造函数的 prototype 属性是否出现在某个实例对象的原型链上

### isPrototypeOf

用于测试一个对象(Parent)是否存在于另一个对象(child)的原型链上
Parent.prototype.isPrototypeOf(child)

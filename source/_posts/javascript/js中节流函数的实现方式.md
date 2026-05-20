---
title: js中节流函数的实现方式
categories: [javascript]
tags: js
date: 2021-03-27 12:38:27
---
> 函数节流也是前端在监听处理高频事件时候，常用的优化方法，在不影响用户体验的情况下，限制事件触发的频率。常用的地方又页面 scorll, resize 事件，还有用户提交复杂表单，有时候会有定时保存草稿箱的功能，都可以使用函数节流来做优化。

## 定时器的实现方式

```
/**
 * 节流throttle（定时器）
 *
 * */
var throttle2 = function(func, delay){
  var timer = null;
  return function() {
    var context = this;
    var args = arguments;
    if (timer) {
      clearTimeout(timer)
    } else {
      timer = setTimeout(function(){
        func.apply(context,args);
        timer = null;
      }, delay);
    }
  }

}

```

## 时间戳的实现方式

```
/**
 * 节流throttle（时间戳）
 *
 * */
var throttle1 = function (func, delay) {
  var prev = Date.now();
  return function () {
    var context = this;
    var args = arguments;
    var now = Date.now();
    if (now - prev >= delay) {
      func.apply(context, args);
      prev = Date.now();
    }
  };
};
function handle() {
  console.log(Math.random());
}
window.addEventListener("scroll", throttle1(handle, 1000));
```

## 组合防抖节流

```
/**
* @method    组合防抖节流
* @param     {int} delay 防抖执行的时间间隔
* @param     {int} mustRunDelay 节流执行的时间间隔
* @return    {返回值类型} 返回值说明
*/

var throttle = function(fn, delay, mustRunDelay) {
  let startTime = Date.now();
  let timer = null;
  let isFirst = true; //断是否是第一次执行，是第一次就不立即执行
  return function() {
    let context = this;
    let args = [].slice.call(arguments);
    let remaining = mustRunDelay-(Date.now()-startTime);
    clearTimeout(timer)

    if (remaining <= 0){
      startTime = Date.now();
      if (!isFirst){
        fn.apply(context, args);
      } else {
        isFirst = false;
      }
    } else{
      timer = setTimeout(function(){
        fn.apply(context, args);
      },delay)
    }
  }
}
window.addEventListener("scroll", throttle(function(){console.log(1)}, 1000, 2000));

```

## 总结对比优缺点

- 定时器的实现，缺点：最后一次时间不够一次 delay 仍然会触发执行
- 时间戳的实现，缺点：时间不够一次 delay，不会触发执行, 第一次会立即执行
- 组合实现，添加 isFirst 标记，如果不加第一次触发事件会立即执行，添加标记过滤第一次执行，这样就可以完美实现了

当然这些都只是从代码逻辑上来考虑，具体还是要结合业务需求灵活使用。

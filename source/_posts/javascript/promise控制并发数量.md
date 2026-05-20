---
title: promise控制并发数量
categories: [javascript]
tags:
  - js
  - 面试题
date: 2021-03-27 21:32:53
---
> 控制并发数量主要是考察对 promise 的掌握情况。

## 使用 promise.all 实现

实现思路：
首先使用 while 并发多个请求
然后不管那个异步请求执行完成，如果待执行的数组中还有任务，就会返回一个新的异步任务（最绕的就是这个）
最后使用 Promise.all 监测所有并发数组执行完成返回。

```
/**
 * 并发控制的方法
 * @params list {Array} - 要迭代的数组
 * @params limit {Number} - 并发数量控制数
 * @params asyncHandle {Function} - 对`list`的每一个项的处理函数，参数为当前处理项，必须 return 一个Promise来确定是否继续进行迭代
 * @return {Promise} - 返回一个 Promise 值来确认所有数据是否迭代完成
 */
 let mapLimit = (list, limit, asyncHandle) => {
    let recursion = (arr) => {
        return asyncHandle(arr.shift())
            .then(()=>{
                if (arr.length!==0) return recursion(arr)   // 数组还未迭代完，递归继续进行迭代
                else return 'finish';
            })
    };

    let listCopy = [].concat(list); // 对外部数组做修改，先做一个复制，不影响外部数据
    let asyncList = []; // 正在进行的所有并发异步操作
    while(limit--) {
        asyncList.push( recursion(listCopy) );
    }
    return Promise.all(asyncList);  // 所有并发异步操作都完成后，本次并发控制迭代完成
}

var dataLists = [1,2,3,4,5,6,7,8,9,11,100,123];
var count = 0;

// 异步加载的方法
function asyncLoad (curItem){
    return new Promise(resolve => {
        count++
        setTimeout(()=>{
            console.log(curItem, '当前并发量:', count--)
            resolve();
        }, Math.random() * 5000)
    });
}

// 测试
mapLimit(dataLists, 3, asyncLoad).then(response => {
    console.log('finish', response)
})

```

## 使用 promise.race 实现

```
// 第二种实现方案

function mapLimit(list, limit, handler) {
    let urlList = [].concat.call(list);
    let promisesList = [];
    promisesList = urlList.splice(0,limit).map((item,index) => {
        return handler(item).then(() => {
            return index;
        })
    })
    let p = Promise.race(promisesList);

    for (let i = 0; i < urlList.length; i++) {
        p = p.then((res)=>{
            promisesList[res] = handler(urlList[i]).then(()=>{
                return res;
            });
            return Promise.race(promisesList);
        })
    }
}

```

参考文章

[15 行代码实现并发控制（javascript）](https://segmentfault.com/a/1190000013128649)

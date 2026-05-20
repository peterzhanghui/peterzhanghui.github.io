---
title: async/await实现简版红绿灯
categories: [javascript]
tags: js
date: 2021-01-01 10:22:43
---
> 通过 async/await 实现简化版的红绿灯

代码如下：

```
async function changeColor(color, duration) {
    inner.style.backgroundColor = color;
    await sleep(duration);
}
function sleep(duration) {
    return new Promise((resolve) => {
        setTimeout(resolve, duration);
    });
}
async function main() {
    while (true) { // 实现循环
        await changeColor("green", 2000);
        await changeColor("yellow", 2000);
        await changeColor("red", 2000);
    }
}

```

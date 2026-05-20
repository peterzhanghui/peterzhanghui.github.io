---
title: 统计html中出现最多的标签
categories: [javascript]
tags:
  - js
  - 面试
date: 2021-01-28
---
### 查找当前页面中出现最多的 html 标签

```
const maxBy = (list, keyBy) => list.reduce((x, y) => keyBy(x) > keyBy(y) ? x : y)

function getFrequentTag () {
  const tags = [...document.querySelectorAll('*')].map(x => x.tagName).reduce((o, tag) => {
    o[tag] = o[tag] ? o[tag] + 1 : 1;
    return o
  }, {})
  return maxBy(Object.entries(tags), tag => tag[1])
}

```

转载文章：
(原文连接)[https://juejin.cn/post/6922229465468633095]

---
title: css中margin属性的使用
date: 2018-11-01
categories: [frontend-engineering]
tags: css
---
> margin 是我们在页面布局的时候经常使用的 css 属性

当 margin 属性值为百分比时，边距是基于父元素的宽度来计算的

经查阅，这与页面默认的书写模式 writing-mode 有关。默认情况下 writing-mode 的值为 horizontal-tb，即水平书写方式。

当把书写模式修改为纵向的时候，margin-top/bottom/left/right 的百分比值都将会以包含元素的高度为参照

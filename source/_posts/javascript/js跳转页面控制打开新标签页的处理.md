---
title: js跳转页面控制打开新标签页的处理
date: 2021-01-12 23:02:27
categories: [javascript]
tags: js
---
> 项目中经常碰到列表跳详情的操作，需求想要新标签页不在当前页面，而是打开一个新的标签页

这需求简单，直接 windows.open(url,'\_blank')搞定，测试发现

### 问题一：如果在 ajax 异步请求数据的时候，会阻止弹框跳转。主要是浏览器会认为这个跳转不是用户自己操作的。

解决方法如下：使用 a 标签模拟用户点击操作

```
/**
* @method    跳转新的标签页
* @param     {参数类型} 参数名 参数说明
* @return    {返回值类型} 返回值说明
*/
Vue.prototype.$open_blank = function(url) {
  //  window.open(url,"_blank");
   let referLink = document.createElement('a');
  referLink.href = url;
  referLink.target = "_blank";
  referLink.rel="noopener noreferrer";
  document.body.appendChild(referLink);
  referLink.click();
  document.body.removeChild(referLink);
}
```

### 问题二：性能问题 Chrome 中跳转新的标签页以后，上一个标签页面会卡死无法操作，其他浏览器正常。

暂未发现解决方案。

### 问题三： 安全问题 新开的窗口中可以通过 window.opener.location = newURL 来重写父页面的 url。所以有安全风险

解决方法 ：a 标签的 rel 添加 noopener

```
referLink.rel="noopener noreferrer";

```

参考文章

[在新窗口中打开页面？小心有坑！](https://cloud.tencent.com/developer/article/1008860)

[打开新窗口的正确姿势](https://blog.asaki.me/2018/05/07/)

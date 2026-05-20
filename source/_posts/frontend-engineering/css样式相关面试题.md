---
title: css样式相关面试题
categories: [frontend-engineering]
tags:
  - css
  - 面试题
date: 2019-02-26 16:43:26
---
> 总结梳理前端开发在面试中遇到的高频 css 面试题

## 子 div 在父 div 中水平垂直居中的方式

1. display: flex 弹性和布局，需要考虑 ie 兼容问题

```
.outside{
    width: 400px;
    height: 400px;
    background: goldenrod;
    display: flex;
    justify-content: center;
    align-items: center;
}
.inside{
    width: 100px;
    height: 100px;
    background: forestgreen;
}
```

宽高和背景色属性下面实现中省略

2. position 定位 + maring(子元素高度确定) / transform（子元素高度不确定）

```
.outside{
    width: 600px;
    height: 400px;
    padding: 30px;
    background: goldenrod;
    position: relative;
}
.inside{
    width: 100px;
    height: 100px;
    position: absolute;
    top: 50%;
    left: 50%;
    margin: -50px 0 0 -50px;
    /* transform:translate(-50%,-50%); */
    background: forestgreen;
}
```

3. display：table-cell，vertical-align：middle;

```
.outside{
    width: 600px;
    height: 400px;
    padding: 30px;
    background: goldenrod;
    display:table-cell;
    vertical-align:middle;
}
.inside{
    width: 100px;
    height: 100px;
    margin: 0 auto;
    background: forestgreen;
}
```

## 用纯 CSS 创建一个三角形？

### 带有背景色的

```
/*
  采用的是相邻边框链接处的均分原理
  将元素的宽高设为0，只设置 border ,
  将任意三条边隐藏掉（颜色设为 transparent ）,剩下的就是一个三角形
 */
#demo{
  width: 0;
  height: 0;
  border-width: 20px;
  border-style: solid;
  border-color: transparent transparent red transparent;
}

```

### 画一个只有边框的三角形

实现方式就是在上面的基础上再加一个小一号的三角形块通过定位，遮罩住部分，最终显示为有边框的三角形

```
span {
    position: absolute;
    top: 30%;
    left: 50%;
    margin-left: -100px;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 0 100px 100px 100px;
    border-color: transparent transparent #362a98 transparent;
}
span i {
    position: absolute;
    left: -96px;
    top: 2px;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 0 96px 96px 96px;
    border-color: transparent transparent #eee transparent;
    -webkit-transition: all 0.3s ease-in-out;
    transition: all 0.3s ease-in-out;
}
span i:hover {
    border-color: transparent transparent #362a98 transparent;
}

```

## 清除浮动

> 当不给父元素设置宽高时，父元素的宽高会被子元素的内容撑开。但当子元素设置浮动属性（float） 后，子元素会溢出到父元素外，父元素的宽高也不会被撑开，这称之为“高度塌陷”。可以理解为使用浮动后的副作用，解决方法大体有以下两种

1.  子元素添加 clear 属性

实现的思路就是给对应的 css 选择器添加伪类，既要把伪元素变成块元素，又不能让他展示出来影响页面布局

```
.clearfix {
  *zoom: 1;/*ie6清除浮动的方式 *号只有IE6-IE7执行，其他浏览器不执行*/
}

.clearfix:after {
  display: block;       // 转化为块布局也可以设置为table，设置为行内块元素
  clear: both;          // 使用clear 清除浮动对元素的影响
  content: " ";         // 添加一个内容
  height: 0;            // 把内容在页面隐藏
  visibility: hidden;   // 把内容在页面隐藏
  overflow: hidden;     // 把内容在页面隐藏
}

```

2. 父元素添加 overflow: hiden;触发浮动元素父元素的 BFC (Block Formatting Contexts, 块级格式化上下文)，使到该父元素可以包含浮动元素

第二种虽然代码量小，但是超出尺寸的内容会被隐藏（不推荐）目前主流的做法是使用第一种

## 盒模型

- 标准盒模型 (box-sizing: content-box;) 宽高大小不包含 padding,border
- IE 盒模型 （box-sizing: border-box;）宽高大小包含 padding,border
  目前采用最多的是 ie 盒模型，设置宽高包含这个元素尺寸，不需要在计算

- flex 布局
- 多列布局 (column-count: 3;容器分三列布局，一般用于 平板电脑等 宽屏上的文章布局)
- 网格布局 （grid）

## 介绍下 BFC 及其应用

BFC 就是块级格式上下文，是页面盒模型布局中的一种 CSS 渲染模式，相当于 一个独立的容器，里面的元素和外部的元素相互不影响(即不会造成 margin 重叠)

### 创建 BFC 的方式有

- html 根元素
- float 浮动
- 绝对定位
- overflow 不为 visiable
- display 为表格布局或者弹性布局

### BFC 主要的作用是

- 清除浮动
- 防止同一 BFC 容器中的相邻元素间的外边距重叠问题

## 经典布局方案

左右固定，中间自适应

- 圣杯布局

```
.clearfix{
        zoom: 1;
    }
    .clearfix::after{
        clear: both;
        content: '.';
        visibility: hidden;
        display: block;
        overflow: hidden;
        height: 0;
    }
    .content{
        overflow: hidden;
        height: 100%;
        padding: 0 100px;
    }
    .center,.left, .right{
        float: left;
    }
    .center{
        width: 100%;
        min-height: 400px;
        background: goldenrod;
    }
    .left, .right{
        width: 100px;
        height: 100px;
        background: forestgreen;
    }
    .left{
        margin-left: -100%;
        position: relative;
        left: -100px;
    }
    .right{
        margin-right: -100px;
    }
        <div class="content ">
       <div class="center"></div>
       <div class="left"></div>
       <div class="right"></div>
   </div>
```

- 双飞翼布局
  和圣杯布局不同的就是 left，right 和 center 不在同一个父级元素下

  ```
  <div class="clearfix">
        <div class="content ">
            <div class="center"></div>
        </div>
        <div class="left"></div>
        <div class="right"></div>
    </div>
     .clearfix{
            zoom: 1;
        }
        .clearfix::after{
            clear: both;
            content: '.';
            visibility: hidden;
            display: block;
            overflow: hidden;
            height: 0;
        }
        .content{
            width: 100%;
            height: 100%;
        }
        .content,.left, .right{
            float: left;
        }
        .center{
            margin: 0 100px 0 100px;
            min-height: 400px;
            background: goldenrod;
        }
        .left, .right{
            width: 100px;
            height: 100px;
            background: forestgreen;
        }
        .left{
            margin-left: -100%;
        }
        .right{
            margin-left: -100px;
        }
  ```

  - 使用 flex 布局

## flex 弹性布局

1. 设置盒子的 display 属性为 flex，或者 line-flex，其对应还有六个 css 属性，分别为：

1）flex-direction：设置子元素的排列方式（row，column，row-reverse，column-reverse）

2）flex-warp：设置子元素的是否换行（nowarp，warp，warp-reverse）

3）flex-flow：flex-direction 和 flex-warp 的缩写，默认为 row nowarp

4）justify-content：设置子元素的水平排列方式（flex-start，flex-end，center，span-around，span-between）

5）align-items：设置子元素的垂直方式（flex-start，flex-end，center，stretch，baseline）

6）align-content：设置多个轴线的排列方式（flex-start，flex-end，center，spand-around，spand-between，stretch）

2. 对应的子元素项目也拥有自身的六个 css 属性，分别为：

1）order：设置元素的排列权重 值越大越在后

2）flex-grow：设置元素的放大比例

3）flex-shrink：设置元素的缩小比例

4）flex-basis：设置多余空间项目主轴所占比例空间

5）**flex：flex-grow 和 flex-shrink 和 flex-basis 的缩写方式 默认为 0 1 auto**

6）align-self：设置子元素自己的垂直排列方式，默认为盒子的 align-items 的值

:warning:：设置 flex 布局后，子元素的 float，clear，vertical-align 都无效

## CSS3 新增属性用法的整理：

1、box-shadow（阴影效果）

2、border-color（为边框设置多种颜色）

3、border-image（图片边框）

4、text-shadow（文本阴影）

5、text-overflow（文本截断）

6、word-wrap（自动换行）

7、border-radius（圆角边框）

8、opacity（透明度）

9、box-sizing（控制盒模型的组成模式）

10、resize（元素缩放）

11、outline（外边框）

12、background-size（指定背景图片尺寸）

13、background-origin（指定背景图片从哪里开始显示）

14、background-clip（指定背景图片从什么位置开始裁剪）

15、background（为一个元素指定多个背景）

16、hsl（通过色调、饱和度、亮度来指定颜色颜色值）

17、hsla（在 hsl 的基础上增加透明度设置）

18、rgba（基于 rgb 设置颜色，a 设置透明度）

## 移动端响应式布局开发的方案

- media
- rem
- vh / vw 类似百分比布局

## 移动端适配 1px 的问题 （待做）

dpr = 物理像素 / css 像素 在 dpr = 2；
1px 的 css 像素在设备中是 2px 的物理像素，这会导致在设备上看上去 1px 的边框是 2px
解决方法： 用 transfrom： scale（）缩小 dpr 倍数 在 meta 标签中设定 scale 缩小两倍

Retina 屏 1px 像素问题

1. 伪元素 + transform scaleY(.5)
2. border-image
3. box-shadow: 0 0 1px red;

## content-visibility: auto

使用 content-visibility 可以跳过渲染屏幕之外的内容

## will-change

目前，主流浏览器一般根据 position、transform 等属性来决定合成策略，来“猜测”这些元素未来可能发生变化
使用 will-change，可以提示浏览器说明元素可能会有变化，这样浏览器就可以给他单独生成一个位图，可以提升合成策略的效果。
浏览器将为元素创建一个单独的层。之后，它将元素的渲染与其他优化一起委派给 GPU。随着 GPU 加速接管动画的渲染，这将使动画更加流畅。

```
//在样式表中
.animating-element{
  will-change：opacity;
}
//在HTML中
<div class =“ animating-elememt”>
  动画子元素
</ div>

```

在浏览器中呈现以上代码段时，它将识别该 will-change 属性并优化将来与不透明度相关的更改。

### 什么时候不使用

虽然 will-change 是为了提高性能，它也可以，如果你滥用它降低了网络应用性能。
使用 will-change 表示该元素将来会更改。
因此，如果您尝试同时使用 will-change 动画和动画，那么它不会给您带来优化。因此，建议在父元素上使用 will-change，在子元素上使用动画。

```
.my-class {
  will-change：opacity;
}
.child-class {
  过渡：不透明度1s缓入；
}

```

请勿使用在非动画元素。
在 will-change 元素上使用时，浏览器将尝试通过将元素移到新层并将转换移交给 GPU 来对其进行优化。如果您没有任何要转换的内容，则会导致资源浪费。

## div 元素使用 display:inline-block 后元素中间还是有空格

引发的原因就是 我们编辑 html 的时候代码会格式化换行，所以浏览器在解析的时候就会展示出来
解决方案：

- 把换行和中间的空格都去掉（影响代码可读性）
- 使用 float
- 给外部的父元素添加 font-size： 0；

## 网站主题切换实现 灰色模式（悼念模式），日间模式，暗黑模式

### 最简单的做法就是给 html 直接设置滤镜效果 filter

日间模式就正常页面样式
灰色模式 ：（灰度 100%）
filter: grayscale(1);
暗黑模式：
filter: invert(1) hue-rotate(180deg);

invert()：反相，反向输出图像着色（白变黑）

### prefers-color-scheme

prefers-color-scheme CSS 媒体特性用于检测用户是否有将系统的主题色设置为亮色(light)或者暗色(dark)

```
@media (prefers-color-scheme: dark) {
  .day.dark-scheme   { background:  #333; color: white; }
  .night.dark-scheme { background: black; color:  #ddd; }
}

@media (prefers-color-scheme: light) {
  .day.light-scheme   { background: white; color:  #555; }
  .night.light-scheme { background:  #eee; color: black; }
}

```

## css 定义全局变量

```
//定义
:root{
   --theme-color:red;
}

//使用的时候
#app{
    background-color:var(--theme-color);
}

//假如我们没有指定--theme-color这个属性，则可以在使用的时候加上替代值
#app{
    background-color:var(--theme-color,black);
}

```

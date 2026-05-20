---
title: 使用canvas实现图片压缩上传
date: 2018-10-17
categories: [frontend-engineering]
tags:
  - canvas
  - js
---
> 项目需求： 上传图片前对图片进行压缩减少文件体积  
> 需要支持上传图片的格式 png，jpg，gif 因为 canvas 不支持 gif，所以对 gif 不做处理
> 又因为 canvas 的 bolb 方法只支持对 jpeg，和 webp 格式的文件做质量压缩，项目又需要兼容 ie，故只能保存为 jpeg 格式文件

## 一、上传前压缩图片的好处

- 可以减少用户的等待时间，提升使用体验，目前手机拍摄的图片文件大小一般在几 M 左右，文件直接上传时会有卡顿现象。
- 可以减少服务端的存储空间
- 再次回去图片资源是也可以快速的加载。虽然目前阿里云的 oss 有相对应的 api 可以通过降低图片质量等方法减少体积，不过使用 canvas 可以直接减少源文件的体积。

## 二、实现思路以及示例代码

1. 使用 FileReader 对象获取本地文件（使用文件选择 input 元素）的 base64 内容
2. 使用 context.drawImage 把获取到的文件画在 canvas 上
3. 使用 canvas.toBlob 对图片做质量压缩

### 示例代码

```

/**
 * 对选中的图片文件处理
 *
 * @param  {obj}  event  图片文件
 * */
uploadImg (event) {
    // 为选择文件返回
    if (!event.target.files[0]) return;
    let file = event.target.files[0],
        fileName = file.name.substring(file.name.lastIndexOf(".") + 1).toLowerCase();
    // 文件格式校验
    if (fileName != "jpg" && fileName != "png" && fileName != "gif" ) {
        this.$store.commit('setPrompt', {status: true, text: '请选择正确的图片格式上传(jpg，png，gif)'})
        return
    }
    // gif图片格式不做处理，其他静态图片做质量压缩处理以减小图片大小
    if (fileName == 'gif') {
        this.uploadApi(file, file.name)
    } else {
        let _this = this;
        // 压缩图片需要的一些元素和对象
        let reader = new FileReader(), img = new Image();
        reader.readAsDataURL(file);
        // 缩放图片需要的canvas
        let canvas = document.createElement('canvas');
        let context = canvas.getContext('2d');
        // base64地址图片加载完毕后
        img.onload = function() {
            // 图片原始尺寸
            let originWidth = this.width;
            let originHeight = this.height;
            canvas.width = originWidth;
            canvas.height = originHeight;
            // 清除画布
            context.clearRect(0, 0, originWidth, originHeight);
            // 图片压缩
            context.drawImage(img, 0, 0, originWidth, originHeight);
            // canvas转为blob并上传
            canvas.toBlob(function(blob) {
                _this.uploadApi(blob, file.name)
            }, file.type == 'image/gif' ? 'image/gif' : "image/jpeg", 0.6);
        }
        // 文件base64化，以便获知图片原始尺寸
        reader.onload = function(e) {
            img.src = e.target.result;
        };
    }
},
/**
 * 上传选中的图片文件
 *
 * @param  {obj}    file  图片文件
 * @param  {string} fileName  文件名称
 * */
uploadApi(file, fileName) {
    let formData = new FormData()
    formData.append('img', file, fileName)
    axios.post('/upload/upload-img', formData, {headers: {'Content-Type': 'multipart/form-data'}}).then((res) => {
        if (res.data.code == 200) {
            this.img_list.splice(this.img_list.length, 1, res.data.url)
        } else {
            this.$store.commit('setPrompt', {status: true, text: res.data.message})
        }
    })
}
```

感谢阅读，如有错误，欢迎指正交流。

参考文档:
[HTML5 file API 加 canvas 实现图片前端 JS 压缩并上传](https://www.zhangxinxu.top/wordpress/2017/07/html5-canvas-image-compress-upload/)

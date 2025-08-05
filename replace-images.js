const fs = require('fs');

// 读取cursor.md文件
const filePath = './source/_posts/cursor.md';
let content = fs.readFileSync(filePath, 'utf8');

// 固定前缀
const baseUrl = 'http://www.jiatt.top/2025/04/25/cursor/';

// 使用正则表达式匹配 {% asset_img filename "description" %} 格式
const assetImgRegex = /{% asset_img\s+([^\s]+)\s+"([^"]+)"\s*%}/g;

let matches = [];
let match;

// 找到所有匹配项
while ((match = assetImgRegex.exec(content)) !== null) {
  matches.push({
    fullMatch: match[0],
    filename: match[1],
    description: match[2]
  });
}

console.log(`🔍 找到 ${matches.length} 个图片引用需要替换：\n`);

// 执行替换
let changeCount = 0;
matches.forEach(({fullMatch, filename, description}) => {
  const newFormat = `![${description}](${baseUrl}${filename})`;
  
  if (content.includes(fullMatch)) {
    content = content.replace(fullMatch, newFormat);
    changeCount++;
    console.log(`✅ ${fullMatch} -> ${newFormat}`);
  }
});

// 同时处理文档示例中的引用（避免影响教程内容）
// 保留一些示例引用不变，只替换实际使用的图片
const exampleRefs = [
  '{% asset_img image1.png "图片描述" %}',
  '{% asset_img slug [width] [height] [title text [alt text]] %}',
  '# 在文章中使用 {% asset_img filename.jpg "描述" %}'
];

// 写回文件
fs.writeFileSync(filePath, content, 'utf8');

console.log(`\n🎉 批量替换完成！`);
console.log(`📊 统计信息：`);
console.log(`   - 共替换了 ${changeCount} 个图片引用`);
console.log(`   - 使用固定前缀：${baseUrl}`);
console.log(`   - 格式：![描述](${baseUrl}文件名)`); 
#!/bin/bash

# 图片URL数组
urls=(
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/a039c68f-b2f0-4e50-b3bc-e00b5e84030f.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/5f4db06a-d525-4f89-909e-262aafb67e96.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/432e4a50-f891-4ef3-8d9d-d4d8128eb09a.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/60576869-bd11-4ae7-b949-c47534e87b70.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/9def3acd-2d8e-41c0-baf5-6b74f224c09a.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/4b79e06a-f422-4d46-becd-4f1aadd8d80f.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/bdae5f48-575f-4bd2-8982-6d315be0e876.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/4b941d29-0f2e-4ac4-a02b-556bf8fc0482.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/e644aea5-3f75-4c80-9227-8ba166fe9540.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/2049c763-3591-4883-b78c-5bb264507f69.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/20e69eb6-31d1-40e4-8b3a-aff0641adaf5.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/5178eadf-5484-4b1c-9e0f-756df2c05f8e.jpeg"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/53484ba1-df3c-48fd-a975-de479c08e1c0.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/e0e48fe7-9517-4925-a973-db05e42a7561.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/cb4a6596-96fe-4c82-985e-87935dd169e4.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/cc74fcd7-5710-4ab2-aa37-feaed604169e.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/eec16266-9858-402b-ac23-9efa35ad830b.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/ea40f647-048a-4bfa-b16c-18dd451dc4b9.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/fc7416fa-3736-4ec4-9c39-8e4d959be738.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/527c7880-cad6-4cda-b65f-2122537286e5.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/ade08ffd-f4d4-433a-aa6f-9609c72cbee1.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/8a973aca-4132-48ef-9704-afd04505b6b8.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/aa89bcbb-bb1b-448b-ad9e-f1c21951528f.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/af828da1-5e7d-44f0-bcb9-ba6d14b29198.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/5dd22d70-77c7-4a52-9f52-000faa1b978b.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/c035e2d9-17c0-44ce-90bb-170af7723f68.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/54Lq35A4MGRe2l7E/img/17409090-7109-4e42-8389-2b0d62b08e97.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/40e64444-f1c1-4bb3-afe9-34c8d7d2d186.png"
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/98824bff-de2a-4083-a1d9-99795279c641.png"  
  "https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/mPdnpEk1oJQQGqw9/img/9403e0dc-d552-4f4b-bc70-c7108032eb61.png"
)

# 目标目录
target_dir="source/_posts/Cursor入门与实践/img"

echo "🚀 开始下载 ${#urls[@]} 张图片..."

success_count=0
fail_count=0

for i in "${!urls[@]}"; do
  url="${urls[$i]}"
  # 获取文件扩展名
  extension="${url##*.}"
  extension="${extension%%\?*}"  # 移除查询参数
  filename="image_$((i+1)).${extension}"
  output_path="${target_dir}/${filename}"
  
  echo "正在下载: $filename"
  
  # 使用curl下载图片
  if curl -L \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
    -H "Referer: https://alidocs.dingtalk.com/" \
    --connect-timeout 10 \
    --max-time 30 \
    -s \
    "$url" \
    -o "$output_path"; then
    
    # 检查文件是否下载成功且不为空
    if [[ -s "$output_path" ]]; then
      echo "✅ 下载成功: $filename"
      ((success_count++))
    else
      echo "❌ 下载失败: $filename (文件为空)"
      rm -f "$output_path"
      ((fail_count++))
    fi
  else
    echo "❌ 下载失败: $filename"
    ((fail_count++))
  fi
  
  # 添加延迟避免请求过于频繁
  sleep 0.5
done

echo ""
echo "📊 下载统计:"
echo "✅ 成功: $success_count 张"
echo "❌ 失败: $fail_count 张"
echo ""
echo "📂 文件保存在: $target_dir"

if [[ $success_count -gt 0 ]]; then
  echo "📝 接下来需要替换 Markdown 文件中的图片链接"
  echo "新的本地图片路径格式: /2025/04/25/Cursor入门与实践/img/image_X.png"
fi 
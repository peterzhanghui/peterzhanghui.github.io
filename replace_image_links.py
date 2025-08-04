#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

# 原始URL和新路径的映射
url_mapping = {
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/a039c68f-b2f0-4e50-b3bc-e00b5e84030f.png': 'img/image_1.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/5f4db06a-d525-4f89-909e-262aafb67e96.png': 'img/image_2.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/432e4a50-f891-4ef3-8d9d-d4d8128eb09a.png': 'img/image_3.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/60576869-bd11-4ae7-b949-c47534e87b70.png': 'img/image_4.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/9def3acd-2d8e-41c0-baf5-6b74f224c09a.png': 'img/image_5.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/4b79e06a-f422-4d46-becd-4f1aadd8d80f.png': 'img/image_6.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/bdae5f48-575f-4bd2-8982-6d315be0e876.png': 'img/image_7.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/4b941d29-0f2e-4ac4-a02b-556bf8fc0482.png': 'img/image_8.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/e644aea5-3f75-4c80-9227-8ba166fe9540.png': 'img/image_9.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/2049c763-3591-4883-b78c-5bb264507f69.png': 'img/image_10.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/20e69eb6-31d1-40e4-8b3a-aff0641adaf5.png': 'img/image_11.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/5178eadf-5484-4b1c-9e0f-756df2c05f8e.jpeg': 'img/image_12.jpeg',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/53484ba1-df3c-48fd-a975-de479c08e1c0.png': 'img/image_13.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/e0e48fe7-9517-4925-a973-db05e42a7561.png': 'img/image_14.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/cb4a6596-96fe-4c82-985e-87935dd169e4.png': 'img/image_15.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/cc74fcd7-5710-4ab2-aa37-feaed604169e.png': 'img/image_16.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/eec16266-9858-402b-ac23-9efa35ad830b.png': 'img/image_17.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/ea40f647-048a-4bfa-b16c-18dd451dc4b9.png': 'img/image_18.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/fc7416fa-3736-4ec4-9c39-8e4d959be738.png': 'img/image_19.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/527c7880-cad6-4cda-b65f-2122537286e5.png': 'img/image_20.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/ade08ffd-f4d4-433a-aa6f-9609c72cbee1.png': 'img/image_21.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/8a973aca-4132-48ef-9704-afd04505b6b8.png': 'img/image_22.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/aa89bcbb-bb1b-448b-ad9e-f1c21951528f.png': 'img/image_23.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/af828da1-5e7d-44f0-bcb9-ba6d14b29198.png': 'img/image_24.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/5dd22d70-77c7-4a52-9f52-000faa1b978b.png': 'img/image_25.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/c035e2d9-17c0-44ce-90bb-170af7723f68.png': 'img/image_26.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/54Lq35A4MGRe2l7E/img/17409090-7109-4e42-8389-2b0d62b08e97.png': 'img/image_27.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/40e64444-f1c1-4bb3-afe9-34c8d7d2d186.png': 'img/image_28.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/J9LnW62vGWdW5lvD/img/98824bff-de2a-4083-a1d9-99795279c641.png': 'img/image_29.png',
    'https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/mPdnpEk1oJQQGqw9/img/9403e0dc-d552-4f4b-bc70-c7108032eb61.png': 'img/image_30.png'
}

def replace_image_links(file_path):
    """替换Markdown文件中的图片链接"""
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    replacement_count = 0
    
    # 替换每个URL
    for old_url, new_path in url_mapping.items():
        if old_url in content:
            content = content.replace(old_url, new_path)
            replacement_count += 1
            print(f"✅ 已替换: {os.path.basename(old_url)} -> {new_path}")
    
    # 如果有替换，则写回文件
    if replacement_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n🎉 成功替换了 {replacement_count} 个图片链接")
        
        # 创建备份文件
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"📄 原文件已备份至: {backup_path}")
    else:
        print("❌ 没有找到需要替换的图片链接")
    
    return replacement_count

def main():
    markdown_file = 'source/_posts/Cursor入门与实践.md'
    
    if not os.path.exists(markdown_file):
        print(f"❌ 文件不存在: {markdown_file}")
        return
    
    print(f"📝 开始处理文件: {markdown_file}")
    print(f"🔍 将替换 {len(url_mapping)} 个图片链接...")
    print()
    
    replace_image_links(markdown_file)

if __name__ == '__main__':
    main() 
# GitHub Actions 依赖安装优化说明

## 🔧 已修复的问题

### 1. Node.js 版本不匹配
- **问题**: GitHub Actions 使用 Node.js 16.20.2，但 `sharp@0.34.3` 需要更新版本
- **解决**: 升级到 Node.js 18 (LTS 版本)
- **修改文件**: 
  - `.github/workflows/deploy.yml`: `node-version: "18"`
  - `package.json`: `"node": ">=18.0.0"`

### 2. NPM 镜像证书过期
- **问题**: 淘宝镜像 `registry.npmmirror.com` 证书过期
- **解决**: 使用官方源 + 备用镜像源策略
- **配置**:
  - 主源: `https://registry.npmjs.org/`
  - 备用源: `https://mirrors.ustc.edu.cn/npm/`

### 3. 缓存策略优化  
- **改进**: 从缓存 `node_modules` 改为缓存 `~/.npm`
- **优势**: 更高效的缓存利用率和跨项目复用

## 🚀 性能优化配置

```yaml
# 禁用不必要的功能提升安装速度
npm config set fund false
npm config set audit false
npm install --prefer-offline --no-audit
```

## 🛡️ 错误处理机制

```bash
# 自动备用源切换
if ! npm install --prefer-offline --no-audit; then
  echo "官方源失败，尝试使用中科大镜像源..."
  npm config set registry https://mirrors.ustc.edu.cn/npm/
  npm install --prefer-offline --no-audit
fi
```

## 📊 预期效果

- ✅ 解决证书过期错误
- ✅ 消除 Node.js 版本警告  
- ✅ 提升安装成功率和稳定性
- ✅ 优化构建时间和缓存效率

## 🔍 本地测试

```bash
# 切换到官方源
npm config set registry https://registry.npmjs.org/

# 清理并重新安装
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# 验证构建
npm run build
```

## 🎯 备用方案

如果官方源在某些地区访问较慢，可手动使用以下镜像源：

```bash
# 中科大镜像
npm config set registry https://mirrors.ustc.edu.cn/npm/

# 华为云镜像  
npm config set registry https://mirrors.huaweicloud.com/repository/npm/

# 腾讯云镜像
npm config set registry https://mirrors.cloud.tencent.com/npm/
```

---

**最后更新**: 2025-01-05  
**相关 Issue**: GitHub Actions 安装依赖报错 
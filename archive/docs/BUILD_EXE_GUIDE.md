# 🚀 天眼查GUI工具打包成EXE指南

## 📋 概述

本指南将帮助您将现代化的天眼查GUI工具打包成独立的exe可执行文件，方便在没有Python环境的Windows系统上运行。

## 🛠️ 准备工作

### 1. 环境要求
- Windows 操作系统
- Python 3.7 或更高版本
- 网络连接（用于下载依赖包）

### 2. 必要文件检查
确保以下文件存在于当前目录：
- ✅ `tianyancha_treeview.py` - 主程序文件
- ✅ `tianyancha_gui_main.py` - 打包入口文件
- ✅ `build_exe.py` - 自动打包脚本
- ✅ `build_exe.bat` - Windows批处理脚本
- ✅ `tianyancha_gui.spec` - PyInstaller配置文件
- ✅ `requirements.txt` - 依赖包列表

## 🚀 打包方法

### 方法1: 自动打包（推荐）

#### Windows用户
双击运行 `build_exe.bat` 文件，程序会自动：
1. 检查Python环境
2. 安装必要的依赖包
3. 清理构建目录
4. 构建exe文件
5. 复制相关文档

#### 或者使用Python脚本
```bash
python build_exe.py
```

### 方法2: 手动打包

#### 步骤1: 安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤2: 使用PyInstaller打包
```bash
# 使用spec文件打包（推荐）
pyinstaller tianyancha_gui.spec --clean

# 或者使用命令行参数
pyinstaller --onefile --windowed --name="天眼查企业信息查询工具" tianyancha_gui_main.py
```

## 📁 输出结果

打包完成后，您将在 `dist/` 目录中找到：

```
dist/
├── 天眼查企业信息查询工具.exe    # 主程序文件
├── 使用说明.txt                   # 用户使用指南
├── GUI_UPGRADE_README.md          # 升级说明
├── UPGRADE_SUMMARY.md             # 升级总结
├── TAB_STYLE_UPDATE.md            # 样式更新说明
└── requirements.txt               # 依赖列表
```

## 🎯 exe文件特点

### 功能完整性
- ✅ 包含所有GUI功能
- ✅ 现代化界面设计
- ✅ 微软雅黑字体支持
- ✅ 完整的查询功能
- ✅ 数据复制和导出
- ✅ 快捷键支持

### 独立运行
- ✅ 无需安装Python环境
- ✅ 无需安装额外依赖包
- ✅ 双击即可运行
- ✅ 支持Windows 7/8/10/11

### 文件大小
- 预计大小：约 15-25 MB
- 包含所有必要的Python运行时
- 包含所有依赖库

## ⚙️ 自定义配置

### 修改图标
在 `tianyancha_gui.spec` 文件中修改：
```python
icon='your_icon.ico'  # 指定图标文件路径
```

### 修改程序名称
在 `tianyancha_gui.spec` 文件中修改：
```python
name='您的程序名称'
```

### 控制台显示
在 `tianyancha_gui.spec` 文件中修改：
```python
console=False  # False=隐藏控制台，True=显示控制台
```

## 🐛 常见问题

### 问题1: 缺少模块错误
**解决方案**: 在 `tianyancha_gui.spec` 的 `hiddenimports` 中添加缺少的模块

### 问题2: exe文件过大
**解决方案**: 
- 使用 `--exclude-module` 排除不需要的模块
- 使用UPX压缩（已在spec中启用）

### 问题3: 启动缓慢
**解决方案**: 
- 这是正常现象，首次启动需要解压文件
- 可以考虑使用 `--onedir` 模式

### 问题4: 杀毒软件误报
**解决方案**: 
- 将exe文件添加到杀毒软件白名单
- 这是PyInstaller打包程序的常见问题

## 📦 分发建议

### 打包分发
建议将整个 `dist/` 目录打包成zip文件分发：
```
天眼查企业信息查询工具_v1.0.zip
├── 天眼查企业信息查询工具.exe
├── 使用说明.txt
└── 其他文档...
```

### 用户说明
提醒用户：
1. 首次运行可能需要几秒钟启动时间
2. 需要网络连接才能查询数据
3. 首次使用需要配置cookies
4. 建议添加到杀毒软件白名单

## 🔧 高级选项

### 优化启动速度
```bash
# 使用目录模式而非单文件模式
pyinstaller --onedir tianyancha_gui_main.py
```

### 添加版本信息
创建 `version.txt` 文件并在spec中引用：
```python
version_info='version.txt'
```

### 数字签名
如果有代码签名证书：
```python
codesign_identity='Your Certificate Name'
```

## ✅ 验证测试

打包完成后，建议进行以下测试：
1. 在干净的Windows系统上运行
2. 测试所有主要功能
3. 测试网络连接和数据查询
4. 测试配置保存和加载
5. 测试快捷键功能

---

**开发者**: Machy@HTSC  
**版本**: v1.0  
**更新时间**: 2025年1月

现在您可以轻松地将天眼查GUI工具打包成exe文件，方便分发和使用！🎊

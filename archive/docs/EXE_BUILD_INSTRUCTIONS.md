# 🚀 天眼查GUI工具EXE打包说明

## 📋 快速开始

我已经为您准备了多种打包方法，选择最适合您的方式：

### 方法1: 一键打包（推荐）
双击运行 `manual_build.bat` 文件，程序会自动完成所有步骤。

### 方法2: Python脚本打包
```bash
python simple_build.py
```

### 方法3: 手动命令行打包
```bash
# 安装PyInstaller（如果还没安装）
pip install pyinstaller

# 执行打包命令
pyinstaller --onefile --windowed --name="天眼查企业信息查询工具" --add-data="tianyancha_treeview.py;." --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=requests --hidden-import=bs4 --hidden-import=beautifulsoup4 --clean tianyancha_gui_main.py
```

## 📁 文件说明

### 打包相关文件
- `tianyancha_gui_main.py` - 主程序入口（用于打包）
- `tianyancha_treeview.py` - GUI核心代码
- `manual_build.bat` - Windows一键打包脚本
- `simple_build.py` - Python打包脚本
- `tianyancha_gui.spec` - PyInstaller配置文件（高级用户）
- `build_exe.py` - 完整自动化打包脚本（网络良好时使用）

### 输出文件
打包完成后，在 `dist/` 目录中您会找到：
- `天眼查企业信息查询工具.exe` - 主程序文件
- `使用说明.txt` - 用户使用指南

## 🎯 exe文件特点

### ✅ 功能完整
- 现代化蓝色主题界面
- 微软雅黑字体，中文显示清晰
- 完整的企业信息查询功能
- 支持基本信息、股东、人员、财务、投资查询
- 支持数据复制和导出
- 支持快捷键操作

### ✅ 独立运行
- 无需安装Python环境
- 无需安装额外依赖包
- 双击即可运行
- 支持Windows 7/8/10/11

### ✅ 文件信息
- 预计大小：15-25 MB
- 包含完整Python运行时
- 包含所有必要依赖库

## 🔧 自定义选项

### 修改程序图标
如果您有图标文件（.ico格式），可以在打包命令中添加：
```bash
--icon=your_icon.ico
```

### 隐藏控制台窗口
默认配置已隐藏控制台，如需显示调试信息，可以移除 `--windowed` 参数。

### 优化文件大小
如果exe文件过大，可以尝试：
```bash
# 使用目录模式（而非单文件）
pyinstaller --onedir --windowed --name="天眼查企业信息查询工具" tianyancha_gui_main.py

# 排除不需要的模块
--exclude-module=matplotlib --exclude-module=numpy
```

## 🐛 常见问题解决

### 问题1: "找不到pyinstaller"
**解决方案**:
```bash
pip install pyinstaller
```

### 问题2: 打包失败，提示缺少模块
**解决方案**: 在打包命令中添加 `--hidden-import=模块名`

### 问题3: exe文件运行时报错
**解决方案**: 
1. 检查是否缺少依赖文件
2. 尝试在命令行中运行exe查看详细错误信息
3. 使用 `--onedir` 模式打包

### 问题4: 杀毒软件误报
**解决方案**: 
- 将exe文件添加到杀毒软件白名单
- 这是PyInstaller打包程序的常见现象

### 问题5: 启动缓慢
**解决方案**: 
- 首次启动需要解压，属于正常现象
- 后续启动会更快
- 可以考虑使用 `--onedir` 模式

## 📦 分发建议

### 打包分发
建议创建一个包含以下文件的zip包：
```
天眼查企业信息查询工具_v1.0.zip
├── 天眼查企业信息查询工具.exe
├── 使用说明.txt
├── 配置说明.md（可选）
└── 更新日志.md（可选）
```

### 用户提醒
分发时提醒用户：
1. 首次运行可能需要几秒钟启动时间
2. 需要网络连接才能查询数据
3. 首次使用需要配置有效的cookies
4. 建议添加到杀毒软件白名单
5. 支持Windows 7及以上系统

## 🎉 完成验证

打包完成后，建议进行以下测试：
- [ ] 在当前电脑上运行exe文件
- [ ] 测试基本查询功能
- [ ] 测试配置保存功能
- [ ] 测试数据复制功能
- [ ] 在其他Windows电脑上测试（如果可能）

## 📞 技术支持

如果在打包过程中遇到问题：
1. 检查Python环境是否正常
2. 确保所有必要文件都在当前目录
3. 检查网络连接是否正常
4. 查看错误信息并根据提示解决

---

**开发者**: Machy@HTSC  
**版本**: 现代化版本 v1.0  
**更新时间**: 2025年1月

现在您可以轻松地将天眼查GUI工具打包成独立的exe文件了！🎊

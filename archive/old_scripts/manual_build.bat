@echo off
chcp 65001 >nul
echo 🚀 手动打包天眼查GUI工具
echo ========================
echo.

echo 🔍 检查PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到PyInstaller，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller安装失败
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller已准备就绪
echo.

echo 🧹 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "天眼查企业信息查询工具.spec" del "天眼查企业信息查询工具.spec"

echo 🔨 开始打包...
pyinstaller --onefile --windowed --name="天眼查企业信息查询工具" --add-data="tianyancha_treeview.py;." --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=requests --hidden-import=bs4 --hidden-import=beautifulsoup4 --clean tianyancha_gui_main.py

if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ✅ 打包成功！
echo 📁 输出文件: dist\天眼查企业信息查询工具.exe
echo.

echo 📝 创建使用说明...
echo 天眼查企业信息查询工具 - 现代化版本 > "dist\使用说明.txt"
echo. >> "dist\使用说明.txt"
echo 使用方法： >> "dist\使用说明.txt"
echo 1. 双击运行程序 >> "dist\使用说明.txt"
echo 2. 输入企业名称进行查询 >> "dist\使用说明.txt"
echo 3. 首次使用需要配置cookies >> "dist\使用说明.txt"
echo. >> "dist\使用说明.txt"
echo 开发者: Machy@HTSC >> "dist\使用说明.txt"
echo 版本: 现代化版本 v1.0 >> "dist\使用说明.txt"

echo ✅ 使用说明已创建
echo.
echo 🎉 构建完成！您可以在dist目录中找到可执行文件。
echo.
pause

@echo off
chcp 65001 >nul
echo 🚀 天眼查GUI工具自动打包程序
echo ================================
echo.

echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python环境，请先安装Python
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.

echo 🔄 开始自动构建...
python build_exe.py

echo.
echo 构建完成！按任意键退出...
pause >nul

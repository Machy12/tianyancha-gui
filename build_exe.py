#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天眼查GUI工具自动打包脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}...")
    print(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        print(f"✅ {description}成功")
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败")
        print(f"错误: {e}")
        if e.stdout:
            print(f"标准输出: {e.stdout}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def check_dependencies():
    """检查必要的依赖"""
    print("🔍 检查依赖包...")
    
    required_packages = ['requests', 'beautifulsoup4', 'lxml', 'pyinstaller']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - 已安装")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("正在自动安装...")
        
        for package in missing_packages:
            if not run_command(f"pip install {package}", f"安装 {package}"):
                return False
    
    return True

def clean_build_dirs():
    """清理构建目录"""
    print("\n🧹 清理构建目录...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.pyc']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 已删除目录: {dir_name}")
    
    # 清理pyc文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_exe():
    """构建exe文件"""
    print("\n🔨 开始构建exe文件...")
    
    # 使用spec文件构建
    if os.path.exists('tianyancha_gui.spec'):
        cmd = "pyinstaller tianyancha_gui.spec --clean"
    else:
        # 如果没有spec文件，使用基本命令
        cmd = ('pyinstaller --onefile --windowed '
               '--name="天眼查企业信息查询工具" '
               '--add-data="tianyancha_treeview.py;." '
               'tianyancha_gui_main.py')
    
    return run_command(cmd, "构建exe文件")

def copy_additional_files():
    """复制额外的文件到dist目录"""
    print("\n📁 复制额外文件...")
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ dist目录不存在")
        return False
    
    # 要复制的文件
    files_to_copy = [
        'GUI_UPGRADE_README.md',
        'UPGRADE_SUMMARY.md',
        'TAB_STYLE_UPDATE.md',
        'requirements.txt'
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir)
            print(f"✅ 已复制: {file_name}")
    
    return True

def create_readme():
    """创建exe使用说明"""
    readme_content = """# 天眼查企业信息查询工具 - 现代化版本

## 使用说明

1. 双击 "天眼查企业信息查询工具.exe" 启动程序
2. 在搜索框中输入企业名称
3. 点击"开始查询"按钮或按Enter键
4. 查看查询结果，支持复制和导出

## 功能特点

- 现代化蓝色主题界面
- 微软雅黑字体，中文显示清晰
- 支持企业基本信息查询
- 支持股东信息查询
- 支持主要人员信息查询
- 支持财务数据查询
- 支持对外投资信息查询
- 支持数据复制和导出
- 支持快捷键操作

## 快捷键

- Enter: 开始查询
- F1: 打开配置
- 1-5: 切换标签页
- Ctrl+A: 全选
- Ctrl+C: 复制
- ESC: 退出程序

## 注意事项

1. 首次使用需要配置有效的cookies
2. 确保网络连接正常
3. 查询频率不要过高，避免被限制

## 技术支持

开发者: Machy@HTSC
版本: 现代化版本 v1.0
更新时间: 2025年1月

如有问题请联系开发者。
"""
    
    with open('dist/使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 已创建使用说明.txt")

def main():
    """主函数"""
    print("🚀 天眼查GUI工具自动打包程序")
    print("=" * 50)
    
    # 检查当前目录
    required_files = ['tianyancha_gui_main.py', 'tianyancha_treeview.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    # 执行构建步骤
    steps = [
        (check_dependencies, "检查依赖"),
        (clean_build_dirs, "清理构建目录"),
        (build_exe, "构建exe文件"),
        (copy_additional_files, "复制额外文件"),
        (create_readme, "创建使用说明")
    ]
    
    for step_func, step_name in steps:
        if not step_func():
            print(f"\n❌ {step_name}失败，构建中止")
            return False
    
    print("\n🎉 构建完成！")
    print("=" * 50)
    print("📁 输出目录: dist/")
    print("📄 可执行文件: dist/天眼查企业信息查询工具.exe")
    print("📖 使用说明: dist/使用说明.txt")
    print("\n✅ 您现在可以将dist目录中的文件分发给其他用户使用了！")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\n按Enter键退出...")
    sys.exit(0 if success else 1)

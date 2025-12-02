#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的exe打包脚本
"""

import os
import sys
import subprocess

def main():
    print("🚀 简化版exe打包脚本")
    print("=" * 40)
    
    # 检查必要文件
    if not os.path.exists('tianyancha_gui_main.py'):
        print("❌ 缺少 tianyancha_gui_main.py 文件")
        return False
    
    if not os.path.exists('tianyancha_treeview.py'):
        print("❌ 缺少 tianyancha_treeview.py 文件")
        return False
    
    print("✅ 必要文件检查通过")
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=天眼查企业信息查询工具',
        '--add-data=tianyancha_treeview.py;.',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=requests',
        '--hidden-import=bs4',
        '--hidden-import=beautifulsoup4',
        '--clean',
        'tianyancha_gui_main.py'
    ]
    
    print(f"🔨 执行打包命令...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ 打包成功！")
        print("📁 输出文件: dist/天眼查企业信息查询工具.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ 未找到 pyinstaller，请先安装:")
        print("   pip install pyinstaller")
        return False

if __name__ == "__main__":
    success = main()
    input("\n按Enter键退出...")
    sys.exit(0 if success else 1)

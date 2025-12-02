#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天眼查企业信息查询工具 - 现代化GUI主程序
用于打包成exe的主入口文件
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

# 添加当前目录到Python路径
if hasattr(sys, '_MEIPASS'):
    # PyInstaller打包后的路径
    base_path = sys._MEIPASS
else:
    # 开发环境路径
    base_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_path)

def show_error(title, message):
    """显示错误对话框"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showerror(title, message)
    root.destroy()

def main():
    """主程序入口"""
    try:
        print("🚀 启动天眼查企业信息查询工具...")
        print("版本: 现代化GUI v1.0")
        print("开发者: Machy@HTSC")
        print("=" * 50)
        
        # 导入现代化GUI类
        from tianyancha_treeview import ModernTianyanchaGUI
        
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口图标（如果有的话）
        try:
            # 可以在这里设置图标
            # root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        # 设置窗口属性
        root.resizable(True, True)
        root.minsize(1200, 800)
        
        # 创建现代化GUI应用
        app = ModernTianyanchaGUI(root)
        
        print("✅ GUI界面已启动")
        print("💡 功能特点:")
        print("   - 现代化蓝色主题设计")
        print("   - 微软雅黑字体，中文显示更清晰")
        print("   - 卡片式布局，界面更美观")
        print("   - 完整的企业信息查询功能")
        print("   - 支持数据复制和导出")
        print("   - 快捷键操作支持")
        print("=" * 50)
        
        # 启动GUI主循环
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"导入模块失败：{str(e)}\n\n请确保所有必要的Python包已安装：\n- tkinter\n- requests\n- beautifulsoup4"
        print(f"❌ 错误: {error_msg}")
        show_error("导入错误", error_msg)
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"程序启动失败：{str(e)}\n\n详细错误信息：\n{traceback.format_exc()}"
        print(f"❌ 错误: {error_msg}")
        show_error("启动错误", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天眼查GUI演示脚本 - 可以选择运行新旧版本GUI
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def show_selection_dialog():
    """显示GUI版本选择对话框"""
    root = tk.Tk()
    root.title("天眼查GUI版本选择")
    root.geometry("500x400")
    root.resizable(False, False)
    
    # 设置窗口居中
    root.eval('tk::PlaceWindow . center')
    
    # 主框架
    main_frame = tk.Frame(root, bg='#f8fafc', padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    title_label = tk.Label(main_frame, 
                          text="🔍 天眼查企业信息查询工具",
                          font=('Microsoft YaHei', 16, 'bold'),
                          bg='#f8fafc',
                          fg='#1e293b')
    title_label.pack(pady=(0, 10))
    
    subtitle_label = tk.Label(main_frame,
                             text="请选择要使用的GUI版本",
                             font=('Microsoft YaHei', 12),
                             bg='#f8fafc',
                             fg='#64748b')
    subtitle_label.pack(pady=(0, 30))
    
    # 版本选择框架
    version_frame = tk.Frame(main_frame, bg='#f8fafc')
    version_frame.pack(fill=tk.X, pady=20)
    
    # 现代版本选项
    modern_frame = tk.Frame(version_frame, bg='white', relief='solid', bd=1)
    modern_frame.pack(fill=tk.X, pady=(0, 15))
    
    modern_inner = tk.Frame(modern_frame, bg='white', padx=20, pady=20)
    modern_inner.pack(fill=tk.X)
    
    modern_title = tk.Label(modern_inner,
                           text="🎨 现代化版本 (推荐)",
                           font=('Microsoft YaHei', 14, 'bold'),
                           bg='white',
                           fg='#2563eb')
    modern_title.pack(anchor=tk.W)
    
    modern_desc = tk.Label(modern_inner,
                          text="• 现代化蓝色主题设计\n• 卡片式布局，界面更清晰\n• 优化的字体和间距\n• 更直观的状态提示\n• 保持所有原有功能",
                          font=('Microsoft YaHei', 10),
                          bg='white',
                          fg='#64748b',
                          justify=tk.LEFT)
    modern_desc.pack(anchor=tk.W, pady=(5, 10))
    
    modern_btn = tk.Button(modern_inner,
                          text="启动现代化版本",
                          font=('Microsoft YaHei', 11, 'bold'),
                          bg='#2563eb',
                          fg='white',
                          relief='flat',
                          padx=20,
                          pady=8,
                          command=lambda: launch_gui('modern', root))
    modern_btn.pack(anchor=tk.W)
    
    # 原始版本选项
    classic_frame = tk.Frame(version_frame, bg='white', relief='solid', bd=1)
    classic_frame.pack(fill=tk.X)
    
    classic_inner = tk.Frame(classic_frame, bg='white', padx=20, pady=20)
    classic_inner.pack(fill=tk.X)
    
    classic_title = tk.Label(classic_inner,
                            text="📋 原始版本",
                            font=('Microsoft YaHei', 14, 'bold'),
                            bg='white',
                            fg='#64748b')
    classic_title.pack(anchor=tk.W)
    
    classic_desc = tk.Label(classic_inner,
                           text="• 传统的系统默认样式\n• 经典的表单布局\n• 稳定可靠的界面\n• 所有功能完整保留",
                           font=('Microsoft YaHei', 10),
                           bg='white',
                           fg='#64748b',
                           justify=tk.LEFT)
    classic_desc.pack(anchor=tk.W, pady=(5, 10))
    
    classic_btn = tk.Button(classic_inner,
                           text="启动原始版本",
                           font=('Microsoft YaHei', 11),
                           bg='#64748b',
                           fg='white',
                           relief='flat',
                           padx=20,
                           pady=8,
                           command=lambda: launch_gui('classic', root))
    classic_btn.pack(anchor=tk.W)
    
    # 底部信息
    info_label = tk.Label(main_frame,
                         text="💡 两个版本功能完全相同，仅界面风格不同\n开发者: Machy@HTSC",
                         font=('Microsoft YaHei', 9),
                         bg='#f8fafc',
                         fg='#94a3b8',
                         justify=tk.CENTER)
    info_label.pack(side=tk.BOTTOM, pady=(30, 0))
    
    root.mainloop()

def launch_gui(version, parent_root):
    """启动指定版本的GUI"""
    parent_root.destroy()
    
    try:
        if version == 'modern':
            from tianyancha_treeview import ModernTianyanchaGUI
            root = tk.Tk()
            app = ModernTianyanchaGUI(root)
            print("🎨 已启动现代化版本GUI")
        else:
            # 注意：原始版本已被注释，这里只是演示
            messagebox.showinfo("提示", 
                              "原始版本已被注释保留。\n如需使用，请在tianyancha_treeview.py中取消注释TianyanchaTreeviewGUI类。\n\n现在将启动现代化版本。")
            from tianyancha_treeview import ModernTianyanchaGUI
            root = tk.Tk()
            app = ModernTianyanchaGUI(root)
            print("📋 已启动GUI（现代化版本）")
        
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("错误", f"启动GUI失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 天眼查GUI版本选择器")
    print("=" * 50)
    show_selection_dialog()

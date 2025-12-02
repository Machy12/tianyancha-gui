#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行现代化天眼查GUI的启动脚本
"""

import tkinter as tk
from tianyancha_treeview import ModernTianyanchaGUI

def main():
    """启动现代化GUI"""
    print("🚀 启动现代化天眼查GUI...")
    
    # 创建主窗口
    root = tk.Tk()
    
    # 设置窗口图标（如果有的话）
    try:
        # root.iconbitmap('icon.ico')  # 如果有图标文件
        pass
    except:
        pass
    
    # 创建现代化GUI应用
    app = ModernTianyanchaGUI(root)
    
    print("✅ GUI已启动，享受现代化的查询体验！")
    print("💡 主要改进：")
    print("   - 现代化的蓝色主题设计")
    print("   - 更清晰的卡片式布局")
    print("   - 优化的字体和间距")
    print("   - 更直观的状态提示")
    print("   - 保持所有原有功能不变")
    
    # 启动GUI主循环
    root.mainloop()

if __name__ == "__main__":
    main()
